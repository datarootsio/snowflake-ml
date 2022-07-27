"""Snowflake utility functions - wrapper around creating a session with private keys."""
import os
from getpass import getpass
from pathlib import Path
from typing import Optional

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from snowflake.snowpark._internal.server_connection import ServerConnection
from snowflake.snowpark.session import Session, _add_session


class SessionML(Session):
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
            private_key_passphrase = None  # overwrite secret values
            session_builder_kwargs = {
                **session_builder_kwargs,
                "private_key": private_key_contents,
            }
        super(SessionML, self).__init__(conn=ServerConnection(session_builder_kwargs))
        _add_session(self)


if __name__ == "__main__":
    PATH_SQL = Path(__file__).parents[1] / "sql"

    # Using `private_key_filepath` and `private_key_passphrase` from env vars
    with SessionML(
        database="snowflake_ml",
        account="vw42238",
        user="murilo",
        warehouse='"reddit_xs"',
        role="accountadmin",
        region="eu-central-1",
        schema="reddit",
    ) as session:

        df = session.sql(
            "create or replace materialized"
            " view snowflake_ml.reddit.flattened_comments as\n"
            + (PATH_SQL / "flattened_comments.sql").read_text()
        )

        print(df.collect())
