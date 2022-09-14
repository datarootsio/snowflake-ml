"""Create evaluation plots (ROC and confusion matrix) and classification report."""
from itertools import chain
from pathlib import Path
from typing import List, Sequence, Tuple

import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.metrics import ConfusionMatrixDisplay, classification_report
from snowflake.snowpark.dataframe import DataFrame
from snowflake.snowpark.functions import call_udf, col, sproc
from snowflake.snowpark.session import Session as SnowparkSession
from snowflake.snowpark.types import DecimalType

from scripts import Session, _ungz
from snowflake_ml import __version__


def get_confusion_matrix(
    y_true: Sequence[float],
    y_pred: Sequence[float],
    img_path: Path = Path.cwd() / "cnf_mat.png",
) -> Path:
    """
    Build confusion matrix.

    :param y_true: True labels
    :param y_pred: Predicted labels
    :param img_path: Path (relative of absolute) in which to save the confusion matrix
    :return: Absolute path where file is written to
    """
    disp = ConfusionMatrixDisplay.from_predictions(y_true, y_pred)
    disp.plot()
    plt.savefig(img_path)
    return img_path.resolve()


def get_roc_curve(
    y_true: Sequence[int],
    y_pred: Sequence[float],
    display_name: str,
    img_path: Path = Path.cwd() / "roc.png",
) -> Path:
    """
    Build ROC curve.

    :param y_true: True labels
    :param y_pred: Predicted values (i.e.: confidence thresholds)
    :param display_name: ROC curve display name
    :param img_path: Path (relative of absolute) in which to save the ROC curve plot
    :return: Absolute path where file is written to
    """
    display = metrics.RocCurveDisplay.from_predictions(
        y_true=y_true, y_pred=y_pred, name=display_name
    )
    display.plot()
    plt.savefig(img_path)
    return img_path.resolve()


def get_classification_report(
    y_true: Sequence[int],
    y_pred: Sequence[int],
    target_names: Sequence[str],
    txt_path: Path = Path.cwd() / "report.txt",
) -> Path:
    """
    Build a classification report.

    :param y_true: Trye labels
    :param y_pred: Predicted labels
    :param target_names: Target names
    :param txt_path: Path (relative of absolute) in which to save the report
    :return: Absolute path where file is written to
    """
    txt_path.write_text(
        classification_report(y_true, y_pred, target_names=target_names),
        encoding="utf-8",
    )
    return txt_path.resolve()


def get_table(table: str, session: SnowparkSession) -> DataFrame:
    """Get table from Snowflake."""
    return (
        session.table(table)
        .select(
            col('"is_toxic"'),
            call_udf("ml_predict_dev", col('"comment_text"'))["prediction"]
            .cast(DecimalType())
            .as_("predicted"),
        )
        .limit(1000)
    )


def _build_plots(session: SnowparkSession, dir: Path) -> Tuple[Path, Path, Path]:
    """Build ROC curve, confusion matrix and classification report."""
    data = get_table(table="test", session=session)
    df_roc = data.to_pandas()
    roc_path = get_roc_curve(
        y_true=df_roc["is_toxic"],
        y_pred=df_roc["PREDICTED"],
        display_name="Profanity filter",
        img_path=dir / "roc.png",
    )

    df = data.select(
        col('"is_toxic"'), (col("predicted") > 0.5).as_("predicted")
    ).to_pandas()

    cnf_mat_path = get_confusion_matrix(
        y_true=df["is_toxic"], y_pred=df["PREDICTED"], img_path=dir / "cnf_mat.png"
    )
    report_path = get_classification_report(
        y_true=df["is_toxic"],
        y_pred=df["PREDICTED"],
        target_names=["True", "False"],
        txt_path=dir / "report.txt",
    )
    return roc_path, cnf_mat_path, report_path


def run_sproc(_session: Session) -> List[str]:
    """Create and run temporary Snowflake stored procedure."""

    @sproc(
        name="ml_eval",
        packages=["snowflake-snowpark-python", "scikit-learn", "matplotlib-base"],
        session=_session,
        replace=True,
        is_permanent=False,
    )
    def run(session: SnowparkSession) -> List[str]:
        """Run stored procedure - build plots and store them in a Snowflake stage."""
        tmp_dir = Path("/tmp")
        plots = _build_plots(session=session, dir=tmp_dir)
        stage_plots = [
            session.file.put(
                local_file_name=str(p),
                stage_location=f"@ml_eval/{__version__}",
                overwrite=True,
            )
            for p in plots
        ]
        return [plot.target for plot in chain.from_iterable(stage_plots)]

    return _session.call(sproc_name="ml_eval")


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
        staged_files = run_sproc(_session=_session)
        print("staged files:", staged_files)
        files = _session.file.get(
            stage_location=f"@ml_eval/{__version__}",
            target_directory=f"file://{Path.cwd().resolve()}",
        )
        local_files = _ungz(*[Path(f.file) for f in files])
        print("local files:", local_files)
