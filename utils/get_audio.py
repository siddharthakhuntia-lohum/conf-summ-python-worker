import os
from utils.helper import get_video_id
from pytube import YouTube
from pydub import AudioSegment

def download_youtube_audio(url):
    """
    Download the audio from a YouTube video and convert it to WAV format.

    Args:
        url (str): The URL of the YouTube video.

    Returns:
        str or None: The path to the downloaded WAV audio file, or None if an error occurs.
    """
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        video_id = get_video_id(url)
        destination = "data"
        os.makedirs(destination, exist_ok=True)
        output_file = audio_stream.download(output_path=destination)
        video_id_file = os.path.join(destination, f"{video_id}.mp4")
        os.rename(output_file, video_id_file)
        return video_id_file
        # # Convert to WAV format using pydub
        # base, ext = os.path.splitext(output_file)
        # audio = AudioSegment.from_file(output_file)
        # wav_file = f"{base}.wav"
        # audio.export(wav_file, format='wav')

        # # Remove the original downloaded file
        # os.remove(output_file)

    except Exception as e:
        print(f"Error: {e}")
        return None