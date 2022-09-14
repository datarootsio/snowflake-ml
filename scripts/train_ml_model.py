"""Train models on Snowflake and save artifacts to stages."""
from datetime import datetime
from pathlib import Path
from typing import List

from snowflake.snowpark.functions import sproc
from snowflake.snowpark.session import Session as SnowparkSession

from scripts import Session
from snowflake_ml import __version__


def snowflake_train(_session: Session) -> List[str]:
    """Train model on Snowflake compute."""
    custom_libpath = sorted(Path("dist/").glob("*.whl"))[-1]
    if not custom_libpath.is_file():
        raise ValueError(f"Expected wheel file, got {custom_libpath}.")

    now = datetime.now().strftime("%Y%m%d-%H%M%S")

    @sproc(
        name="ml_train",
        packages=[
            "snowflake-snowpark-python==0.8.0",
            "scikit-learn==1.1.1",
        ],
        imports=[str(custom_libpath)],
        stage_location=f"@ml_models/{__version__}/{now}",
        replace=True,
        is_permanent=False,
    )
    def run(session: SnowparkSession) -> List[str]:
        import os
        import sys

        import_dir = sys._xoptions["snowflake_import_directory"]
        sys.path.append(os.path.join(import_dir, custom_libpath.name))

        from tempfile import NamedTemporaryFile

        from snowflake_ml import __version__
        from snowflake_ml.model import save_model, train

        root_artifacts = Path("/tmp")

        df = session.table("train").to_pandas()

        pipe = train(text=df["comment_text"], labels=df["is_toxic"], dir=root_artifacts)
        with NamedTemporaryFile(dir=root_artifacts, suffix=".joblib.gz") as tmpfile:
            save_model(pipeline=pipe, file=tmpfile)
            model = session.file.put(
                local_file_name=tmpfile.name,
                stage_location=f"@ml_models/{__version__}/{now}",
                overwrite=False,
            )
        return [m.target for m in model]

    return _session.call(sproc_name="ml_train")


if __name__ == "__main__":
    import subprocess

    subprocess.check_call(["poetry", "build", "-f", "wheel"])

    with Session(
        database="snowflake_ml",
        account="vw42238",
        user="murilo",
        warehouse='"reddit_xs"',
        role="accountadmin",
        region="eu-central-1",
        schema="reddit",
    ) as _session:
        snowflake_train(_session=_session)
