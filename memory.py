from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from datetime import datetime
import os
import streamlit as st


llm=None
NEBIUS_API_KEY =st.secrets.get("NEBIUS_API_KEY")
NEBIUS_BASE_URL= "https://api.studio.nebius.com/v1/"
NEBIUS_MODEL_NAME=st.secrets.get("NEBIUS_MODEL_NAME")

missing_configs = []
if not NEBIUS_API_KEY:
    missing_configs.append("NEBIUS_API_KEY")
if not NEBIUS_BASE_URL:
    missing_configs.append("base url missing")
if not NEBIUS_MODEL_NAME:
    missing_configs.append("base model name is missing")

if missing_configs:
    st.error(f"Nebius configuration missing: {', '.join(missing_configs)}.")
else:
    try:
        llm = ChatOpenAI(
            model=NEBIUS_MODEL_NAME,
            api_key=NEBIUS_API_KEY,
            base_url=NEBIUS_BASE_URL,
            temperature=0.3,
            max_tokens=200
        )
    except Exception as e:
        st.error(f"failed to initialize Nebius model: {e}")
        llm = None

user_sessions = {}

def get_conversation(username):
    if username not in user_sessions:
        memory = ConversationBufferMemory(return_messages=True)
        conversation = ConversationChain(llm=llm, memory=memory)
        user_sessions[username] = conversation
    return user_sessions[username]

def chat_with_bot(username, user_input):
    conv = get_conversation(username)
    response = conv.predict(input=user_input)
    log_diary(username, user_input, response)
    return response

def log_diary(username, user_input, bot_response):
    prompt = f"""
You are a chatbot writing your personal diary. Describe this interaction in first person:

User: {user_input}
You: {bot_response}

Make it sound like you're a curious AI learning about your friend.
"""
    diary_entry = llm.predict(prompt)
    save_diary_entry(username, diary_entry)

def save_diary_entry(username, entry):
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M")
    diary_dir = os.path.join("diaries", username)
    os.makedirs(diary_dir, exist_ok=True)

    file_path = os.path.join(diary_dir, f"{date}.txt")
    with open(file_path, "a") as f:
        f.write(f"\n--- Entry at {time} ---\n{entry}\n")
