import tiktoken
from pytube import YouTube
import os


def get_video_id(url):
    """
    Extract the video ID from a YouTube video URL.

    Args:
        url (str): The URL of the YouTube video.

    Returns:
        str: The video ID extracted from the URL.
    """
    if "youtube.com" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be" in url:
        return url.split("/")[-1]
    else:
        return None


def parse_json_data(json_data):
    """
    Parse JSON data to extract the video URL.

    Args:
        json_data (dict): JSON data containing video information.

    Returns:
        str: The URL of the video.
    """
    return json_data.get('videoURL', None)


def parse_transcript(transcript):
    """
    Parse a list of transcript items into a single paragraph.

    Args:
        transcript (list): A list of transcript items, where each item contains a 'text' key.

    Returns:
        str: The concatenated text from all transcript items as a single paragraph.
    """
    return " ".join(item['text'] for item in transcript).strip()


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """
    Get the number of tokens in the given text.

    Args:
        text (str): The text to count the tokens for.

    Returns:
        int: The number of tokens in the text.
    """
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def get_yt_video_metadata(url: str):
    """
    Get metadata for a YouTube video using the tiktok API.

    Args:
        video_id (str): The ID of the YouTube video.

    Returns:
        dict: The metadata for the YouTube video.
    """
    yt = YouTube(url)

    metadata = {
        "title": yt.title,
        "description": yt.description,
        "author": yt.author,
        "length": yt.length,
        "views": yt.views,
        "rating": yt.rating,
        "thumbnail_url": yt.thumbnail_url,
        "publish_date": yt.publish_date,
        "keywords": yt.keywords,
        "video_id": yt.video_id,
    }

    return metadata


def delete_audio_file(file_path: str):
    """
    Delete the audio file at the given path.

    Args:
        file_path (str): The path to the audio file to delete.
    """
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Error deleting audio file: {e}")
