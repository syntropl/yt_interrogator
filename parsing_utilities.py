from datetime import datetime, timedelta
import re

def is_url(string_input: str) -> bool:
    url_pattern = re.compile(
        r'^(https?://)?'  # Optional scheme
        r'(([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})'  # Domain
        r'(/.*)?$'  # Optional path
    )
    return bool(url_pattern.match(string_input))

def is_youtube_url(string_input: str) -> bool:
    youtube_pattern = re.compile(
        r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)(/.*)?$'
    )
    return bool(youtube_pattern.match(string_input))






def section_print(text, title=None):
    print("\n\n")
    if title:
        print("______________________________________________________________________________")
        print(f"\n{title}")
    print("______________________________________________________________________________")
    print(f"\n{text}")
    print("______________________________________________________________________________\n")
    






def format_duration(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}h:{int(minutes):02}m:{int(seconds):02}s"

def parse_transcript(transcript_entries, include_times=False):
    if not transcript_entries:
        return "No transcript found"
    
    transcript_string = ""
    for entry in transcript_entries:
        if include_times:
            formatted_start = format_duration(entry['start'])
            transcript_string += f"\n[{formatted_start}]  "
        transcript_string += entry['text']
    transcript_string+="\n\n______________________________________________________________________________\n\n\n"
    
    
    return transcript_string

def parse_video_metadata(metadata, include_transcript=True):
    # Set line length based on the longest string in 'title' or 'url'
    line_length = max(len(metadata['title']), len(metadata['url']))
    line_string = "_" * line_length

    # Format date (assuming it's a string in YYYYMMDD format)
    upload_date = datetime.strptime(metadata['upload_date'], "%Y%m%d").strftime("%Y-%m-%d")

    duration = format_duration(metadata['video_duration_in_seconds'])
    transcript_entries = metadata['transcript_entries']

    metadata_printable_string = f'''

{line_string}
{metadata['url']}
{line_string}
{metadata['title']}
{metadata['uploader']}
\n
{upload_date}
{duration}
{line_string}

'''
    if include_transcript:
        metadata_printable_string+=parse_transcript(transcript_entries,include_times=True)
    return metadata_printable_string

def serialize_session(interrogation_list_of_lists):
    complete_metadata = interrogation_list_of_lists[0][0]
    parsed_basic_metadata = parse_video_metadata(complete_metadata, include_transcript=False)  # This is a dict parsed into string
    parsed_transcript = parse_transcript(complete_metadata['transcript_entries'], include_times=True)
    
    summary = interrogation_list_of_lists[0][1]  # This is a string
    exchanges = interrogation_list_of_lists[1:]  # This is a list of lists of strings

    line_separator = "\n_____________________________________\n"

    output = "(full transcript is at the bottom of this file)\n"
    output += f"{parsed_basic_metadata}\n"

    output += f"{summary}\n"
    for exchange in exchanges:
        output += line_separator
        if len(exchange) >= 2:
            output += f"{exchange[0]}\n"
            output += line_separator
            output += f"{exchange[1]}\n"
            if len(exchange) > 2:
                # Join any additional exchange parts with newlines
                additional_parts = "\n".join(exchange[2:])
                output += line_separator
                output += f"{additional_parts}\n"
        else:
            # Handle cases where exchange has fewer than 2 elements
            output += "\n".join(exchange) + "\n"
    
    output += line_separator
    output += f"{parsed_basic_metadata}\n"
    output += line_separator
    output += "\nFULL TRANSCRIPT\n"
    output += line_separator    
    output += f"{parsed_transcript}"
    
    return output
