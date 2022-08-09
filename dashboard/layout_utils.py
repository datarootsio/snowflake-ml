"""
Header and footer layouts.

Based off of https://discuss.streamlit.io/t/st-footer/6447
"""
from typing import Union

import streamlit as st
import toml
from htbuilder import HtmlElement, a, div, img, p, styles
from htbuilder.units import percent, px


def image(src_as_string: str, **style: px) -> img:
    """Image HTML object."""
    return img(src=src_as_string, style=styles(**style))


def link(link: str, text: str, **style: px) -> a:
    """Links HTML object."""
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args: Union[str, HtmlElement]) -> None:
    """Specify the layout to be used in the footer (structured based on `*args`)."""
    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="lightgray",
        text_align="center",
        height="auto",
        opacity=0.9,
    )

    body = p()
    foot = div(style=style_div)(body)

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, (str, HtmlElement)):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def header() -> None:
    """Set header - remove hamburger menu."""
    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)


def footer() -> None:
    """Set footer."""
    myargs = [
        "Made with ❤️ using ",
        image(
            "https://aws1.discourse-cdn.com/business7/uploads/streamlit/original/"
            "2X/f/f0d0d26db1f2d99da8472951c60e5a1b782eb6fe.png",
            width=px(25),
            height=px(25),
        ),
        " by ",
        image(
            "https://dataroots.io/static/"
            "f4caa8d32099d3d9beae1a1d03d2893d/cd836/logo-rainbow-green.webp",
            height=px(20),
        ),
    ]
    layout(*myargs)


def set_layout(layout: str = "wide", **kwargs: str) -> None:
    """Set the page layout."""
    kwargs = {**toml.load(".streamlit/settings.toml").get("layout", {}), **kwargs}
    st.set_page_config(layout=layout, **kwargs)
    header()
    footer()
