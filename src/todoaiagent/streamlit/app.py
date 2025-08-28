import streamlit as st
from typing import List, Dict

st.set_page_config(page_title="To-Do AI Agent Showcase", layout="centered")


st.title("📝 To-Do AI Agent Showcase")


# initialize session states
if "todos" not in st.session_state:
    st.session_state["todos"] = []
if "transkript" not in st.session_state:
    st.session_state["transkript"] = ""
if "voice_file" not in st.session_state:
    st.session_state["voice_file"] = None


# --- input section ---
st.subheader("Input")


input_mode = st.selectbox(
"Input Type", ["Voice", "Text"]
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

# --- process state ---
st.subheader("Process Status")
process_placeholder = st.empty()

# --- output section ---
st.subheader("Created To-Dos")
if "todos" not in st.session_state:
    st.session_state["todos"] = []

if submit_btn:
    if input_mode == "Text" and not st.session_state["transkript"].strip():
        st.warning("Please copy transkript in text area above.")
    elif input_mode == "Voice" and st.session_state["voice_file"] is None:
        st.warning("Please uplaod transkript as audio file.")
    else:
        with st.spinner("AI Agent analyzes transkript and creates ToDos..."):
            # TODO: add call to python backen

            # store result in todos
            todos: List[Dict] = [
                {"title": "Prepare Meeting Follow-up", "priority": "High", "due": "2025-09-01"},
                {"title": "Contact Customer XY", "priority": "Medium", "due": "2025-09-03"},
            ]
            st.session_state["todos"] = todos

        process_placeholder.info("✅ Transkript processed, following To-Dos got created.")

# --- display created To-Dos and trello link ---
if st.session_state["todos"]:
    for todo in st.session_state["todos"]:
        st.markdown(f"- **{todo['title']}**  | Priorität: {todo['priority']} | Fällig: {todo['due']}")

    st.markdown("\n🔗 [View ToDos in trello](https://trello.com/) ")