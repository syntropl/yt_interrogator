
def initiate_set_api_key():
    print("to be implemented")
    info = '''
this string should accurately describe what will happen and adress security concerns
where will the key be stored
'''
    print(info)
    should_continue = True
    while(should_continue):
        user_input = input("input valid openai api key")
        test_api_key(user_input)


def test_api_key(key):
    max_attempts = 2
    last_response = ""
    for attempt in range(0,max_attempts):
        test_prompt = '''respond with a word exactly 12 characters long. interlinnked.'''
        print("initiating api key test:\n")
        print(f"test_prompt = '{test_prompt}'")
        last_response = llm.invoke(test_prompt)
        print(response.content)
        if(len(response.content)==12):
            return True
    print(last_response)
    return False
        



def iniate_set_output_lanugage():
    print("to be implemented")
def initiate_set_output_folder_path():
    print("to be implemented")

