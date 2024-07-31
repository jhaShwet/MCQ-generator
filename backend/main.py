from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
import requests
from langchain_community.tools import DuckDuckGoSearchRun

app = FastAPI()

# File-based storage path
DB_FILE = 'mcq_data.json'

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            print(f"Error loading JSON data: {e}")
            return {}
    return {}

def save_data(data):
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error saving JSON data: {e}")

questions_db = load_data()

def get_next_id(data):
    numeric_keys = [int(key) for key in data.keys() if key.isdigit()]
    return max(numeric_keys, default=0) + 1

next_id = get_next_id(questions_db)

class Query(BaseModel):
    topic: str

class UserAnswer(BaseModel):
    question_id: int
    answer: str

search = DuckDuckGoSearchRun()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the MCQ application API"}

@app.post("/generate/")
async def generate_content(query: Query):
    ai21_api_key = os.getenv('AI21_API_KEY')
    if not ai21_api_key:
        raise HTTPException(status_code=500, detail="AI21 API key not set. Please set the environment variable 'AI21_API_KEY'.")

    url = "https://api.ai21.com/studio/v1/j2-large/complete"
    headers = {
        "Authorization": f"Bearer {ai21_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": f"Generate a multiple-choice question on the topic: {query.topic}",
        "numResults": 1,
        "maxTokens": 100
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        print("Parsed JSON result:", result)

        completions = result.get('completions', [])
        if not completions:
            raise HTTPException(status_code=500, detail="No completions found in response")

        text = completions[0].get('data', {}).get('text', '').strip()
        if not text:
            raise HTTPException(status_code=500, detail="Generated text is empty")

        lines = text.split('\n')
        if len(lines) < 2:
            raise HTTPException(status_code=500, detail="Invalid response format from AI21")

        question = lines[0].strip()
        options = [line.strip() for line in lines[1:] if line.strip()]

        global next_id
        question_id = next_id
        questions_db[question_id] = {
            'topic': query.topic,
            'question': question,
            'options': options,
            'user_answer': ''
        }
        next_id += 1
        save_data(questions_db)

        return {"question": question, "options": options, "id": question_id}
    except requests.RequestException as e:
        print(f"Request error: {e}")
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
        raise HTTPException(status_code=500, detail=f"Value error: {e}")
    except KeyError as e:
        print(f"Key error: {e}")
        raise HTTPException(status_code=500, detail=f"Key error: {e}")

@app.post("/search/")
async def search_content(query: Query):
    try:
        results = search.invoke(query.topic)
        return {"results": results}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@app.post("/submit_answer/")
async def submit_answer(user_answer: UserAnswer):
    if user_answer.question_id in questions_db:
        questions_db[user_answer.question_id]['user_answer'] = user_answer.answer
        save_data(questions_db)
        return {"detail": "Answer submitted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Question not found")
