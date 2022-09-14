"""Load Huggingface model and tokenizer into a Snowflake stage."""
from datetime import datetime
from pathlib import Path
from typing import List, Type, Union

from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizer,
)

from scripts import Session
from snowflake_ml import __version__


def huggingface2snowflake(
    session: Session,
    huggingface_obj: Union[Type[PreTrainedModel], Type[PreTrainedTokenizer]],
    hugginface_name: str = "unitary/toxic-bert",
    local_model: Path = Path.cwd() / "models" / "toxic_bert",
    stage_model: str = "@ml_models",
) -> List[str]:
    """Download huggingface object and put it in Snowflake stage."""
    huggingface_obj.from_pretrained(
        hugginface_name,
        cache_dir="/tmp",
    ).save_pretrained(local_model)
    model = session.file.put(
        local_file_name=str(local_model)
        if local_model.is_file()
        else f"{local_model}/*",
        stage_location=stage_model,
        overwrite=True,
    )
    return [m.target for m in model]


if __name__ == "__main__":
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    with Session(
        database="snowflake_ml",
        account="vw42238",
        user="murilo",
        warehouse='"reddit_xs"',
        role="accountadmin",
        region="eu-central-1",
        schema="reddit",
    ) as session:
        model_targets = huggingface2snowflake(
            session=session,
            huggingface_obj=AutoModelForSequenceClassification,
            local_model=Path.cwd() / "models" / "toxic_bert_model",
            stage_model=f"@ml_models/{__version__}/{now}/model/",
        )
        tokenizer_targets = huggingface2snowflake(
            session=session,
            huggingface_obj=AutoTokenizer,
            local_model=Path.cwd() / "models" / "toxic_bert_tokenizer",
            stage_model=f"@ml_models/{__version__}/{now}/tokenizer/",
        )
        print(model_targets, tokenizer_targets)
