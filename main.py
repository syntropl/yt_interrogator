from pip_setup import pip_update_missing_dependencies
from settings import initiate_set_api_key, iniate_set_output_lanugage, initiate_set_output_folder_path
from api_key_manager import print_api_key
from interrogate_transcript import interrogate_transcript

should_close_program = False

settings_commands = "SETTINGS \n\nset_api_key, language"
helpstring = "\n\nHELP\n\ncostam, costam, help"



ascii_intro = '''

▗▖  ▗▖▗▄▖ ▗▖ ▗▖▗▄▄▄▖▗▖ ▗▖▗▄▄▖ ▗▄▄▄▖                        
 ▝▚▞▘▐▌ ▐▌▐▌ ▐▌  █  ▐▌ ▐▌▐▌ ▐▌▐▌                           
  ▐▌ ▐▌ ▐▌▐▌ ▐▌  █  ▐▌ ▐▌▐▛▀▚▖▐▛▀▀▘                        
  ▐▌ ▝▚▄▞▘▝▚▄▞▘  █  ▝▚▄▞▘▐▙▄▞▘▐▙▄▄▖                        
                                                           
                                                           
                                                           
▗▄▄▄▖▗▄▄▖  ▗▄▖ ▗▖  ▗▖ ▗▄▄▖ ▗▄▄▖▗▄▄▖ ▗▄▄▄▖▗▄▄▖▗▄▄▄▖         
  █  ▐▌ ▐▌▐▌ ▐▌▐▛▚▖▐▌▐▌   ▐▌   ▐▌ ▐▌  █  ▐▌ ▐▌ █           
  █  ▐▛▀▚▖▐▛▀▜▌▐▌ ▝▜▌ ▝▀▚▖▐▌   ▐▛▀▚▖  █  ▐▛▀▘  █           
  █  ▐▌ ▐▌▐▌ ▐▌▐▌  ▐▌▗▄▄▞▘▝▚▄▄▖▐▌ ▐▌▗▄█▄▖▐▌    █           
                                                           
                                                           
                                                           
▗▄▄▄▖▗▖  ▗▖▗▄▄▄▖▗▄▄▄▖▗▄▄▖ ▗▄▄▖  ▗▄▖  ▗▄▄▖ ▗▄▖▗▄▄▄▖▗▄▖ ▗▄▄▖ 
  █  ▐▛▚▖▐▌  █  ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌▐▌   ▐▌ ▐▌ █ ▐▌ ▐▌▐▌ ▐▌
  █  ▐▌ ▝▜▌  █  ▐▛▀▀▘▐▛▀▚▖▐▛▀▚▖▐▌ ▐▌▐▌▝▜▌▐▛▀▜▌ █ ▐▌ ▐▌▐▛▀▚▖
▗▄█▄▖▐▌  ▐▌  █  ▐▙▄▄▖▐▌ ▐▌▐▌ ▐▌▝▚▄▞▘▝▚▄▞▘▐▌ ▐▌ █ ▝▚▄▞▘▐▌ ▐▌
                                                           
                                                           
                                                 
                                                   '''


helpstring = '''
type in command to enter special modes:

set_api_key : to set new api key                             
print_api_key : to print api key
language : to set llm output language                    (TODO)
folder: to change output folder path for saved sessions   (TODO)

quit: to exit program

'''


def start_sequence():
    print(ascii_intro)
    print("for commands type 'help'\n\n")
    
def main_sequence():
    #if api key not set (or wrong)
    # make user update it

    while(should_close_program==False):
        user_input = input("\n\ninput command or youtube video url:\n>")
        match user_input:
            case "help":
                print(helpstring)
            case "set_api_key":
                initiate_set_api_key()
            case "print_api_key":
                print_api_key()
            case "lanugage":
                iniate_set_output_lanugage()
            case "folder":
                initiate_set_output_folder_path()
            case "quit":
                break
            case _:
                try:
                    interrogate_transcript(user_input)
                except Exception as e:
                    pass


        


    
    

if __name__ == "__main__":
    start_sequence()
    main_sequence()
    print("\n\n\n END OF PROGRAM\n\n\n")
    
# INTERPRET_COMMAND
# PRINT_MENU# PRINT_LONG_HELPok
