import json
import redis
from utils.get_transcript import get_transcript
from utils.helper import get_video_id, parse_json_data, parse_transcript, delete_audio_file, get_yt_video_metadata
from utils.get_audio import download_youtube_audio
from utils.get_transcript_from_whisper import get_transcript_from_whisper
from summarizer import summarize
import logging
from aws_clients.write_to_database import add_item_to_table

r = redis.Redis()
log_format = "%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.DEBUG, filename='data.log',
                    filemode='w', format=log_format, datefmt=date_format)

while True:
    # Blocking pop operation, waits until an item is available
    _, data = r.blpop('jsonQueue1')
    json_data = json.loads(data)
    videoURl = parse_json_data(json_data)
    videoId = get_video_id(videoURl)
    logging.info("Received job for video: %s", videoId)
    logging.info("Getting transcript for video: %s", videoId)
    transcript = get_transcript(videoId)

    if transcript is None:
        logging.info("No transcript found for video: %s", videoId)
        logging.info("Downloading audio for video: %s", videoId)
        audio_file_path = download_youtube_audio(videoURl)
        logging.info("Downloaded audio file to: %s", audio_file_path)
        if audio_file_path is None:
            logging.error("Error downloading audio for video: %s", videoId)
            continue
        logging.info(
            "Getting transcript for video: %s using OpenAI API", videoId)
        transcript = get_transcript_from_whisper(audio_file_path).text
        logging.info(
            "Generated transcript for video: %s using Whisper", videoId)
        logging.info("Deleting audio file for video: %s", videoId)
        delete_audio_file(audio_file_path)
    else:
        logging.info("Transcript found for video: %s", videoId)
        transcript = parse_transcript(transcript)
    logging.info("Entering summarizer for video: %s", videoId)
    summary = summarize(transcript)
    logging.info("Summarized video: %s", videoId)
    metadata = get_yt_video_metadata(videoURl)
    logging.info("Got metadata for video: %s", videoId)
    logging.info("Metadata: %s", metadata)
    logging.info("Adding item to table for video: %s", videoId)
    response = add_item_to_table(metadata, summary)
    logging.info("Added item to table for video: %s", videoId)
    logging.info("Job complete for video: %s", videoId)
    print("Job complete for video: ", videoId)
    print(response)


