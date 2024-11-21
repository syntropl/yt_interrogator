import os
from pathlib import Path

from dotenv import load_dotenv, set_key
from langchain_community.llms import OpenAI 


from parsing_utilities import section_print

# Define the path to the .env file
ENV_FILE = Path('.') / '.env'

# Load environment variables from the .env file
load_dotenv(dotenv_path=ENV_FILE, override=True)


        

    
def verify_openai_api_key(key: str) -> bool:
    """
    Verifies the provided OpenAI API key by making a test API call.
    Returns True if the key is valid, False otherwise.

    Args:
        key (str): The OpenAI API key to verify.

    Returns:
        bool: True if the API key is valid, False otherwise.
    """

    try:
        load_dotenv(dotenv_path=ENV_FILE, override=True)
        
        llm = OpenAI(openai_api_key=key)
        test_prompt = '''"Respond only with a word exactly 11 characters long. interlinked."'''
        response_text = llm.invoke(test_prompt).strip().strip('.')

        section_print(f"\n\nTEST PROMPT:\n{test_prompt}\n"+f'''\nRESPONSE: \n"{response_text}"''' ,"verifying api key...\n")
     

        if len(response_text) == 11:
            print("openai api connection verified")
            return True
        else:
            print(f"\n\nTEST FAILED:\nResponse length is {len(response_text)} instead of 11.\n")
            return False
    except Exception as e:
        print(f"Error during API call: {e}")
        return False
    

def set_api_key(key: str):
    """
    Sets the OpenAI API key after verification and stores it in the .env file.

    Args:
        key (str): The OpenAI API key to set.
    """
    try:

        # Store the API key in the .env file
        print('''\nsetting api key as environment variable''')
        set_key(str(ENV_FILE), "OPENAI_API_KEY_for_yt_interrogator", key)
        print('''reading api key from env''')
        load_dotenv(dotenv_path=ENV_FILE, override=True)

        if (os.getenv("OPENAI_API_KEY_for_yt_interrogator")==key):
            
            print("\nAPI KEY IS SET")
        else:
            print('\n\nERROR: key NOT SAVED to env')

    except Exception as e:
        print(f"\n\nERROR: Failed to set API key. {str(e)}")

def print_api_key(masked=False):
    load_dotenv(dotenv_path=ENV_FILE, override=True)
    key = os.getenv("OPENAI_API_KEY_for_yt_interrogator")
    if key is None:
        print("API key not found in environment variables.")
    
    if masked:
        masked_key = f"{key[:10]}{'*' * (len(key) - 20)}{key[-10:]}"
        print(masked_key)
    else:
        print(key)

def ensure_api_key_is_verified() -> bool:
    """
    Retrieves the API key from the .env file and verifies its validity.
    Returns True if valid, False otherwise.

    Returns:
        bool: True if the API key from .env is valid, False otherwise.
    """
    load_dotenv(dotenv_path=ENV_FILE, override=True)
    try:
        api_key = os.getenv("OPENAI_API_KEY_for_yt_interrogator")
        if not api_key:
            print("API key is not set in .env file.")
            return False
        if verify_openai_api_key(api_key):
            return True
        else:
            print("ERROR: API key from .env is invalid.")
            return False
    except Exception as e:
        print(f"ERROR: Failed to verify API key from environment. {str(e)}")
        return False

def mask_api_key(api_key: str) -> str:
    """
    Masks the API key for secure display.
    Shows only the last 4 characters.

    Args:
        api_key (str): The API key to mask.

    Returns:
        str: The masked API key.
    """
    if len(api_key) <= 4:
        return "*" * len(api_key)
    else:
        return "*" * (len(api_key) - 4) + api_key[-4:]



if __name__ == "__main__":
        print_api_key()
        user_key = input("input your openai api key")
        set_api_key(user_key)

