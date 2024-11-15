from datetime import datetime, timedelta

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
    
    return transcript_string