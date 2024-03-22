from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import CouldNotRetrieveTranscript, NoTranscriptFound

def get_transcript(video_id):
    """
    Retrieve the transcript of a YouTube video.

    Args:
        video_id (str): The ID of the YouTube video.

    Returns:
        list or None: A list of transcript items if available, or None if no transcript is found or an error occurs.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id=video_id)
        print(transcript)
        return ""
    except (NoTranscriptFound, CouldNotRetrieveTranscript):
        return None
    except Exception as e:
        return str(e)
