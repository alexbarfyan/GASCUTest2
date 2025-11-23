from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

# ---------- OpenAI client ----------
# Make sure OPENAI_API_KEY is set in Render → Environment
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Your published prompt
PROMPT_ID = "pmpt_69215e9582e081968dd5810b961e517f08893b154215bcb7"

# ---------- FastAPI app ----------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can lock this to your github.io domain later
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "Eric backend is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message:
        raise HTTPException(status_code=400, detail="Message is required")

    try:
        # Use the Responses API with your prompt
        response = client.responses.create(
            prompt={
                "id": PROMPT_ID,
                "version": "1"
            },
            input=req.message,
        )

        # Helper to get text; adjust if your client version differs
        # For current SDKs, this usually works:
        reply_text = response.output_text

        return ChatResponse(reply=reply_text)

    except Exception as e:
        print("OpenAI error:", e)
        raise HTTPException(status_code=500, detail="OpenAI error")
