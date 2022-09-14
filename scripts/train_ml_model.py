"""Train models on Snowflake and save artifacts to stages."""
from datetime import datetime
from pathlib import Path
from typing import List

from snowflake.snowpark.file_operation import PutResult
from snowflake.snowpark.functions import sproc
from snowflake.snowpark.session import Session as SnowparkSession
from transformers import AutoTokenizer

from scripts.snowflake_utils import Session
from snowflake_ml import __version__


def local_train(
    session: Session, model_output_dir: Path = Path("/tmp")
) -> List[PutResult]:
    """Train transformer locally and push weights to Snowflake Stage."""
    from snowflake_ml import __version__
    from snowflake_ml.model import get_model_untrained, save_model, train

    df = session.table("train").limit(100).to_pandas()
    model = get_model_untrained("unitary/toxic-bert")
    tokenizer = AutoTokenizer.from_pretrained("unitary/toxic-bert")
    trained_model = train(
        model=model,
        tokenizer=tokenizer,
        output_dir=str(model_output_dir),
        train_data=df,
        num_train_epochs=1,
    )
    save_model(model=trained_model, model_dir=model_output_dir)
    return session.file.put(
        local_file_name=str(model_output_dir / "model.pth"),
        stage_location=f"@ml_models/{__version__}",
        overwrite=True,
    )


def snowflake_train(
    _session: Session, stage_model: str, stage_tokenizer: str
) -> List[str]:
    """Train model on Snowflake compute."""
    custom_libpath = sorted(Path("dist/").glob("*.whl"))[-1]
    if not custom_libpath.is_file():
        raise ValueError(f"Expected wheel file, got {custom_libpath}.")

    now = datetime.now().strftime("%Y%m%d-%H%M%S")

    @sproc(
        name="ml_train",
        packages=[
            "snowflake-snowpark-python==0.8.0",
            "transformers==4.18.0",
            "pytorch==1.10.2",
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
        from transformers import AutoTokenizer

        from snowflake_ml import __version__
        from snowflake_ml.misc import ungz
        from snowflake_ml.model import get_model_untrained, save_model, train

        root_dir = Path("/tmp")
        train_model_dir = Path(root_dir) / "trained"
        if Path(stage_model).suffix == "":
            model_target = root_dir / Path(stage_model).name
        if Path(stage_tokenizer).suffix == "":
            tokenizer_target = root_dir / Path(stage_tokenizer).name

        session.file.get(stage_location=stage_model, target_directory=str(model_target))
        session.file.get(
            stage_location=stage_tokenizer, target_directory=str(tokenizer_target)
        )

        ungz(*list(model_target.rglob("*.gz")), *list(tokenizer_target.rglob("*.gz")))

        df = session.table("train").limit(100).to_pandas()
        model = get_model_untrained(str(model_target))
        tokenizer = AutoTokenizer.from_pretrained("unitary/toxic-bert")
        trained_model = train(
            model=model,
            tokenizer=tokenizer,
            output_dir=str(train_model_dir),
            train_data=df,
            num_train_epochs=1,
        )
        save_model(model=trained_model, model_dir=train_model_dir)
        model = session.file.put(
            local_file_name=f"{train_model_dir}/model.pth",
            stage_location=f"@ml_models/{__version__}",
            overwrite=True,
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
        warehouse="reddit_xl",
        role="accountadmin",
        region="eu-central-1",
        schema="reddit",
    ) as _session:
        snowflake_train(
            _session=_session,
            stage_model="ml_models/0.0.0.dev0/20220914-111057/model/",
            stage_tokenizer="ml_models/0.0.0.dev0/20220914-111444/tokenizer/",
        )
