"""Langing page on application."""
import streamlit as st

from dashboard.layout_utils import set_layout

set_layout(layout="centered")

st.balloons()
st.title("Hi there! 👋")

st.markdown(
    """
<p align="center">
  <img alt="logo" src="https://media.giphy.com/media/lrbN8OxA0tNx3K4ccF/giphy.gif"/>
</p>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
Thanks for the interest in this project!

Here, we'll explore using Snowflake as a full end-to-end solution to deploy machine
learning models. What's more, we'll be using Apache Kafka and Confluent to stream data
into Snowflake, which will process the data and show the aggregated data in Streamlit!

But first, let set the scene!

## Story time! 📖

You answer on the second ring. It's the CEO of your company, Johannes. Congratulations
is in order. You're the new Chief Data Officer (CDO)! The bad news is: we have
absolutely no idea on how our data looks like. Luckily, you have a good idea on where
to start...
"""
)
