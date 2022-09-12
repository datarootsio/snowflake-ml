"""Page with results from machine learning models in Snowflake."""
import streamlit as st

from dashboard.layout_utils import set_layout
from dashboard.snowflake_helpers import convert_df_types, init_connection

# Main app
set_layout()
session = init_connection()

st.title("Content moderation")
st.header("Posts")
st.dataframe(
    session.table("ml_posts_toxic")
    .to_pandas()
    .pipe(convert_df_types, dtype_mapping={"IS_TOXIC": "float64"})
    .set_index("RECORD_ID")
    .sort_values(by=["IS_TOXIC", "CREATED_TIMESTAMP"], ascending=[False, False])
)
