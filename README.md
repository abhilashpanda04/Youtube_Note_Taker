# 🎥 YouTube Video Summarizer

A powerful tool that uses AI to extract and summarize transcripts from YouTube videos, making content consumption faster and more efficient.

## 🌟 Features

- 📝 Extracts transcripts from YouTube videos
- 🤖 Uses advanced LLM (Ollama with Qwen3) for summarization
- ✨ Clean and simple command-line interface
- 🔍 Handles video URLs validation automatically
- 📊 Provides concise, readable summaries

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd youtube-summerizer
```

2. Install dependencies:
```bash
pip install -e .
```

## 💻 Usage

Run the program from the command line:

```bash
python src/main.py
```

When prompted, enter a YouTube video URL. The program will:
1. Fetch the video transcript
2. Process it through the LLM
3. Generate a concise summary

## 🛠️ Tech Stack

- `youtube_transcript_api`: For fetching video transcripts
- `pydantic`: For data validation
- `ollama`: For LLM integration
- `loguru`: For logging

## 📝 Example

```python
from src.main import main

# Simply pass a YouTube URL
main("https://www.youtube.com/watch?v=your_video_id")
```

## ⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📬 Contact

Your Name - [Your Email]

Project Link: [Repository URL]