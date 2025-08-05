from youtube_transcript_api import YouTubeTranscriptApi
from pydantic import BaseModel, Field, AnyHttpUrl
from llm import LLM
from prompt import Prompt
from loguru import logger
from dotenv import load_dotenv


load_dotenv()


class YouTubeTranscriptFetcher:
    
    def __init__(self, youtube_url: str):
        """
        Initializes the YouTubeTranscriptFetcher with a valid YouTube URL.
        
        Args:
            youtube_url (ValidUrl): A model containing the YouTube video URL.
        """
        self.ytt_api = YouTubeTranscriptApi()
        self.youtube_url = AnyHttpUrl(url=youtube_url)
        self.video_id = str(self.youtube_url._url).split("v=")[-1]


    def get_youtube_transcript(self) -> str:
        try:
            transcript_list = self.ytt_api.fetch(self.video_id)
            transcript_text = ' '.join([entry.text for entry in transcript_list])
            return transcript_text
        except Exception as e:
            return f"Error getting transcript: {str(e)}"


def main(youtube_video_url: str):
    """
    Main function to run the YouTube transcript fetcher and LLM.
    """
    prompt = Prompt()
    llm = LLM(provider_type="ollama", model_name="qwen3:8b")
    logger.info("Fetching YouTube transcript...")

    fetcher = YouTubeTranscriptFetcher(youtube_video_url)
    transcript = fetcher.get_youtube_transcript()
    logger.info("Transcript fetched successfully.")
    result = llm.run(prompt.user_prompt.format(youtube_transcription=transcript))
    logger.info("LLM processing completed.")
    print("YouTube Video Summary:\n", result)



# Example usage
if __name__ == "__main__":
    youtube_video_url=input("Enter YouTube video URL: ")
    if not youtube_video_url:
        print("No URL provided. Exiting.")
    else:   
        main(youtube_video_url) if youtube_video_url else print("Please provide a valid YouTube video URL.")