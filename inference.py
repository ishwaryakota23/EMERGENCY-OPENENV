import os

API_BASE_URL = os.getenv("API_BASE_URL", "dummy")
MODEL_NAME = os.getenv("MODEL_NAME", "dummy")
HF_TOKEN = os.getenv("HF_TOKEN")

from fastapi import FastAPI
from env import EmergencyEnv, Action
from tasks import tasks

app = FastAPI()

env_instance = None


@app.post("/openenv/reset")
def reset():
    global env_instance

    task = tasks[0]   # you can rotate later, not needed now
    env_instance = EmergencyEnv(task)

    obs = env_instance.reset()

    return {
        "observation": obs.request_text,
        "available_units": obs.available_units
    }


@app.post("/openenv/step")
def step(action: dict):
    global env_instance

    action_obj = Action(**action)

    obs, reward, done, _ = env_instance.step(action_obj)

    return {
        "observation": obs.request_text,
        "reward": reward,
        "done": done,
        "available_units": obs.available_units
    }
