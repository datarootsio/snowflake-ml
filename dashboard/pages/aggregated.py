"""Streamlit app."""
import os
from datetime import date
from functools import reduce
from operator import and_
from typing import Dict, Sequence, Tuple

import pandas as pd
import streamlit as st
import toml

from dashboard.layout_utils import footer, header
from dashboard.snowflake_helpers import convert_df_types, init_connection, snowflake2pd

if os.getenv("ST_ENV") != "DEV":
    st.set_page_config(
        page_title="Reddit-Snowflake",
        page_icon=toml.load(".streamlit/settings.toml").get("app", {}).get("favicon"),
        layout="wide",
    )
    header()
    footer()


def _filter_options(
    df: pd.DataFrame, st_key: str, date_col: str = "CREATED_DATE"
) -> Tuple[Dict[str, Sequence[str]], Tuple[date, date]]:
    """Get filtering options based on elements sent to dashboard."""
    _df = df.copy(deep=True)
    # String filters
    unq_vals = {
        c: _df[c].unique() for c in _df.select_dtypes(["boolean", "string"]).columns
    }
    selected = {
        k: st.multiselect(k, options=v, default=v.tolist(), key=st_key + k)
        for k, v in unq_vals.items()
    }
    # Date filters
    _ds = _df[date_col]
    dates = st.slider(
        "Date",
        min_value=_ds.min(),
        max_value=_ds.max(),
        value=(_ds.min(), _ds.max()),
        key=st_key + date_col,
    )
    return selected, dates


session = init_connection()
df = convert_df_types(snowflake2pd("aggregated_posts", _session=session))

st.markdown(
    """
# Posts data
## Aggregated data

Choose which dimension to filter the data on:
"""
)

col1, col2 = st.columns(2)
with col1:
    selected_dims, dates = _filter_options(df, st_key="posts")
with col2:
    st.bar_chart(
        df.loc[
            reduce(
                and_,
                [df[col].isin(vals) for col, vals in selected_dims.items()],
                df["CREATED_DATE"].between(*dates),
            )
        ]
        .groupby("SUBREDDIT")[
            df.select_dtypes(include="number", exclude="boolean").columns
        ]
        .sum()
        .T.rename_axis(None, axis="columns"),
        height=600,
    )

st.markdown(
    """
## Timeseries data

Choose which dimension and KPI to visualize:
"""
)

col1, col2 = st.columns(2)
with col1:
    col = st.selectbox(
        "Dimension", options=df.select_dtypes(include=["boolean", "string"]).columns
    )
    sel = st.selectbox(
        "Dimension",
        options=df.select_dtypes(include="number", exclude="boolean").columns,
    )
with col2:
    _df = (
        df.set_index("CREATED_DATE")
        .loc[
            :,
            lambda _df: _df.select_dtypes(
                exclude=["boolean", "string"]
            ).columns.tolist()
            + [col],
        ]
        .groupby(["CREATED_DATE", col])
        .sum()
        .loc[:, sel]
        .unstack()
        .rename_axis(None, axis="columns")
    )
    st.area_chart(_df, height=200)

st.markdown(
    """
    ---
# Comments data
## Aggregated data

Choose which dimension to filter the data on:
"""
)

df = convert_df_types(snowflake2pd("aggregated_comments", _session=session))

col1, col2 = st.columns(2)
with col1:
    selected_dims, dates = _filter_options(df, st_key="comments")
with col2:
    st.bar_chart(
        df.loc[
            reduce(
                and_,
                [df[col].isin(vals) for col, vals in selected_dims.items()],
                df["CREATED_DATE"].between(*dates),
            )
        ]
        .groupby("SUBREDDIT")[
            df.select_dtypes(include="number", exclude="boolean").columns
        ]
        .sum()
        .T.rename_axis(None, axis="columns"),
        height=500,
    )

print(df.dtypes)
