import streamlit as st
import requests
import json
from datetime import datetime

# --- App Setup ---
st.set_page_config(page_title="TaskNest - Daily Planner", layout="centered")
st.title("🪺 TaskNest - Your AI-Powered Daily Planner")
st.caption("Plan, Prioritize, and Achieve your daily goals with a little AI help.")

# --- Hugging Face Section ---
st.subheader("🔑 Hugging Face API")
hf_api_key = st.text_input("Enter your Hugging Face API Key", type="password")
hf_model = "HuggingFaceH4/zephyr-7b-beta"  # ✅ Confirmed to work with Hugging Face Inference API

def hf_generate(prompt):
    if not hf_api_key:
        return "⚠️ Please enter your API key first."

    headers = {
        "Authorization": f"Bearer {hf_api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,
            "do_sample": True,
            "temperature": 0.7
        }
    }

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{hf_model}",
            headers=headers,
            data=json.dumps(payload),
            timeout=60
        )

        if response.status_code != 200:
            return f"❌ API Error {response.status_code}: {response.text[:100]}"

        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        else:
            return f"❌ Unexpected response: {result}"

    except Exception as e:
        return f"❌ Request Failed: {str(e)}"

# --- Task State ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- Add Task ---
st.subheader("📋 Add a New Task")
with st.form("task_form"):
    task_desc = st.text_input("Task Description")
    task_time = st.time_input("Task Time")
    submit = st.form_submit_button("Add Task")

    if submit and task_desc:
        st.session_state.tasks.append({
            "task": task_desc,
            "time": task_time.strftime("%I:%M %p"),
            "status": "Pending"
        })
        st.success("✅ Task added!")

# --- Show Tasks ---
st.subheader("📆 Today's Tasks")
if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks):
        cols = st.columns([4, 2, 2])
        cols[0].markdown(f"**{task['task']}**")
        cols[1].write(task["time"])
        if cols[2].button("✅ Done", key=f"done_{i}"):
            st.session_state.tasks[i]["status"] = "Completed"

    if st.button("🧹 Clear Completed"):
        st.session_state.tasks = [t for t in st.session_state.tasks if t["status"] != "Completed"]
        st.success("Cleared completed tasks.")
else:
    st.info("No tasks yet. Add one above!")

# --- AI Summary ---
st.subheader("🧠 AI Summary of Your Day")
if st.button("Generate AI Summary"):
    if not hf_api_key:
        st.warning("Please enter your Hugging Face API key above.")
    else:
        tasks_text = "\n".join([f"- {t['task']} at {t['time']} ({t['status']})" for t in st.session_state.tasks])
        prompt = f"Summarize my day based on this task list:\n{tasks_text}\n\nGive it in 2-3 sentences."
        with st.spinner("Generating AI summary..."):
            summary = hf_generate(prompt)
            st.success("Here’s your day summary:")
            st.markdown(f"📝 _{summary.strip()}_")
