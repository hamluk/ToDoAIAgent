
from dotenv import load_dotenv
import streamlit as st

from todoaiagent.adapters.trello.client import TrelloClient
from todoaiagent.agents.config import TodoAgentSettings
from todoaiagent.agents.langchain.tools import create_tasks_from_transcript_chain
from todoaiagent.config import Mistral, OpenAI, PromptSettings, LLMSettings

from todoaiagent.services.todo_service import TodoService

import os

from todoaiagent.services.audio_to_text import audio_to_text

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
if "human_feedback" not in st.session_state:
    st.session_state["human_feedback"] = None
if "submitted" not in st.session_state:
    st.session_state["submitted"] = False
if "analyzed_todos" not in st.session_state:
    st.session_state["analyzed_todos"] = None


settings = TodoAgentSettings(llm_mistral_model=os.getenv("LLM_MISTRAL_MODEL"), mistral_api_key=os.getenv("MISTRAL_API_KEY"))
# ---- Pydantic AI Agent approach ----
# agent = TodoAgent(settings=settings)
# pmt_client = TrelloClient(trello_base_url, api_key, api_token, max_retries, timeout)
# todoservice = TodoService(pmt_client)
# deps = TodoAgentDependencies(todoservice, id_list)

# trello_todos = None
# try:
#     trello_todos = agent.run(transkript_text, deps=deps)
# except Exception as e:
#     st.session_state["process_state"] = "error"
#     st.session_state["error_message"] = e
# ---- End Pydantic AI Agent approach ----

# ---- LangChain approach ----

pmt_client = TrelloClient(trello_base_url, api_key, api_token, max_retries, timeout)
todoservice = TodoService(pmt_client)


@st.dialog(title="Review created Tasks", width="medium", dismissible=False)
def show_created_tasks():
    task_container = st.container()

    with task_container:
        for task in st.session_state["analyzed_todos"].tasks:
            st.write(str(task))

    if st.button("Approve"):

        task_container.empty()
        st.session_state["process_state"] = "success"
        st.rerun()

    if st.button("Reject"):
        task_container.empty()
        st.session_state["process_state"] = "rejected"
        st.rerun()


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
    st.session_state["process_state"] = "idle"
    if input_mode == "Text" and not st.session_state["transkript"].strip():
        st.warning("Please copy transkript in text area above.")
    elif input_mode == "Voice" and st.session_state["voice_file"] is None:
        st.warning("Please uplaod transkript as audio file.")
    else:
        # --- process state ---
        st.subheader("Process Status")

        mistral_settings = Mistral(
            mistral_model=os.getenv("LLM_MISTRAL_MODEL"),
            api_key=os.getenv("MISTRAL_API_KEY")
        )
        openai_settings = OpenAI(
            temperature=float(os.getenv("TEMPERATURE")),
            api_model=os.getenv("OPENAI_MODEL_NAME"),
        )
        prompt_settings = PromptSettings(
            system_prompt_file=os.getenv("SYSTEM_PROMPT_FILE"),
            prompt_dir=os.getenv("PROMPT_DIR"),
            max_prompt_tokens=4000
        )
        llm_settings = LLMSettings(
            provider=os.getenv("LLM_CHAT_PROVIDER"),
            mistral=mistral_settings,
            openai=openai_settings,
            prompt=prompt_settings
        )


        if "todos" not in st.session_state:
            st.session_state["todos"] = []
        with st.spinner("AI Agent analyzes transkript and creates ToDos..."):

            transkript_text = ""
            if input_mode == "Text":
                transkript_text = st.session_state["transkript"]
            elif input_mode == "Voice":
                transkript_text = audio_to_text(st.session_state["voice_file"])

            st.session_state["analyzed_todos"] = create_tasks_from_transcript_chain(transkript_text, llm_settings)
            st.session_state["process_state"] = "approval"
            # ---- End LangChain approach ----
            st.rerun()


if st.session_state["process_state"] == "approval":
    show_created_tasks()


# ---- display created To-Dos and trello link ----
process_placeholder = st.empty()
if st.session_state["process_state"] == "success":
    st.subheader("Created To-Dos")

    trello_todos = todoservice.createTodo(st.session_state["analyzed_todos"].tasks, id_list)

    if trello_todos is not None:
        st.session_state["todos"] = trello_todos

        for todo in st.session_state["todos"]:
            st.markdown(f"{todo}")

        st.markdown("\n🔗 [View ToDos in trello](https://trello.com/b/0tRcSjHf/todo-ai-agent-showcase) ")
        process_placeholder.info("✅ Transkript processed and todos created.")
    st.session_state["analyzed_todos"] = None
elif st.session_state["process_state"] == "rejected":
    process_placeholder.info("⚠ To-Dos rejected by human. No To-Dos were created.")
    st.session_state["analyzed_todos"] = None