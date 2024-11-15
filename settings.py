from api_key_manager import set_api_key

def initiate_set_api_key():
    info = '''

this program uses api key stored in system env to avoid accidental sharing of the private key

get your key on openai api key page: https://platform.openai.com/api-keys

'''
    print(info)
    should_continue = True
    while(should_continue):
        user_input = input("input a valid openai api key\n>")
        set_api_key(user_input)
        if verify_openai_api_key(os.getenv("OPENAI_API_KEY_for_yt_interrogator")):
            should_continue=False


        



def iniate_set_output_lanugage():
    print("to be implemented")
def initiate_set_output_folder_path():
    print("to be implemented")

