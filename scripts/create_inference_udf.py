"""Create inference UDF using python Snowpark."""
import os
from datetime import datetime
from pathlib import Path

from snowflake.snowpark.functions import pandas_udf
from snowflake.snowpark.types import PandasSeries

from scripts.snowflake_utils import Session
from snowflake_ml import __version__


def main() -> None:
    """Create UDF with custom python code."""
    custom_libpath = sorted(Path("dist/").glob("*.whl"))[-1]
    if not custom_libpath.is_file():
        raise ValueError(f"Expected wheel file, got {custom_libpath}.")

    now = datetime.now().strftime("%Y%m%d-%H%M%S")

    with Session(
        database="snowflake_ml",
        account="vw42238",
        user="murilo",
        warehouse='"reddit_xs"',
        role="accountadmin",
        region="eu-central-1",
        schema="reddit",
    ):

        @pandas_udf(
            name=f"ml_predict_{os.getenv('ENVIRONMENT', 'DEV')}",
            is_permanent=True,
            stage_location=f"@py_udfs/{__version__}/{now}",
            replace=True,
            imports=[str(custom_libpath)],
            packages=["snowflake-snowpark-python==0.8.0"],
        )
        def run(ds: PandasSeries[str]) -> PandasSeries[dict]:
            import os
            import sys

            import_dir = sys._xoptions["snowflake_import_directory"]
            sys.path.append(os.path.join(import_dir, custom_libpath.name))

            from snowflake_ml import __version__
            from snowflake_ml.model import predict

            return ds.apply(
                lambda s: {"prediction": predict(s), "model_version": __version__}
            )


if __name__ == "__main__":
    main()
