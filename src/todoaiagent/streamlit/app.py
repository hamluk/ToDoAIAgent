from dotenv import load_dotenv
import streamlit as st
from typing import List

from todoaiagent.adapters.trello.client import TrelloClient
from todoaiagent.agents.config import TodoAgentSettings
from todoaiagent.agents.models.dependencies import TodoAgentDependencies
from todoaiagent.agents.todo_agent import TodoAgent
from todoaiagent.domain.models import Todo

import os

from todoaiagent.services.audio_to_text import audio_to_text
from todoaiagent.services.todo_service import TodoService

# load environment variables for dev purpose
load_dotenv()

trello_base_url = os.getenv("TRELLO_BASE_URL")
id_list = os.getenv("ID_LIST")
api_key = os.getenv("API_KEY")
api_token = os.getenv("TOKEN")
max_retries = int(os.getenv("MAX_RETRIES"))
timeout = int(os.getenv("TIMEOUT"))

st.set_page_config(page_title="To-Do AI Agent Showcase", layout="centered")


st.title("📝 To-Do AI Agent Showcase")


# initialize session states
if "todos" not in st.session_state:
    st.session_state["todos"] = []
if "transkript" not in st.session_state:
    st.session_state["transkript"] = ""
if "voice_file" not in st.session_state:
    st.session_state["voice_file"] = None
if "process_state" not in st.session_state:
    st.session_state["process_state"] = "idle"
if "error_message" not in st.session_state:
    st.session_state["error_message"] = ""


settings = TodoAgentSettings(llm_mistral_model=os.getenv("LLM_MISTRAL_MODEL"), mistral_api_key=os.getenv("MISTRAL_API_KEY"))


# --- input section ---
st.subheader("Input")


input_mode = st.selectbox(
"Input Type", ["Text", "Voice"]
)


if input_mode == "Text":
    st.session_state["voice_file"] = None
    transkript = st.text_area(
    "Insert Transkript as copy",
    height=200,
    key="transkript"
    )
elif input_mode == "Voice":
    st.session_state["transkript"] = ""
    voice_file = st.file_uploader("Uplaod Audio file", type=["mp3", "wav", "m4a"], key="voice_file")


submit_btn = st.button("Submit")

if submit_btn:
    if input_mode == "Text" and not st.session_state["transkript"].strip():
        st.warning("Please copy transkript in text area above.")
    elif input_mode == "Voice" and st.session_state["voice_file"] is None:
        st.warning("Please uplaod transkript as audio file.")
    else:
        # --- process state ---
        st.subheader("Process Status")
        process_placeholder = st.empty()

        if "todos" not in st.session_state:
            st.session_state["todos"] = []
        with st.spinner("AI Agent analyzes transkript and creates ToDos..."):

            transkript_text = ""
            if input_mode == "Text":
                transkript_text = st.session_state["transkript"]
            elif input_mode == "Voice":
                transkript_text = audio_to_text(st.session_state["voice_file"])

            agent = TodoAgent(settings=settings)
            pmt_client = TrelloClient(trello_base_url, api_key, api_token, max_retries, timeout)
            todoservice = TodoService(pmt_client)
            deps = TodoAgentDependencies(todoservice, id_list)
            
            trello_todos = None
            try:
                trello_todos = agent.run(transkript_text, deps=deps)
            except Exception as e:
                st.session_state["process_state"] = "error"
                st.session_state["error_message"] = e

            if trello_todos is not None:
                st.session_state["todos"] = trello_todos

        if st.session_state["process_state"] != "error":
            process_placeholder.info("✅ Transkript processed and todos created.")
        else:
            process_placeholder.error(f"❌ Error creating ToDos: {st.session_state["error_message"]}")

# --- display created To-Dos and trello link ---
if st.session_state["todos"]:
    st.subheader("Created To-Dos")

    for todo in st.session_state["todos"]:
        st.markdown(f"{todo}")

    st.markdown("\n🔗 [View ToDos in trello](https://trello.com/b/0tRcSjHf/todo-ai-agent-showcase) ")