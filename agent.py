import logging
import os
import requests
from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
    metrics,
)
from livekit.agents.pipeline import VoicePipelineAgent
from deepgram import Deepgram
import openai
import torch
import torchaudio

# Load API Keys
load_dotenv()
API_KEY = os.getenv("LIVEKIT_API_KEY")
API_SECRET = os.getenv("LIVEKIT_API_SECRET")
LIVEKIT_WS_URL = os.getenv("LIVEKIT_WS_URL", "").strip()

if not API_KEY or not API_SECRET or not LIVEKIT_WS_URL:
    raise ValueError("Missing LiveKit API credentials. Check your .env file.")

logger = logging.getLogger("voice-assistant")
FLASK_SERVER_URL = "https://4a5a-183-82-27-92.ngrok-free.app/validate_audio"

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = torch.hub.load('snakers4/silero-vad', 'silero_vad', force_reload=True)

async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(role="system", text="You are a helpful voice assistant.")
    await ctx.connect(
    url=LIVEKIT_WS_URL,
    api_key=API_KEY,
    api_secret=API_SECRET,
    auto_subscribe=AutoSubscribe.AUDIO_ONLY
)
    participant = await ctx.wait_for_participant()

    async def before_tts_cb(text: str) -> str:
        words_per_second = 2
        estimated_duration = len(text.split()) / words_per_second
        response = requests.post(FLASK_SERVER_URL, json={"text": text, "duration": estimated_duration})
        return response.json().get("trimmed_text", text) if response.status_code == 200 else text

    agent = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=Deepgram.STT(model="nova-3-general"),
        llm=openai.LLM(),
        tts=openai.TTS(),
        chat_ctx=initial_ctx,
        before_tts_cb=before_tts_cb,
    )

    agent.start(ctx.room, participant)
    await agent.say("Hey, how can I help you today?", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
