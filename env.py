from pydantic import BaseModel

# Observation (what agent sees)
class Observation(BaseModel):
    request_text: str
    available_units: list
    step_count: int


# Action (what agent sends)
class Action(BaseModel):
    action_type: str   # "type" / "severity" / "resource"
    value: str


class EmergencyEnv:
    def __init__(self, task):
        self.task = task
        self.current_step = 0
        self.done = False

    def reset(self):
        self.current_step = 0
        self.done = False

        return Observation(
            request_text=self.task["input"]["request_text"],
            available_units=self.task["input"]["available_units"],
            step_count=self.current_step
        )

    def step(self, action: Action):
        self.current_step += 1
        reward = 0.0

        expected = self.task["expected"]
        text = self.task["input"]["request_text"].lower()

        # ---------------- STEP 1: TYPE ----------------
        if self.current_step == 1:
            if action.value == expected["type"]:
                reward = 0.3

        # ---------------- STEP 2: SEVERITY (context-aware) ----------------
        elif self.current_step == 2:

            if "critical" in text or "multiple" in text or "unconscious" in text:
                correct_severity = "critical"
            elif "injury" in text or "accident" in text:
                correct_severity = "high"
            else:
                correct_severity = expected["severity"]

            if action.value == correct_severity:
                reward = 0.3

        # ---------------- STEP 3: RESOURCE (dynamic decision) ----------------
        elif self.current_step == 3:
            units = self.task["input"]["available_units"]

            # find closest unit dynamically
            closest_unit = min(units, key=lambda x: x["distance"])["id"]

            if action.value == closest_unit:
                reward = 0.4

            self.done = True

        # ---------------- STEP PENALTY ----------------
        reward = reward - 0.01
        reward = max(0, reward)

        return (
            Observation(
                request_text=self.task["input"]["request_text"],
                available_units=self.task["input"]["available_units"],
                step_count=self.current_step
            ),
            reward,
            self.done,
            {}
        )

    def state(self):
        return {
            "step": self.current_step,
            "done": self.done
        }