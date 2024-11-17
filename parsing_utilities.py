from datetime import datetime, timedelta

def section_print(text, title=None):
    print("\n\n")
    if title:
        print("______________________________________________________________________________")
        print(f"\n{title}")
    print("______________________________________________________________________________")
    print(text)
    print("\n\n______________________________________________________________________________\n")
    

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