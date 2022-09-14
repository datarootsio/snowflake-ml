"""Move datasets to Snowflake tables."""
from pathlib import Path
from typing import Sequence

import pandas as pd

from scripts import Session


def _write_pd(df: pd.DataFrame, table_name: str, session: Session) -> None:
    """Write pandas dataframe to Snowflake."""
    return (
        session.create_dataframe(data=df)
        .write.mode("overwrite")
        .save_as_table(table_name)
    )


def _merge_labels(
    *dfs: pd.DataFrame,
    target_cols: Sequence[str] = (
        "toxic",
        "severe_toxic",
        "obscene",
        "threat",
        "insult",
        "identity_hate",
    ),
    out_cols: Sequence[str] = ("id", "comment_text", "is_toxic")
) -> pd.DataFrame:
    """Merge toxicity labels."""
    if not (0 < len(dfs) <= 2):
        raise ValueError("Must pass 1 or 2 dataframes.")
    if len(dfs) > 1:
        text, labels = dfs
        data = pd.concat([text, labels], join="inner", axis="columns").loc[
            :, lambda _df: ~_df.columns.duplicated()
        ]
    else:
        data = dfs[0]
    return (
        data.assign(is_toxic=data[target_cols].sum(axis="columns").astype("bool"))
        .loc[:, out_cols]
        .reset_index(drop=True)
    )


if __name__ == "__main__":
    # Using `private_key_filepath` and `private_key_passphrase` from env vars
    DATA_PATH = Path(__file__).parents[1] / "data" / "raw"

    train = DATA_PATH / "train.csv"
    test = DATA_PATH / "test.csv"
    test_labels = DATA_PATH / "test_labels.csv"

    train = _merge_labels(pd.read_csv(train))
    test = _merge_labels(pd.read_csv(test), pd.read_csv(test_labels))

    with Session(
        database="snowflake_ml",
        account="vw42238",
        user="murilo",
        warehouse='"reddit_xs"',
        role="accountadmin",
        region="eu-central-1",
        schema="reddit",
    ) as session:
        _write_pd(df=train, table_name="train", session=session)
        _write_pd(df=test, table_name="test", session=session)
