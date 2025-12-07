import openai
from dotenv import load_dotenv
import streamlit as st

from todoaiagent.adapters.trello.client import TrelloClient
from todoaiagent.agents.langchain.tools import create_tasks_from_transcript_chain
from todoaiagent.config import Mistral, OpenAI, PromptSettings, LLMSettings

from todoaiagent.services.todo_service import TodoService


from todoaiagent.services.audio_to_text import audio_to_text

# load environment variables for dev purpose
load_dotenv()

trello_base_url = st.secrets["TRELLO_BASE_URL"]
id_list = st.secrets["ID_LIST"]
api_key = st.secrets["API_KEY"]
api_token = st.secrets["TOKEN"]
max_retries = int(st.secrets["MAX_RETRIES"])
timeout = int(st.secrets["TIMEOUT"])

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
if "locked" not in st.session_state:
    st.session_state.locked = False
if "api_key" not in st.session_state:
    st.session_state.api_key = None
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = ""


#settings = TodoAgentSettings(llm_mistral_model=os.getenv("LLM_MISTRAL_MODEL"), mistral_api_key=os.getenv("MISTRAL_API_KEY"))
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
example_prompts = {
    "meeting notes": """
Participants:
•	Sarah (Project Lead)
•	Michael (Tech Lead)
•	Julia (Marketing)
•	Jonas (Sales)
•	Lisa (Customer Success)

Sarah:\nAlright, let’s get started. First topic: our API rollout is slightly delayed. Michael, please prepare a short risk assessment by Wednesday, so we can decide whether we can keep the launch date.
Michael:\nGot it. And I need the final requirements from BetaCorp. Lisa, can you send those to me by tomorrow morning?
Lisa:\nSure. I just need to review them with their IT team first — I’ll handle that this afternoon.
Julia:\nThe landing page is almost ready, but I still need the product description from Mike’s documentation. Michael, can you send me the PDF by Friday?
Michael:\nYes, that works.
Jonas:\nFrom the sales side: We urgently need to update our pricing sheet. Julia, could you finish your new graphic by Thursday? Then I’ll take care of updating the PDF.
Julia:\nYes, Thursday is fine. I’ll send everything over by 5 PM.
Sarah:\nAnd Jonas, please schedule a short alignment call with BetaCorp for next week. Sometime between Tuesday and Thursday would be ideal.
Jonas:\nWill do. I’ll send them three time options today.
Sarah:\nPerfect. Last item: I need a short status update from everyone by Friday at noon — just two or three bullet points each.
        """,
    "weekly planer": """
Monday:\nI need to finalize the redesign for my client Studio Reimann. The mobile version is almost done, but the checkout flow still needs work. This should be completed by Tuesday evening. Then I want to prepare three social media posts for Instagram and LinkedIn — theme: “Behind the Scenes Redesign.” I want to get them done by the end of this week.\n
Tuesday:\nSend a follow-up to GreenLabs because they still haven’t approved the UI concept. I also need to create the invoice for Craft Brewery — deadline is Thursday.\n
Wednesday:\nI’m recording a new podcast episode in the afternoon — title: “How to Charge More as a Freelancer.” Before that, I need to finish the intro script, ideally by Wednesday morning.\n
Thursday:\nI plan to update my portfolio website. The case study layout needs improvement. It should definitely happen this week.\n
Friday:\nTax stuff. I have to organize my receipts and prepare the VAT pre-declaration — deadline is Monday next week. And I want to schedule one hour of learning for this week — probably watching a few advanced Figma prototyping tutorials.\n
        """
}


@st.dialog(title="Review created Tasks", width="medium", dismissible=False)
def show_created_tasks():
    task_container = st.container()
    analyzed_todos = st.session_state["analyzed_todos"].tasks

    with task_container:
        if len(analyzed_todos) == 0:
            st.write("No tasks to review.")
        else:
            for i, task in enumerate(analyzed_todos):
                cols = st.columns([4, 1])
                with cols[0]:
                    st.write(str(task))
                with cols[1]:
                    if st.button("Delete", key=f"delete_task_{i}"):
                        analyzed_todos.pop(i)
                        st.session_state["analyzed_todos"].tasks = analyzed_todos
                        st.rerun()

    st.divider()
    approve_col, decline_col = st.columns(2)
    with approve_col:
        if st.button("Approve", disabled=len(analyzed_todos) == 0):
            task_container.empty()
            st.session_state["process_state"] = "success"
            st.rerun()

    with decline_col:
        if st.button("Reject", type="primary"):
            task_container.empty()
            st.session_state["process_state"] = "rejected"
            st.rerun()

def set_api_key():
    if st.session_state.api_key_input:
        st.session_state.api_key = st.session_state.api_key_input
        st.session_state.locked = True

def unlock_fields():
    st.session_state.locked = False


with st.expander("Read Me:", expanded=True):
    st.markdown("""
            ##### Turn meeting transcript automatically with one click into real tasks📝🧠

            *Q: Why did you build this?*  
            A: Because after every meeting or workday, someone still has to sit down and extract the actual tasks. This is a waste of time, and it has to be done again after every meeting.
            
            *Q: So what does your showcase do?*  
            A: You give it a transcript, and the agent analyzes it, creates clean actionable to-dos, and saves them directly into a connected Project Management Tool.
            
            *Q: So it’s just summarizing text?*  
            A: No, it’s an autonomous agent. It decides what counts as a task and handles the full creation process for you.
            
            *Q: And what do I, the user, have to do?*  
            A: Nothing but pass in the transcript. The agent handles the rest.

            #### 📩 Interested in more?
            If you enjoyed this showcase and want to explore custom **AI solutions** for your business or project,  
            feel free to reach out:

            | [🌐 Visit my Website](https://lukashamm.dev) | [💬 Visit my LinkedIn Profile](https://www.linkedin.com/in/lukashamm-dev) | [👨‍💻 View my GitHub](https://github.com/hamluk) | [📧 Send me an Email](mailto:lukas@lukashamm.dev) |
            |---|---|---|---|
            """)

st.divider()

st.text_input(
        key="api_key_input",
        label="API Key:",
        type="password",
        disabled=st.session_state.locked)

if st.session_state.locked:
    st.button(
        key="unlock_button",
        label="Update API Key",
        on_click=unlock_fields)
else:
    st.button(
        key="set_model_api_key",
        label="Set API Key",
        on_click=set_api_key)


if not st.session_state.locked:
    st.warning("Please set your Openai API Key before starting.")
else:
    # --- input section ---
    with st.expander("Example transcripts:"):
        for key, prompt in example_prompts.items():
            if st.button(key, type="tertiary"):
                st.session_state.prompt_input = prompt

    st.subheader("Input")
    input_mode = st.selectbox(
    "Input Type", ["Text", "Voice"]
    )
    if input_mode == "Text":
        st.session_state["voice_file"] = None
        transkript = st.text_area(
            "Insert Transkript as copy",
            height=200,
            key="transkript",
            value=st.session_state.prompt_input
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
                mistral_model=st.secrets["LLM_MISTRAL_MODEL"],
                api_key=st.secrets["MISTRAL_API_KEY"]
            )
            openai_settings = OpenAI(
                temperature=float(st.secrets["TEMPERATURE"]),
                api_model=st.secrets["OPENAI_MODEL_NAME"],
                openai_api_key=st.session_state.api_key
            )
            prompt_settings = PromptSettings(
                system_prompt_file=st.secrets["SYSTEM_PROMPT_FILE"],
                prompt_dir=st.secrets["PROMPT_DIR"],
                max_prompt_tokens=4000
            )
            llm_settings = LLMSettings(
                provider=st.secrets["LLM_CHAT_PROVIDER"],
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

                create_response = None
                try:
                    create_response = create_tasks_from_transcript_chain(transkript_text, llm_settings)
                except openai.AuthenticationError:
                    st.error("Open AI API Key is invalid.")

                if not create_response or len(create_response.tasks) == 0:
                    st.error("No tasks could be extracted from the transcript. Please try again. Check your API Key or try a different transcript")
                else:
                    st.session_state["analyzed_todos"] = create_response
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