from api_key_manager import set_api_key, verify_openai_api_key
import os
from dotenv import load_dotenv
from pathlib import Path






def initiate_set_api_key():
    info = '''

this program uses api key stored in system env to avoid accidental sharing of the private key

get your key on openai api key page: https://platform.openai.com/api-keys

'''
    ENV_FILE = Path('.') / '.env'
    load_dotenv(dotenv_path=ENV_FILE)
    print(info)
    should_continue = True
    while(should_continue):
        user_input = input("input a valid openai api key\n>")
        set_api_key(user_input)
        if verify_openai_api_key(os.getenv("OPENAI_API_KEY_for_yt_interrogator")):
            should_continue=False


import shelve

with shelve.open("settings") as settings:
    print(f"Current language: {settings.get('language', 'en')}")
    settings["language"] = "fr"        

def set_user_language(new_language):
    with shelve.open("settings") as settings:  
        settings["language"] = new_language


def get_user_language():
    with shelve.open("settings") as settings:  
        return settings['language']

def initiate_set_output_lanugage():
    print(f"current output language is {get_user_language()}")
    user_input = input("input your preffered output language. to cancel input 'cancel\n>")
    match user_input:
        case "cancel":
            pass
        case _:
            set_user_language(user_input)
            print(f"\noutput language is now set to {get_user_language()}")
    print("to be implemented")
def initiate_set_output_folder_path():
    print("to be implemented")

