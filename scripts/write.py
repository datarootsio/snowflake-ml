"""Utility functions to write data to Snowflake."""
from pathlib import Path
from typing import Any, Union

import pandas

from scripts.snowflake_utils import Session


def csv(
    filepath: Union[Path, str],
    table_name: str,
    session: Session,
    **read_csv_kwargs: Any,
) -> None:
    """Write CSV file to Snowflake."""
    return pd(
        df=pandas.read_csv(filepath, **read_csv_kwargs),
        table_name=table_name,
        session=session,
    )


def pd(df: pandas.DataFrame, table_name: str, session: Session) -> None:
    """Write pandas dataframe to Snowflake."""
    return (
        session.create_dataframe(data=df)
        .write.mode("overwrite")
        .save_as_table(table_name)
    )
