import json
import redis
from utils.get_transcript import get_transcript
from utils.helper import get_video_id, parse_json_data, parse_transcript, delete_audio_file
from utils.get_audio import download_youtube_audio
from utils.get_transcript_from_whisper import get_transcript_from_whisper
from summarizer import summarize

r = redis.Redis()

while True:
    # Blocking pop operation, waits until an item is available
    _, data = r.blpop('jsonQueue1')
    json_data = json.loads(data)
    videoURl = parse_json_data(json_data)
    videoId = get_video_id(videoURl)
    transcript = get_transcript(videoId)
    if transcript is None:
        print(f'No transcript found for video: {videoId}')
        print(f'Downloading audio for video: {videoId}')
        audio_file_path = download_youtube_audio(videoURl)
        print(f"Audio file path: {audio_file_path}")
        if audio_file_path is None:
            print(f'Error downloading audio for video: {videoId}')
            continue
        print(f'Getting transcript for video: {videoId} using OpenAI API')
        transcript = get_transcript_from_whisper(audio_file_path).text
        delete_audio_file(audio_file_path)
    else:
        transcript = parse_transcript(transcript)
    summary = summarize(transcript)
    print(f"Summary: {summary}")
