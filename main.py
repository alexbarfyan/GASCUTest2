from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

# ---- OpenAI client ----
# Make sure OPENAI_API_KEY is set in Render → Environment
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set in environment")

client = OpenAI(api_key=api_key)

PROMPT_ID = "pmpt_69215e9582e081968dd5810b961e517f08893b154215bcb7"

# ---- FastAPI app ----
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict to your GitHub domain later
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# Health check so / returns something useful
@app.get("/")
async def health():
    return {"status": "ok", "message": "Eric backend is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message:
        raise HTTPException(status_code=400, detail="Message is required")

    try:
        # Call Responses API with your prompt
        response = client.responses.create(
            prompt={
                "id": PROMPT_ID,
                "version": "1"
            },
            input=req.message
        )

        # This helper should give you a plain text answer
        reply_text = response.output_text

        return ChatResponse(reply=reply_text)

    except Exception as e:
        # This will show up in Render logs
        print("OpenAI error:", repr(e))
        raise HTTPException(status_code=500, detail="OpenAI error")
