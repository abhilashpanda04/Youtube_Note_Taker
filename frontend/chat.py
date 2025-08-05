import chainlit as cl
from chainlit.input_widget import TextInput, Select
import httpx

@cl.on_chat_start
async def start():
    # Send welcome message with input instructions
    await cl.Message(
        content="Welcome to YouTube Summarizer! Please select a mode and enter a YouTube URL.",
        author="System"
    ).send()

    # Create and send input elements
    await cl.Message(
        content="",
        elements=[
            Select(
                id="mode",
                label="Select Mode",
                values=["Transcript", "Summary", "Both"],
                initial_value="Transcript"
            ),
        ]
    ).send()

@cl.on_message
async def main(message: cl.Message):
    # Get the mode from the last message's elements
    settings = message.elements
    mode = settings[0].value if settings else "Transcript"
    video_url = message.content

    try:
        async with httpx.AsyncClient() as client:
            if mode == "Transcript":
                response = await client.post(
                    "http://localhost:8000/fetch-transcript",
                    json={"video_url": video_url}
                )
                result = response.json()["transcript"]
            
            elif mode == "Summary":
                response = await client.post(
                    "http://localhost:8000/summarize",
                    json={"video_url": video_url}
                )
                result = response.json()["summary"]
            
            else:  # Both
                transcript_response = await client.post(
                    "http://localhost:8000/fetch-transcript",
                    json={"video_url": video_url}
                )
                summary_response = await client.post(
                    "http://localhost:8000/summarize",
                    json={"video_url": video_url}
                )
                result = f"""
                Transcript: {transcript_response.json()['transcript']}
                
                Summary: {summary_response.json()['summary']}
                """

        await cl.Message(
            content=result,
        ).send()

    except Exception as e:
        await cl.Message(
            content=f"Error processing request: {str(e)}",
            type="error"
        ).send()
