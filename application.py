import json
from utils.get_transcript import get_transcript
from utils.helper import get_video_id, parse_json_data, parse_transcript, delete_audio_file, get_yt_video_metadata
from utils.get_audio import download_youtube_audio
from utils.get_transcript_from_whisper import get_transcript_from_whisper
from summarizer import summarize
# import logging
from aws_clients.write_to_database import add_item_to_table


# log_format = "%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s"
# date_format = "%Y-%m-%d %H:%M:%S"
# # logging.basicConfig(level=logging.DEBUG, filename='data.log',
# filemode='w', format=log_format, datefmt=date_format)


def process_jobs(job):
    print("JOb received")
    # videoURl = parse_json_data(job)
    videoURL = "https://www.youtube.com/watch?v=fJ9rUzIMcZQ"
    videoId = get_video_id(videoURL)
    # logging.info("Received job for video: %s", videoId)
    # logging.info("Getting transcript for video: %s", videoId)
    video_transcript = get_transcript(videoId)
    print(video_transcript)
    if video_transcript is None:
        # logging.info("No transcript found for video: %s", videoId)
        # logging.info("Downloading audio for video: %s", videoId)
        audio_file_path = download_youtube_audio(videoURL)
        # logging.info("Downloaded audio file to: %s", audio_file_path)
        # if audio_file_path is None:

        # logging.error("Error downloading audio for video: %s", videoId)
        # logging.info(
        # "Getting transcript for video: %s using OpenAI API", videoId)
        video_transcript = get_transcript_from_whisper(audio_file_path).text
        # logging.info(
        # "Generated transcript for video: %s using Whisper", videoId)
        # logging.info("Deleting audio file for video: %s", videoId)
        delete_audio_file(audio_file_path)
    else:
        # logging.info("Transcript found for video: %s", videoId)
        video_transcript = parse_transcript(video_transcript)
    # logging.info("Entering summarizer for video: %s", videoId)
    video_summary = summarize(video_transcript)
    # logging.info("Summarized video: %s", videoId)
    video_metadata = get_yt_video_metadata(videoURL)
    # logging.info("Got metadata for video: %s", videoId)
    # logging.info("Metadata: %s", video_metadata)
    # logging.info("Adding item to table for video: %s", videoId)
    _ = add_item_to_table(video_metadata, video_summary)
    # logging.info("Added item to table for video: %s", videoId)
    # logging.info("Job complete for video: %s", videoId)
    print("Job complete for video: ", videoId)
    return videoId


process_jobs("https://www.youtube.com/watch?v=2xomWWncop0")
