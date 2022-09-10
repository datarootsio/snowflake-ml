"""Streamlit app."""
from datetime import date
from functools import reduce
from operator import and_
from typing import Any, Dict, Sequence, Tuple

import pandas as pd
import streamlit as st

from dashboard.layout_utils import set_layout
from dashboard.snowflake_helpers import convert_df_types, init_connection, snowflake2pd
from scripts.snowflake_utils import Session


def _filter_options(
    df: pd.DataFrame,
    dim_cols: Sequence[str],
    *,
    st_key: str,
    date_col: str = "CREATED_DATE",
) -> Tuple[Dict[str, Sequence[str]], Tuple[date, date]]:
    """Get filtering options based on elements sent to dashboard."""
    # String filters
    unq_vals = {c: df[c].unique() for c in dim_cols}
    selected = {
        k: st.multiselect(k, options=v, default=v.tolist(), key=st_key + k)
        for k, v in unq_vals.items()
    }
    # Date filters
    _ds = df[date_col]
    dates = st.slider(
        "Date",
        min_value=_ds.min(),
        max_value=_ds.max(),
        value=(_ds.min(), _ds.max()),
        key=f"{st_key}_{date_col}",
    )
    return selected, dates


def _aggregated(df: pd.DataFrame, plot_height: int = 600, **filter_kwargs: Any) -> None:
    """Plot aggregated figures."""
    st.markdown(
        """
    ## Aggregated data

    Choose which dimension to filter the data on:
    """
    )
    agg_cols = df.select_dtypes(include="number", exclude=["boolean", "float"]).columns
    avg_cols = df.select_dtypes(include="float").columns
    dim_cols = df.select_dtypes(include=["boolean", "string"]).columns

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_dims, dates = _filter_options(df, dim_cols=dim_cols, **filter_kwargs)
    with col2:
        st.bar_chart(
            df.loc[
                reduce(
                    and_,
                    [df[col].isin(vals) for col, vals in selected_dims.items()],
                    df["CREATED_DATE"].between(*dates),
                )
            ]
            .groupby("SUBREDDIT")[agg_cols]
            .sum()
            .T.rename_axis(None, axis="columns"),
            height=plot_height,
        )
    with col3:
        st.bar_chart(
            df.loc[
                reduce(
                    and_,
                    [df[col].isin(vals) for col, vals in selected_dims.items()],
                    df["CREATED_DATE"].between(*dates),
                ),
                avg_cols,
            ]
            .mean()
            .to_frame("All subreddits"),
            height=plot_height,
        )


def _timeseries(df: pd.DataFrame, st_key: str) -> None:
    """Plot timeseries figures."""
    st.markdown(
        """
    ## Timeseries data

    Choose which dimension and KPI to visualize:
    """
    )
    agg_cols = df.select_dtypes(include="number", exclude=["boolean", "float"]).columns
    avg_cols = df.select_dtypes(include="float").columns
    dim_cols = df.select_dtypes(include=["boolean", "string"]).columns

    col1, col2 = st.columns(2)
    with col1:
        col = st.selectbox("Dimension", options=dim_cols, key=f"{st_key}_dim")
        sel = st.selectbox("Metric", options=agg_cols, key=f"{st_key}_metric")

        st.area_chart(
            df[["CREATED_DATE", sel, col]]
            .groupby(["CREATED_DATE", col])
            .sum()
            .loc[:, sel]
            .unstack()
            .rename_axis(None, axis="columns"),
            height=200,
        )

    with col2:

        _df = (
            df[["CREATED_DATE", "NUMBER_OF_RECORDS", *avg_cols]]
            .groupby(["CREATED_DATE"])
            .sum()
            .assign(
                AVERAGE_TITLE_LENGTH=lambda _df: _df["SUM_TITLE_LENGTH"]
                / _df["NUMBER_OF_RECORDS"]
            )
            .assign(
                AVERAGE_BODY_LENGTH=lambda _df: _df["SUM_BODY_LENGTH"]
                / _df["NUMBER_OF_RECORDS"]
            )
            .loc[:, ["AVERAGE_TITLE_LENGTH", "AVERAGE_BODY_LENGTH"]]
        )
        st.line_chart(
            _df,
            height=400,
        )


def _plot_summary(
    title: str, table_name: str, session: Session, st_key: str, **dtypes_mapping: str
) -> None:
    """Plot summaries for Snowflake table."""
    st.title(title)
    df = snowflake2pd(table_name, _session=session)
    df = convert_df_types(df, dtype_mapping=dtypes_mapping)
    _aggregated(df, st_key=st_key)
    _timeseries(df, st_key=st_key)


# Main app
set_layout()
session = init_connection()

_plot_summary(
    title="Posts data",
    table_name="aggregated_posts",
    session=session,
    st_key="posts",
    SUM_TITLE_LENGTH="float64",
    SUM_BODY_LENGTH="float64",
)

_plot_summary(
    title="Comments data",
    table_name="aggregated_comments",
    session=session,
    st_key="comments",
    SUM_TITLE_LENGTH="float64",
    SUM_BODY_LENGTH="float64",
    CONTROVERSIALITY="boolean",
)
