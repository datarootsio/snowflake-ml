"""Scripts to create materialized views (not possible via Terraform)."""
from pathlib import Path

from scripts.snowflake_utils import Session

PATH_SQL = Path(__file__).parents[1] / "sql"


def _create_matview_from_file(file: Path, session: Session) -> None:
    """Small convenience function to create materialized views from files."""
    table = session.sql(
        f"create or replace materialized"
        f" view snowflake_ml.reddit.{file.stem} as\n" + file.read_text()
    )
    print(table.collect())


if __name__ == "__main__":
    # Using `private_key_filepath` and `private_key_passphrase` from env vars
    with Session(
        database="snowflake_ml",
        account="vw42238",
        user="murilo",
        warehouse='"reddit_xs"',
        role="accountadmin",
        region="eu-central-1",
        schema="reddit",
    ) as session:
        for file in ["flattened_posts.sql", "flattened_comments.sql"]:
            _create_matview_from_file(file=PATH_SQL / file, session=session)
