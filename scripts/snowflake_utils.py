"""Snowflake utility functions - wrapper around creating a session with private keys."""
import os
from getpass import getpass
from pathlib import Path
from typing import Optional

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from snowflake.snowpark._internal.server_connection import ServerConnection
from snowflake.snowpark.session import Session as SnowparkSession
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
