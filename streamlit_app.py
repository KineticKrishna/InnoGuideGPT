from collections import namedtuple
import altair as alt

import os, time
import pandas as pd
import math
import glob

from io import StringIO
import base64
import openai

# -------------IMPORTING CORE FUNCTIONALITIES OF THE SpeeKAR_BOT-------------
from innoguideGPT import (
    speechtotext,
    texttospeech_raw,
    extract_commands_from_text
)


# -------------------AUDIO FUNCTIONALITY-------------------------
from mutagen.wave import WAVE

# --------------------HTML BUILDER AND FUNCTIONALITIES-----------------------------------#
from htbuilder import (
    HtmlElement,
    div,
    ul,
    li,
    br,
    hr,
    a,
    p,
    img,
    styles,
    classes,
    fonts,
)
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb

import streamlit as st
from audiorecorder import audiorecorder


from PIL import Image


# ------------------DEFAULTS--------------------#
LANGUAGE = "en"

SECRET_API_KEY = os.environ["SECRET_API_KEY"]
openai.api_key = SECRET_API_KEY




# -----------------------HELPER FUNCTIONS--------------------------#
def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):
    style = """
    <style>
      # MainMenu {visibility: display;}
      footer {visibility: display;}
     .stApp { bottom: 105px; }
    </style>
    """
    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 50, 0, 50),
        width=percent(100),
        color="blue",
        text_align="left",
        height="auto",
        opacity=1,
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(1.5),
    )

    body = p()
    foot = div(style=style_div)(hr(style=style_hr), body)

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


# -------------------------------FUNCTIONS FOR KAR BASED RESPONSE GENERATION-------------#
def process_query(speech_input, email, passwd):
    question0 = speech_input
    question = speech_input
    query = speechtotext(speech_input)

    # ans, context, keys = chatbot_slim(query, text_split)
    return query

# -------------------------------------------------------------------------#
# --------------------------GUI CONFIGS------------------------------------#
# -------------------------------------------------------------------------#
# App title
st.set_page_config(page_title="InnoGuideGPT")
st.header("InnoGuideGPT: Making navigation robots humanlike!")
st.title("Howdy! I am at your service! Where do you want to go?")
audio = audiorecorder("Click to record", "Click to stop recording")


# Hugging Face Credentials
with st.sidebar:
    st.title("InnoGuideGPT")
    st.success(
        "Access to this Gen-AI Powered Chatbot is provided by  [Rahul](https://www.linkedin.com/in/rahul-sundar-311a6977/)!!",
        icon="✅",
    )
    hf_email = "rahul.sundar95@gmail.com"
    hf_pass = "PASS"
    st.markdown(
        "📖 This app is hosted by Rahul Sundar [website](https://github.com/RahulSundar)!"
    )
    image = Image.open("innoguideibotcfiiitmlogos/innoGuide_logo.jpg")
    st.image(
        image,
        caption=None,
        width=None,
        use_column_width=None,
        clamp=False,
        channels="RGB",
        output_format="auto",
    )


# ------------------------------------------------------------------------------#
# -------------------------QUERY AUDIO INPUT - RETURNING TEXT QUERY-------------#
# ------------------------------------------------------------------------------#
if not audio.empty():
    # To play audio in frontend:
    st.audio(audio.export().read())

    # To save audio to a file, use pydub export method:
    audio.export("query.wav", format="wav")

    # To get audio properties, use pydub AudioSegment properties:
    st.write(f"Duration: {audio.duration_seconds} seconds")

    # st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")
    querywav = WAVE("query.wav")
    if querywav.info.length > 0:
        query = process_query("query.wav", hf_email, hf_pass)
        st.markdown(
            """
            <style>
            .big-font {
                font-size:20px !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # st.markdown("Your question in text ::")
        st.markdown(
            '<p class="big-font"> Your question in text : </p>', unsafe_allow_html=True
        )
        # if "messages" not in st.session_state.keys():
        #    st.session_state.messages = [{"role": "assistant", "content": query}]
        st.write(query)

    json = str(extract_commands_from_text(query))
    st.markdown(
        """
            <style>
            .big-font {
                font-size:20px !important;
            }
            </style>
            """,
        unsafe_allow_html=True,
    )

    # st.markdown("Your question in text ::")
    
    st.markdown(
        '<p class="big-font"> Play your answer below! </p>', unsafe_allow_html=True
    )
    st.write(json)
    # -----------text to speech--------------------------#
    texttospeech_raw("The JSON object extracted from your command is as above", language="en")
    audio_file = open("answer.wav", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/wav")
    mymidia_placeholder = st.empty()
    with open("answer.wav", "rb") as audio_file:
        #st.audio(audio_bytes, format="audio/wav")
        audio_bytes = audio_file.read()
        b64 = base64.b64encode(audio_bytes).decode()
        md = f"""
             <audio controls autoplay="true">
             <source src="data:audio/wav;base64,{b64}" type="audio/wav">
             </audio>
             """
        mymidia_placeholder.empty()
        time.sleep(1)
        mymidia_placeholder.markdown(md, unsafe_allow_html=True)

myargs = [
    "Engineered in India",
    "" " with ❤️ by ",
    link("https://www.linkedin.com/in/rahul-sundar-311a6977/", "@Rahul"),
    br(),
    link("https://github.com/RahulSundar", "InnoguideGPT"),
]


def footer():
    myargs = [
        "Engineered in India",
        "" " with ❤️ by ",
        link("https://www.linkedin.com/in/rahul-sundar-311a6977/", "@Rahul"),
        link("", "@Tankala Satyasai"),
        br(),
        ", and",
        link("", "@Sri Krishna")
    ]
    layout(*myargs)


footer()
