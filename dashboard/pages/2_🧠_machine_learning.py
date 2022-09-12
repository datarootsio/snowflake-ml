"""Page with results from machine learning models in Snowflake."""
import streamlit as st

from dashboard.layout_utils import set_layout
from dashboard.snowflake_helpers import convert_df_types, init_connection, snowflake2pd

# Main app
set_layout()
session = init_connection()

st.title("Content moderation")
st.header("Posts")
st.dataframe(
    snowflake2pd("ml_posts_toxic", _session=session)
    .pipe(convert_df_types, dtype_mapping={"IS_TOXIC": "float64"})
    .set_index("RECORD_ID")
    .sort_values(by=["IS_TOXIC", "CREATED_TIMESTAMP"], ascending=[False, False])
)
