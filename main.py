from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

# ---- OpenAI client (key must be set in Render env) ----
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Your published prompt ID
PROMPT_ID = "pmpt_69215e9582e081968dd5810b961e517f08893b154215bcb7"

# ---- FastAPI app ----
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later you can restrict to your github.io origin
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# Health-check route so / doesn’t 404
@app.get("/")
async def health():
    return {"status": "ok", "message": "Eric backend is running"}

# Chat endpoint used by your front-end
@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message:
        raise HTTPException(status_code=400, detail="Message is required")

    try:
        # Call Responses API with your prompt
        response = client.responses.create(
            prompt={
                "id": PROMPT_ID,
                "version": "1",
            },
            input=req.message,
        )

        # New SDKs expose this helper:
        reply_text = response.output_text

        return ChatResponse(reply=reply_text)

    except Exception as e:
        print("OpenAI error:", e)
        raise HTTPException(status_code=500, detail="OpenAI error")
