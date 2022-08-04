"""Helper functions to interact with Snowflake data."""
import pandas as pd
import streamlit as st

from snowflake_ml.snowflake_utils import SessionML


@st.experimental_singleton
def init_connection() -> SessionML:
    """Initiatize Snowflake connection."""
    return SessionML(**st.secrets["snowflake"])


@st.experimental_memo(ttl=60 * 10)
def snowflake2pd(table: str, _session: SessionML) -> pd.DataFrame:
    """Get a Snowflake table and return it as a pandas dataframe."""
    return _session.table(table).to_pandas()


def convert_df_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convert dataframe types."""
    # Manually map types that are not converted correctly
    d_types = {
        "AVERAGE_TITLE_LENGTH": "float64",
        "AVERAGE_BODY_LENGTH": "float64",
        "CONTROVERSIALITY": "boolean",
    }
    return (
        df.copy(deep=True)
        .astype({k: v for k, v in d_types.items() if k in df.columns})
        .convert_dtypes()
    )
