"""Helper functions to interact with Snowflake data."""
from typing import Dict, Optional

import pandas as pd
import streamlit as st

from scripts.snowflake_utils import Session


@st.experimental_singleton
def init_connection() -> Session:
    """Initiatize Snowflake connection."""
    return Session(**st.secrets["snowflake"])


@st.experimental_memo(ttl=60 * 10)
def snowflake2pd(table: str, _session: Session) -> pd.DataFrame:
    """Get a Snowflake table and return it as a pandas dataframe."""
    return _session.table(table).to_pandas()


def convert_df_types(
    df: pd.DataFrame, dtype_mapping: Optional[Dict[str, str]] = None
) -> pd.DataFrame:
    """Convert dataframe types."""
    # Manually map types that are not converted correctly
    dtype_mapping = dtype_mapping or {}
    return df.copy(deep=True).convert_dtypes().astype(dtype_mapping)
