"""Helper functions to interact with Snowflake data."""
from typing import Dict, Optional

import pandas as pd
import streamlit as st

from snowflake_ml import SessionML


@st.experimental_singleton
def init_connection() -> SessionML:
    """Initiatize Snowflake connection."""
    return SessionML(**st.secrets["snowflake"])


@st.experimental_memo(ttl=60 * 10)
def snowflake2pd(table: str, _session: SessionML) -> pd.DataFrame:
    """Get a Snowflake table and return it as a pandas dataframe."""
    return _session.table(table).to_pandas()


def convert_df_types(
    df: pd.DataFrame, dtype_mapping: Optional[Dict[str, str]] = None
) -> pd.DataFrame:
    """Convert dataframe types."""
    # Manually map types that are not converted correctly
    dtype_mapping = dtype_mapping or {}
    return df.copy(deep=True).astype(dtype_mapping).convert_dtypes()
