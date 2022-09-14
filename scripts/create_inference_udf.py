"""Create inference UDF using python Snowpark."""
import os
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from sklearn.pipeline import Pipeline
from snowflake.snowpark.functions import pandas_udf
from snowflake.snowpark.types import PandasSeries

from scripts import Session
from snowflake_ml import __version__
from snowflake_ml.model import load_model


def create_udf_from_stage(_session: Session, pipe: Pipeline) -> None:
    """Create UDF with custom python code."""
    custom_libpath = sorted(Path("dist/").glob("*.whl"))[-1]
    if not custom_libpath.is_file():
        raise ValueError(f"Expected wheel file, got {custom_libpath}.")

    now = datetime.now().strftime("%Y%m%d-%H%M%S")

    @pandas_udf(
        name=f"ml_predict_{os.getenv('ENVIRONMENT', 'DEV')}",
        is_permanent=True,
        stage_location=f"@py_udfs/{__version__}/{now}",
        replace=True,
        imports=[str(custom_libpath)],
        packages=[
            "snowflake-snowpark-python==0.8.0",
            "scikit-learn==1.1.1",
            "joblib==1.1.0",
        ],
        session=_session,
    )
    def run(ds: PandasSeries[str]) -> PandasSeries[dict]:
        import os
        import sys

        import_dir = sys._xoptions["snowflake_import_directory"]
        sys.path.append(os.path.join(import_dir, custom_libpath.name))

        import pandas as pd

        from snowflake_ml import __version__
        from snowflake_ml.model import predict

        predictions = pd.DataFrame(
            {"prediction": predict(pipe=pipe, text=ds), "model_version": __version__}
        )
        return pd.Series(predictions.to_dict("records"))


if __name__ == "__main__":
    with Session(
        database="snowflake_ml",
        account="vw42238",
        user="murilo",
        warehouse='"reddit_xs"',
        role="accountadmin",
        region="eu-central-1",
        schema="reddit",
    ) as _session, TemporaryDirectory() as tmpdir:
        artifacts = _session.file.get(
            stage_location="ml_models/0.0.0.dev0/20220914-191458/tmperna0zc3.joblib.gz",
            target_directory=tmpdir,
        )
        if len(artifacts) != 1:
            raise ValueError(f"Expected one artifact, got {len(artifacts)}.")

        pipe = load_model(Path(tmpdir) / Path(artifacts[0].file).name)
        create_udf_from_stage(_session=_session, pipe=pipe)
