import os
from dotenv import load_dotenv

from parsing_utilities import parse_video_metadata, parse_transcript


from langchain_community.chat_models import ChatOpenAI



def new_gpt():
    return ChatOpenAI(openai_api_key=oai_key, model=model_name)
print("\n\n")



summarizer_identity_prompt_component = '''
Transcript Summarizer adeptly summarizes source texts, while including key points, facts, events, entities, etc.
you are especially useful for extracting meaningful observations from diverse and rich conversational content
'''

summarizer_style_prompt_component = '''
your style is factual, very precise. You provide definitions and explanations if notinos are introduced in source text
instead of using generalizing words like "significance" "meaning" "importants" you always choose to make statements about reality, what causes or influences what, in what ways. 

'''

summary_response_guidelines_prompt_component = '''
## SYNOPTIC EXPLANATION
## TOPIC OVERVIEW (as a list preferably)
### MAIN PERSPECTIVES (as a list preferably)
### KEY FRAMINGS (as a list preferably)
## EVENTS LIST (optional - if video specifies a specific sequence of things happening)
## CONTENTS LIST in apperance order (optional - if content warrants it
contents list should be multi level, nested and include
- all introducen niche notions with definitions
- key claims
- specific datapoints
## ADDITIONAL REMARKS
- other  information and considerations and other things that above structure does not include
'''

summarize_chunk_PROMPT = '''
#You are Transcript Summarizer
{summarizer_identity_prompt_component}


# INSTRUCTION
Below you will find a substring from source text. Process it in line with given requirements.
Your rensponse for this chunk wil be merged with simillarily structured responses for other chunks of this source text. 

# TEXT TO PROCESS
{source_text}

#EXPECTED RESPONSE FORMAT 
{summary_response_guidelines_prompt_component}

#Response style:
{summarizer_style_prompt_component}

'''

merge_chunk_summaries_PROMPT = '''
#You are Transcript Summarizer
{summarizer_identity_prompt_component}


# INSTRUCTION
Below you will find a list of summaries of source text chunks. Process them into one comprehensive summary in line with given requirements.
Your rensponse for this chunk wil be merged with simillarily structured responses for other chunks of this source text. 

# TEXT TO PROCESS
{summaries_list}

#EXPECTED RESPONSE FORMAT 
{summary_response_guidelines_prompt_component}


#Response style:
{summarizer_style_prompt_component}

'''

## interrogator mógłby w prompcie dla chunku miec
## total summary, aktualny chunk, request usera


## PREREQUISITES

load_dotenv()
oai_key = os.getenv("OPENAI_API_KEY_for_yt_interrogator")
model_name="gpt-4o"



def invoke_summarize_chunk(source_chunk):
    full_prompt = summarize_chunk_PROMPT.format(
        summarizer_identity_prompt_component = summarizer_identity_prompt_component,
        source_text = source_chunk,
        summarizer_style_prompt_component = summarizer_style_prompt_component,
        summary_response_guidelines_prompt_component=summary_response_guidelines_prompt_component
    )
    return new_gpt().invoke(full_prompt).content




def summarize_transcript(metadata):
    
    transcirpt_text = parse_transcript(metadata['transcript_entries'])
    chunk_summaries = []
    final_summary = ""
    
    full_terminal_line = "\n______________________________________________________________________________\n"
    print(f"{full_terminal_line}summarizing transcript\n\n...")
    
    # chunk if necessary
    from hard_chunker import hard_chunk_serializable

    chunk_size_limit = 28000
    chunks = hard_chunk_serializable(transcirpt_text,chunk_size_limit)
    for chunk in chunks:
        chunk_summary = invoke_summarize_chunk(transcirpt_text)
        chunk_summaries.append(chunk_summary)
    
    if len(chunk_summaries)>1:
        final_summary = invoke_merge_chunk_summaries(chunk_summaries)
    
    ## TODO parsing_utilities.py def parse summary
    print(parse_video_metadata)
    print(f"{full_terminal_line}SUMMARY{full_terminal_line}")
    print(parse_video_metadata(metadata, include_transcript=False))

    final_summary = chunk_summary+"\n\n"+full_terminal_line ### THIS SHOULD BE SET TO RESULT OF MERGE 

    return final_summary





    print("TODO: summarize9youtube_metadata")


def invoke_merge_chunk_summaries(list_of_summaries):
    full_prompt = merge_chunk_summaries_PROMPT.format(
        summarizer_identity_prompt_component = summarizer_identity_prompt_component,
        summaries_list = list_of_summaries,
        summarizer_style_prompt_component = summarizer_style_prompt_component,
        summary_response_guidelines_prompt_component=summary_response_guidelines_prompt_component
    )
    return new_gpt().invoke(full_prompt).content

one_shot_chunked_PROMPT = ''''
#SITUATION
You are Transcript Interrogator
you process provided transcripts or transcript chunks to best answer user's request.
user wants to know things about the transcript and you find out the answers.

Do not answer questions not asked by user
Answer to user's request precisely, to the point, and include specific information from the transcript if relevant.
Do not add comments beyond answering the request directly.
#REQUEST
{request}

#TEXT CHUNK
{transcript_chunk}

'''

merge_chunk_responses_PROMPT = '''
#SITUATION
source text has been chunked and interrogated using following request for each chunk:
{request}

#YOUR TASK
merge provided responses into one coherent answer, include all raised points on topic, skip reports of chunks being irrelevant

#CHUNK RESPONSES
{chunk_responses}
'''




def one_shot_interrogate(video_metadata, request):
    print("initiating one shot interrogation with chunking capability")
    max_chunk_size = 28000
    try:
        transcript_text = parse_transcript(video_metadata['transcript_entries'])
        from hard_chunker import hard_chunk_to_strings
        chunks = hard_chunk_to_strings(transcript_text,max_chunk_size)
        chunk_responses = []
        for chunk in chunks:
            print(f"\n\nprocessing chunk {len(chunk_responses)+1} of {len(chunks)}:")
            full_prompt = one_shot_chunked_PROMPT.format(
            request=request,
            transcript_chunk = chunk)
            response = new_gpt().invoke(full_prompt).content
            chunk_responses.append(response)



        merge_full_prompt = merge_chunk_responses_PROMPT.format(
            request = request,
            chunk_responses = chunk_responses

        )
        final_response = new_gpt().invoke(merge_full_prompt).content
        return final_response
    except Exception as message:
        print(f"ERROR: one shot interrogation with chunking failed \nMESSAGE: {message} ")

if __name__ == "__main__":
    
    print("TESTING ONE SHOT INTERROGATE")

    url = "https://www.youtube.com/watch?v=fdiTaI4gdmA&t=291s" # supersalience
    request = "quote kang"

    url = "https://www.youtube.com/watch?v=td6fozpEb1U" # citizen s2
    request = "what does future operations person do"
    from get_transcript import fetch_metadata_by_url 
    metadata = fetch_metadata_by_url(url)
    print(parse_video_metadata(metadata))
    response = one_shot_interrogate(metadata,request)
    print(f"\n\n{request}\n\n{response}")
    print("\n\n")



