"""Page with more information about the project."""
from pathlib import Path

import streamlit as st

from dashboard.layout_utils import set_layout

set_layout()

README = Path(__file__).parents[2] / "README.md"

st.markdown(README.read_text(), unsafe_allow_html=True)

st.markdown(
    """
# Links:

- [dataroots](https://dataroots.io/)
- [Github repo](https://github.com/datarootsio/snowflake-ml)
- [LinkedIn](https://www.linkedin.com/company/dataroots/mycompany/)
- [Instagram](https://www.instagram.com/lifeatdataroots/)
"""
)
