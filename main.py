from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

PROMPT_ID = "pmpt_69215e9582e081968dd5810b961e517f08893b154215bcb7"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        response = client.responses.create(
            prompt={
                "id": PROMPT_ID,
                "version": "1"
            },
            input=req.message
        )

        return {"reply": response.output_text}

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="OpenAI error")
