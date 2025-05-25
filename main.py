from openai import OpenAI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import SupabaseDB
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Load from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

class Query(BaseModel):
    input_text: str

@app.post("/ask")
async def ask_question(query: Query):
    try:
        #1. Call OpenAI API
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4"
            messages=[{"role": "system", "content": "You're a helpful assistant to generate practice question in JSON format list key 'questions' and  item has key like 'question' and 'answer'"},
                      {"role": "user", "content": query.input_text}],
        )

        content = response.choices[0].message.content
        json_data = json.loads(content)
        
        # 2. Save to Supabase
        data = {
            "question": query.input_text,
            "answer": json_data
        }
        db = SupabaseDB()
        db.save_to_supabase(data) 

        # 3. Return the result
        #json_data = {"questions":[{"question":"What is the capital of France?","answer":"Paris"},{"question":"Who wrote the play 'Romeo and Juliet'?","answer":"William Shakespeare"}]} #result.get("questions", [])
        return {"response": json_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ping")
async def health_check():
    return {"status": "ok"}
    