from get_transcript import fetch_subtitles_by_url, fetch_metadata_by_url
from invocations import summarize_transcript

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
            request = input('ask me something about the transcript: \n>')
            match request:
                case "help":
                    print(interrogation_helpstring)
                case "end":
                    should_keep_interrogating = False
                case _:
                    response = one_shot_interrogate(request)
                    ## LEARN TO USE CHAT MODEL INSTEAD?
                    interrogation_memory.append(request, response)

    

    except Exception as e:
        print(f"ERROR: fetching youtbe metadata failed. \n MESSAGE: {e}")
        
    

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=fdiTaI4gdmA&t=291s" # supersalience
    interrogate_transcript(url)
