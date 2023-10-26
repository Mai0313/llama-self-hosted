from fastapi import FastAPI
from pydantic import BaseModel
import datetime

from src.model import generate_response


class UserInput(BaseModel):
    user_input: str
    time_input: str

app = FastAPI()

@app.post("/llama")
async def handle_data(item: UserInput):
    user_input = item.user_input
    time_input = item.time_input
    response = generate_response(user_input)
    process_time = datetime.datetime.now() - datetime.datetime.strptime(time_input, "%Y-%m-%d %H:%M:%S")
    return {"status": "Success", "result": response, "process_time": process_time}

# uvicorn api:app --host 0.0.0.0 --port 7787 --reload
