from get_transcript import fetch_metadata_by_url
from invocations import summarize_transcript
from invocations import invoke_interrogate_chunk, invoke_merge_chunk_interrogation_responses, calculate_chunk_size_for_interrogation
from parsing_utilities import parse_video_metadata, parse_transcript, section_print
from parsing_utilities import is_url, is_youtube_url
from save_to_file import save_interrogation

from langchain_community.callbacks import get_openai_callback
import os
import re
from datetime import datetime
from collections import namedtuple


interrogation_helpstring = '''

commands:

COMMAND           DESCRIPTION
---------------------------------------------------------
end               Finalize session and exit to main loop
save              Create a text file from this session


otherwise you can ask, for instance to:
- expand a topic mentioned in summary
- ask to list specific kind of information you think may be in the transcript
'''





def interrogate_loop(yt_url):
    if "htttp" in yt_url:
        print("http")
        if "youtube.com" not in yt_url:
            raise ValueError("ERROR: user input is not a valid youtube url")
        print("youtube")
    try:
        with get_openai_callback() as token_counts:     
            metadata = fetch_metadata_by_url(yt_url, get_transcript=True)
            basic_metadata = parse_video_metadata(metadata)
            summary = summarize_transcript(metadata)
            section_print(token_counts, "TOKENS USED FOR THIS QUESTION AND ANSWER")
            print("\n\n")

        print(basic_metadata)  
        print(summary)
        interrogation_log = [[metadata, summary]]
        exchanges = []

        should_keep_interrogating = True

        while should_keep_interrogating:
            print("\nfor commands type 'help'\n\n")
            request = input('ask me something about the transcript:\n\n>')
            if is_url(request):
                if is_youtube_url(request):
                        print(f""" you are currently working on the video:\n "{metadata['title']}"
                                    \nIf you want to start with new video, proceed to end this session
""")
                        print(interrogation_helpstring)
                        return(request) # program loop will now check for yt url and begins new session
            match request:
                case "help":
                    print(interrogation_helpstring)
                case "save":
                    interrogation_log.extend(exchanges)
                    save_interrogation(interrogation_log)
                    should_keep_interrogating = False 
                
                case "end":
                    should_keep_interrogating = False
                    
                case _:
                    with get_openai_callback() as token_counts: 
                        response = one_shot_interrogate(metadata,request,exchanges)
                        exchanges.append([request, response])
                        print("\n\n")
                        section_print(response, request)
                        section_print(token_counts, "\TOKENS USED FOR THIS QUESTION AND ANSWER")
                        print("\n\n")


    

    except Exception as e:
        print(f"ERROR: interrogate_transcript failed.  \n MESSAGE: {e}\n.")
 

def one_shot_interrogate(video_metadata, request, previous_conversation_list_of_lists):
    print("initiating one shot interrogation with chunking capability")
    # max_chunk_size = 28000
    max_chunk_size = calculate_chunk_size_for_interrogation(request,previous_conversation_list_of_lists)
    try:
        transcript_text = parse_transcript(video_metadata['transcript_entries'])
        from hard_chunker import hard_chunk_to_strings
        chunks = hard_chunk_to_strings(transcript_text,max_chunk_size)
        chunk_responses = []
        for chunk in chunks:
            print(f"processing chunk {len(chunk_responses)+1} of {len(chunks)} (using previous exchanges)...")
            response = invoke_interrogate_chunk(chunk, request, previous_conversation_list_of_lists)
            chunk_responses.append(response)
        print("integrating chunk analyses...")
        final_response= invoke_merge_chunk_interrogation_responses(request, chunk_responses)
        return final_response
        
    except Exception as message:
        print(f"ERROR: one shot interrogation with chunking failed \nMESSAGE: {message} ")






if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=fdiTaI4gdmA&t=291s" # supersalience
    # url = "https://www.youtube.com/watch?v=5sDzvJn04Dc&list=PLnNSjVGWqTO6WqTCsGBqZDwvL1Beo7VHN" # jim rutt + ryan patrick
    # url = "https://www.youtube.com/watch?v=td6fozpEb1U" # citizen s2
    url = "https://www.youtube.com/watch?v=1aA1WGON49E" #1 min lecture
    interrogate_loop(url)
