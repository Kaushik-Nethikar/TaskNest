# 🪺 TaskNest – AI-Powered Daily Planner

**TaskNest** is a simple, intelligent, and extendable daily planner built with **Streamlit**. It lets users manage tasks and generate smart AI summaries using the **Hugging Face Inference API**.

---

## 🔗 Try It Live

👉 [Click here to open TaskNest](https://tasknest1.streamlit.app/)

> Replace the above link with your actual Streamlit Cloud URL after deployment.

---

## 🚀 Features

- ✅ Add, manage, and complete tasks
- 🧠 Generate AI-based summaries of your day
- 🔐 Enter your own Hugging Face API key securely
- 💡 Clean and responsive interface

---

## 🧩 Tech Stack

- Python 3.9+
- Streamlit
- Hugging Face Inference API
- requests

---

## 🔑 Hugging Face API Key Setup

1. Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click **"New token"**
3. Choose **Role: Read**
4. Paste the token into the app when prompted

---

## ✅ Model Used

```python
hf_model = "HuggingFaceH4/zephyr-7b-beta"
