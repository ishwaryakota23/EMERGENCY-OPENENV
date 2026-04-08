from env import EmergencyEnv, Action
from tasks import tasks

# -------- LOGGING FUNCTIONS --------
def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}")

def log_step(step, action, reward, done):
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null")

def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}")


# -------- SIMPLE AGENT --------
# -------- IMPROVED AGENT --------
def simple_agent(step, obs):
    text = obs.request_text.lower()
    units = obs.available_units

    # Step 1 → classify type (keyword reasoning)
    if step == 1:
        if any(word in text for word in ["fire", "smoke", "burn"]):
            predicted_type = "fire"
        elif any(word in text for word in ["accident", "injury", "crash"]):
            predicted_type = "medical"
        elif any(word in text for word in ["unconscious", "breathing"]):
            predicted_type = "medical"
        else:
            predicted_type = "medical"  # default fallback

        return Action(action_type="type", value=predicted_type)

    # Step 2 → determine severity (more nuanced)
    elif step == 2:
        if any(word in text for word in ["unconscious", "not breathing"]):
            severity = "critical"
        elif any(word in text for word in ["injury", "accident"]):
            severity = "high"
        elif any(word in text for word in ["delay", "late"]):
            severity = "medium"
        else:
            severity = "low"

        return Action(action_type="severity", value=severity)

    # Step 3 → resource allocation (decision-based)
    elif step == 3:
        # sort units by distance
        sorted_units = sorted(units, key=lambda x: x["distance"])

        # simulate decision: pick best available
        selected_unit = sorted_units[0]["id"]

        return Action(action_type="resource", value=selected_unit)

def run():
    total_scores = []

    for task in tasks:
        env = EmergencyEnv(task)

        log_start(task["name"], "emergency_env", "rule-based-agent")

        obs = env.reset()
        rewards = []
        steps = 0

        for step in range(1, 4):
            action = simple_agent(step, obs)

            obs, reward, done, _ = env.step(action)

            rewards.append(reward)
            steps = step

            log_step(step, action.value, reward, done)

            if done:
                break

        total_reward = sum(rewards)
        score = min(max(total_reward, 0), 1)
        success = score > 0.5

        log_end(success, steps, score, rewards)

        total_scores.append(score)

    final_score = sum(total_scores) / len(total_scores)
    print(f"\nFinal Average Score: {final_score:.2f}")


if __name__ == "__main__":
    run()