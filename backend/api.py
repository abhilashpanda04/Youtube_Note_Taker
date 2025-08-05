from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.main import YouTubeTranscriptFetcher
from backend.llm import LLM
from backend.prompt import Prompt
from nest_asyncio import apply
apply()

app = FastAPI(
    title="YouTube Transcript Fetcher API",
    description="API to fetch and summarize YouTube video transcripts",
    version="1.0.0"
)

class VideoRequest(BaseModel):
    video_url: str

@app.get("/")
async def root():
    return {"message": "Welcome to the YouTube Summarizer API"}

@app.post("/fetch-transcript")
async def fetch_transcript(request: VideoRequest):
    try:
        fetcher = YouTubeTranscriptFetcher(youtube_url=request.video_url)
        transcript = fetcher.get_youtube_transcript()
        return {
            "status": "success",
            "transcript": transcript
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching transcript: {str(e)}"
        )

@app.post("/summarize")
async def summarize(request: VideoRequest):
    try:
        
        fetcher = YouTubeTranscriptFetcher(youtube_url=request.video_url)
        transcript = fetcher.get_youtube_transcript()
        print(f"Transcript: {transcript}")
        prompt = Prompt()
        llm = LLM(provider_type="ollama", model_name="qwen3:8b")
        result = await llm.run(prompt.user_prompt.format(youtube_transcription=transcript))
        return {
            "status": "success",
            "summary": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching transcript: {str(e)}"
        )
