"""Train models on Snowflake and save artifacts to stages."""
from pathlib import Path

from scripts.snowflake_utils import Session

# from snowflake_ml.model import get_model_untrained, train, save_model
# from snowflake_ml import __version__


def local_train(_session: Session, model_output_dir: str = "/tmp") -> None:
    """Train transformer locally and push weights to Snowflake Stage."""
    from snowflake_ml import __version__
    from snowflake_ml.model import get_model_untrained, save_model, train

    df = _session.table("train").limit(100).to_pandas()
    model = get_model_untrained()
    trained_model = train(
        model=model, output_dir=model_output_dir, train_data=df, num_train_epochs=1
    )
    save_model(model=trained_model, model_dir=Path(model_output_dir))
    _session.file.put(
        local_file_name=f"{model_output_dir}/model.pth",
        stage_location=f"@ml_models/{__version__}",
        overwrite=True,
    )


if __name__ == "__main__":
    with Session(
        database="snowflake_ml",
        account="vw42238",
        user="murilo",
        warehouse='"reddit_xs"',
        role="accountadmin",
        region="eu-central-1",
        schema="reddit",
    ) as _session:
        local_train(_session=_session, model_output_dir="models/")
