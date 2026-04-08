import os
from fastapi import FastAPI, Request
from env import EmergencyEnv, Action
from tasks import tasks

API_BASE_URL = os.getenv("API_BASE_URL", "dummy")
MODEL_NAME = os.getenv("MODEL_NAME", "dummy")
HF_TOKEN = os.getenv("HF_TOKEN")



app = FastAPI()

env_instance = None

@app.get("/")
def home():
    return {"message": "API is working"}

@app.post("/openenv/reset")
def reset():
    global env_instance

    task = tasks[0]
    env_instance = EmergencyEnv(task)

    obs = env_instance.reset()

    return {
        "observation": obs.request_text,
        "available_units": obs.available_units
    }


@app.post("/openenv/step")
async def step(request: Request):
    global env_instance

    data = await request.json()
    action_obj = Action(**data)

    obs, reward, done, _ = env_instance.step(action_obj)

    return {
        "observation": obs.request_text,
        "reward": reward,
        "done": done,
        "available_units": obs.available_units
    }
