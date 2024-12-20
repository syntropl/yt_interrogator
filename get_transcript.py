

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


# from parsing_utilities import format_duration, parse_transcript
import re

from datetime import datetime
from collections import namedtuple



import yt_dlp



""""usage
(url string) -> fetch_metadata_by_url -> (metadata dict) can include transcript
(metadata dict) -> parse_video_metadata -> (printable string with metadata, transcript is optional)

(url string) -> fetch_subtitles_by_url -> (tanscript entries list)

transctipt_entries is a  list of dicts (metadata[transcript_entries])

each entry contains three default fields:
metadata['transcript_entries'][index][text] = line of subtitles
metadata['transcript_entries'][index][start] = time in video of subtitle
metadata['transcript_entries'][index][duration] = duration of subtitle on screen

"""



def fetch_subtitles_by_url(video_url):
    """
    Fetches YouTube transcript for the given URL.
    Returns the English transcript if available; otherwise, returns the original language transcript.
    
    :param url: str - YouTube video URL
    :return: list of transcript entries or None if no transcript is found
    """
    # Extract video ID from the URL
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', video_url)
    if not match:
        print("Invalid YouTube URL.")
        return None


   
    video_id = match.group(1)

    try:
        # First, try to fetch the English transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        print("English transcript fetched successfully.\n")
        return transcript
    
    except (TranscriptsDisabled, NoTranscriptFound):
        print("English transcript not available. Attempting to fetch the original language transcript.")
        try:
            # Fetch the list of available transcripts
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Select the first available transcript (original language)
            transcript = transcript_list.find_transcript([transcript.language_code for transcript in transcript_list])
            transcript_fetch = transcript.fetch()
            print(f"Transcript fetched in '{transcript.language}' language.")
            return transcript_fetch
        except (TranscriptsDisabled, NoTranscriptFound):
            print("No transcripts available for this video.")
            return None
        except Exception as e:
            print(f"An error occurred while fetching the original transcript: {str(e)}")
            return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None
    


def fetch_metadata_by_url(video_url, get_transcript=True):

    transcript_entries = []
    if (get_transcript):
        transcript_entries = fetch_subtitles_by_url(video_url)

    ydl_opts = {
        'quiet': True,
        'no_warnings': True 
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        metadata = {
            'title': info.get('title', 'Unknown Title'),
            'url': video_url,
            'upload_date': info.get('upload_date', 'Unknown Date'),
            'uploader': info.get('uploader', 'Unknown Channel'),
            'video_duration_in_seconds': info.get('duration', 0),
            'transcript_entries': transcript_entries
        }
        return metadata


## THIS SHOULD BE IN parsing_utilities.py
# def parse_video_metadata(metadata, include_transcript=True):
#     # Set line length based on the longest string in 'title' or 'url'
#     line_length = max(len(metadata['title']), len(metadata['url']))
#     line_string = "_" * line_length

#     # Format date (assuming it's a string in YYYYMMDD format)
#     upload_date = datetime.strptime(metadata['upload_date'], "%Y%m%d").strftime("%Y-%m-%d")

#     duration = format_duration(metadata['video_duration_in_seconds'])
#     transcript_entries = metadata['transcript_entries']

#     metadata_printable_string = f'''

# {line_string}
# {metadata['url']}
# {line_string}
# {metadata['title']}
# {metadata['uploader']}
# \n
# {upload_date}
# {duration}
# {line_string}

# '''
#     if include_transcript:
#         metadata_printable_string+=parse_transcript(transcript_entries,include_times=True)
#     return metadata_printable_string


# def print_youtube_metadata(metadata, include_transcript=True):

#     # Set line length based on the longest string in 'title' or 'url'
#     line_length = max(len(metadata['title']), len(metadata['url']))
#     line_string = "_" * line_length

#     # Format date (assuming it's a string in YYYYMMDD format)
#     upload_date = datetime.strptime(metadata['upload_date'], "%Y%m%d").strftime("%Y-%m-%d")

#     # Format duration (convert seconds to HH:MM:SS)
#     total_seconds = metadata['video_duration_in_seconds']
#     hours, remainder = divmod(total_seconds, 3600)
#     minutes, seconds = divmod(remainder, 60)
#     duration = f"{hours:02}h:{minutes:02}m:{seconds:02}s"

#     transcript_entries = metadata['transcript_entries']

#     print(f'''

# {line_string}
# {metadata['url']}
# {line_string}
# {metadata['title']}
# {metadata['uploader']}
# \n
# {upload_date}
# {duration}
# {line_string}

# ''')
#     if(transcript_entries):
#         print(parse_transcript(transcript_entries, include_times=False))
#     else:
#         print("Transcript not found")
    



def test_print_all_metadata():
    url = "https://www.youtube.com/watch?v=fdiTaI4gdmA&t=291s" # supersalience
    print(parse_video_metadata(fetch_metadata_by_url(url),include_transcript=True))
    print("\n\n")


# Example usage
if __name__ == "__main__":
    print("\n\n\n")
    test_print_all_metadata()



