"""Utility and helper functions - Session, CSVs and GZips."""
import gzip
import os
import shutil
from getpass import getpass
from pathlib import Path
from typing import Any, List, Optional, Union

import pandas
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from snowflake.snowpark import Session as SnowparkSession
from snowflake.snowpark._internal.server_connection import ServerConnection
from snowflake.snowpark.session import _add_session


class Session(SnowparkSession):
    """Wrapper to use private keys to connect to Snowflake server."""

    def __init__(
        self,
        *,
        private_key_file: Optional[str] = None,
        private_key_passphrase: Optional[str] = None,
        **session_builder_kwargs: str,
    ):
        """
        Initialize session directly (without session builder).

        Expect keyword arguments only. Accepts arguments normally passed to
         `Session.builder.configs`, `private_key_filepath` and `private_key_passphrase`
         arguments. The `private_key_filepath` and `private_key_passphrase` arguments
         may also be inferred from environment variables (SNOWSQL_PRIVATE_KEY_FILEPATH
         and SNOWSQL_PRIVATE_KEY_PASSPHRASE, respectively). See
         https://docs.snowflake.com/en/user-guide/python-connector-api.html for more
         information.
        """
        private_key_file = private_key_file or os.getenv("SNOWSQL_PRIVATE_KEY_FILEPATH")
        if private_key_file is not None:
            private_key_filepath: Path = Path(private_key_file)
            if not private_key_filepath.is_file():
                raise ValueError(f"File in {private_key_filepath} does not exist.")
            private_key_passphrase = (
                private_key_passphrase
                or os.environ.get("SNOWSQL_PRIVATE_KEY_PASSPHRASE")
                or getpass("Snowflake key passphrase:")
            )

            with private_key_filepath.open("rb") as key:
                private_key = serialization.load_pem_private_key(
                    key.read(),
                    private_key_passphrase.encode(),
                    backend=default_backend(),
                )
            private_key_contents = private_key.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
            session_builder_kwargs = {
                **session_builder_kwargs,
                "private_key": private_key_contents,
            }
        super(Session, self).__init__(conn=ServerConnection(session_builder_kwargs))
        _add_session(self)


def _ungz(*files: Path) -> List[Path]:
    """Decompress `.gz` files."""
    for file in files:
        with gzip.open(file, "rb") as f_in:
            with open(file.with_suffix(""), "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(file)
    return [file.with_suffix("") for file in files]


def write_csv(
    filepath: Union[Path, str],
    table_name: str,
    session: Session,
    **read_csv_kwargs: Any,
) -> None:
    """Write CSV file to Snowflake."""
    return write_pd(
        df=pandas.read_csv(filepath, **read_csv_kwargs),
        table_name=table_name,
        session=session,
    )


def write_pd(df: pandas.DataFrame, table_name: str, session: Session) -> None:
    """Write pandas dataframe to Snowflake."""
    return (
        session.create_dataframe(data=df)
        .write.mode("overwrite")
        .save_as_table(table_name)
    )
