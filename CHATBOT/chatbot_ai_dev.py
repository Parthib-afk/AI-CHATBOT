from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from prompt import SYSTEM_PROMPT

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Request body format
class ChatRequest(BaseModel):
    message: str
    history: list[str] = []
@app.post("/ask-ai")
def ask_ai(data: ChatRequest):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    # Add previous chat context
    for msg in data.history[-5:]:
        messages.append({"role": "user", "content": msg})

    # Current user message
    messages.append({"role": "user", "content": data.message})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.3
    )

    reply = response.choices[0].message.content
    return {"reply": reply}