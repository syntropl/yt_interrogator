from settings import initiate_set_api_key, initiate_set_output_lanugage, initiate_set_output_folder_path
from api_key_manager import ensure_api_key_is_verified, print_api_key
from interrogate_transcript import interrogate_loop, save_interrogation
from parsing_utilities import is_url, is_youtube_url
from langchain_community.callbacks import get_openai_callback


should_close_program = False

settings_commands = "SETTINGS \n\nset_api_key, language"
helpstring = "\n\nHELP\n\ncostam, costam, help"



ascii_intro = '''
██╗   ██╗ ██████╗ ██╗   ██╗████████╗██╗   ██╗██████╗ ███████╗                                     
╚██╗ ██╔╝██╔═══██╗██║   ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝                                     
 ╚████╔╝ ██║   ██║██║   ██║   ██║   ██║   ██║██████╔╝█████╗                                       
  ╚██╔╝  ██║   ██║██║   ██║   ██║   ██║   ██║██╔══██╗██╔══╝                                       
   ██║   ╚██████╔╝╚██████╔╝   ██║   ╚██████╔╝██████╔╝███████╗                                     
   ╚═╝    ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝ ╚═════╝ ╚══════╝                                     
                                                                                                  
████████╗██████╗  █████╗ ███╗   ██╗███████╗ ██████╗██████╗ ██╗██████╗ ████████╗                   
╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝                   
   ██║   ██████╔╝███████║██╔██╗ ██║███████╗██║     ██████╔╝██║██████╔╝   ██║                      
   ██║   ██╔══██╗██╔══██║██║╚██╗██║╚════██║██║     ██╔══██╗██║██╔═══╝    ██║                      
   ██║   ██║  ██║██║  ██║██║ ╚████║███████║╚██████╗██║  ██║██║██║        ██║                      
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝                      
                                                                                                  
██╗███╗   ██╗████████╗███████╗██████╗ ██████╗  ██████╗  ██████╗  █████╗ ████████╗ ██████╗ ██████╗ 
██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔════╝ ██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
██║██╔██╗ ██║   ██║   █████╗  ██████╔╝██████╔╝██║   ██║██║  ███╗███████║   ██║   ██║   ██║██████╔╝
██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗██╔══██╗██║   ██║██║   ██║██╔══██║   ██║   ██║   ██║██╔══██╗
██║██║ ╚████║   ██║   ███████╗██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║  ██║   ██║   ╚██████╔╝██║  ██║
╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝                                                                                            
                                                 
                                                   '''


helpstring = """
COMMAND           DESCRIPTION
-------------------------------------------------
set_api_key       to set new api key
print_api_key     to print api key
language          to set llm output language
quit              to exit program

"""


def start_sequence():
    
    from api_key_manager import ensure_api_key_is_verified
    if not ensure_api_key_is_verified():
        initiate_set_api_key()
    print(ascii_intro)
    
def main_sequence():
    #if api key not set (or wrong)
    # make user update it
    interrogations = []
    with get_openai_callback() as token_counts:
        
        while(should_close_program==False):
            print(helpstring)
            user_input = input("\n\ninput command or youtube video url:\n>")
            match user_input:
                case "help":
                    print(helpstring)
                case "set_api_key":
                    initiate_set_api_key()
                case "print_api_key":
                    print_api_key()
                case "language":
                    initiate_set_output_lanugage()
                case "folder":
                    initiate_set_output_folder_path()
                case "quit":
                    print("\nYou ended this run.")
                    if len(interrogations)>0:
                        print(f"\n____________________\nInterrogated videos:")
                        print("\n")
                        for interrogation in interrogations:
                            print(interrogation[0][0]['title'])
                        print("\n")
                    print(f"{token_counts}")
                              
                    


                    break
                case "save":
                    for interrogation in interrogations:
                        save_interrogation(interrogation)
                case _:
                    try:
                        interrogation = interrogate_loop(user_input)


                    except Exception as e:
                        pass



def run():
    start_sequence()
    main_sequence()
    print("\n\n\n END OF PROGRAM\n\n\n")
    


if __name__ == "__main__":
    run()

    
# INTERPRET_COMMAND
# PRINT_MENU# PRINT_LONG_HELPok
