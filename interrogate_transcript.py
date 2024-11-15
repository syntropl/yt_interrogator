import os
from dotenv import load_dotenv

from langchain_community.chat_models import ChatOpenAI


load_dotenv()
oai_key = os.getenv("OPENAI_API_KEY_for_yt_interrogator")
model_name="gpt-4o"

def new_gpt():
    return ChatOpenAI(openai_api_key=oai_key, model=model_name)
print("\n\n")
resp = new_gpt().invoke("convince me to go to sleep in less than 9 words").content

print(f"\n\n{resp}")
print()
