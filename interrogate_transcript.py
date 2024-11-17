from get_transcript import fetch_subtitles_by_url, fetch_metadata_by_url
from invocations import summarize_transcript, one_shot_interrogate

from parsing_utilities import parse_video_metadata




interrogation_helpstring = '''

commands:

end - will finalize session
TODO get_topic_times {topic}  - will ask llm to give timestamps where each topic is mentioned

you can for instance:
ask about specific details in the video
ask about 

'''





def interrogate_transcript(yt_url):
    if "htttp" in yt_url:
        print("http")
        if "youtube.com" not in yt_url:
            raise ValueError("ERROR: user input is not a valid youtube url")
        print("youtube")
    try:

        metadata = fetch_metadata_by_url(yt_url, get_transcript=True)
        print(parse_video_metadata(metadata))
        summary = summarize_transcript(metadata)
        print(summary)
        print("for commands type 'help'\n\n")

        interrogation_memory = []
        should_keep_interrogating = True

        while should_keep_interrogating:
            print("\nfor commands type 'help'\n\n")
            request = input('ask me something about the transcript: \n>')
            match request:
                case "help":
                    print(interrogation_helpstring)
                case "end":
                    should_keep_interrogating = False
                case _:
                    response = one_shot_interrogate(metadata,request)
                    print(f"\n\n{request}\n\n{response}")
                    print("\n\n")
                    from parsing_utilities import section_print
                    section_print(response, request)
                    ## LEARN TO USE CHAT MODEL INSTEAD?
                    #interrogation_memory.extend([request, response])

    

    except Exception as e:
        print(f"ERROR: interrogate_transcript failed.  \n MESSAGE: {e}\n.")
        
    

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=fdiTaI4gdmA&t=291s" # supersalience
    # url = "https://www.youtube.com/watch?v=5sDzvJn04Dc&list=PLnNSjVGWqTO6WqTCsGBqZDwvL1Beo7VHN" # jim rutt + ryan patrick
    # url = "https://www.youtube.com/watch?v=td6fozpEb1U" # citizen s2

    interrogate_transcript(url)
