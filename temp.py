import os
from dotenv import load_dotenv

from parsing_utilities import parse_video_metadata, parse_transcript

from invocations import new_gpt

from langchain_community.chat_models import ChatOpenAI

from langchain_community.callbacks import get_openai_callback
from langchain_openai import OpenAI

llm  = new_gpt()

from interrogate_transcript import one_shot_interrogate
from get_transcript import fetch_metadata_by_url

with get_openai_callback() as cb:
    metadata = fetch_metadata_by_url("https://www.youtube.com/watch?v=SPMpB9k89Zg")
    one_shot_interrogate(metadata, "summarize in five sentences", [["news","lebanon"]] )
    