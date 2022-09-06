"""Create inference UDF using python Snowpark."""
import os
from pathlib import Path

from snowflake.snowpark.functions import udf

from scripts.snowflake_utils import Session
from snowflake_ml import __version__


def main() -> None:
    """Create UDF with custom python code."""
    custom_libpath = sorted(Path("dist/").glob("*.whl"))[-1]
    if not custom_libpath.is_file():
        raise ValueError(f"Expected wheel file, got {custom_libpath}.")

    with Session(
        database="snowflake_ml",
        account="vw42238",
        user="murilo",
        warehouse='"reddit_xs"',
        role="accountadmin",
        region="eu-central-1",
        schema="reddit",
    ):

        @udf(
            name=f"ml_predict_{os.getenv('ENVIRONMENT', 'DEV')}",
            is_permanent=True,
            stage_location=f"@py_udfs/{__version__}",
            replace=True,
            imports=[str(custom_libpath)],
            packages=["snowflake-snowpark-python"],
        )
        def run(s: str) -> dict:
            import os
            import sys

            import_dir = sys._xoptions["snowflake_import_directory"]
            sys.path.append(os.path.join(import_dir, custom_libpath.name))

            from snowflake_ml import __version__
            from snowflake_ml.model import predict

            return {"prediction": predict(s), "model_version": __version__}


if __name__ == "__main__":
    main()
