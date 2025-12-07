# 🧠 **ToDoAiAgent**

**Turn meeting transcripts automatically into real tasks with one click**

---

## 🚀 Overview

Ever walked out of a meeting or finished a workday only to realize you still have to put everything into actionable tasks?

That’s exactly the problem this ToDoAiAgent tackles.

The goal is to eliminate the time-consuming process of manually reviewing conversations, extracting todos, and updating project management tools. The AI agent therefore that takes any transcript, from a team meeting, a personal weekly plan, or even a voice recording and automatically turns it into structured to-dos. No summaries you need to rewrite, no manual copying into your project board. 

The agent analyzes the transcript, extracts tasks with priorities and due dates, and **directly creates them inside your project management system**. In this demo, it seamlessly populates a Trello board you’ve set up beforehand. All logic lives inside the agent’s system prompt, meaning you simply hand over a transcript, and it knows exactly what to do.

A Streamlit-powered demo makes the experience accessible, interactive and easy to test without touching any code.

> Note: A personal OpenAI API key is required to run the demo.
> 

---

## 🌐 Live Demo

*Coming soon — link will be added here once deployed.*

---

## 🎥 Screenshots

*Add screenshots or a GIF here (UI, transcript example, created Trello card).*

---

## ✨ Features

- **Turns transcripts into real tasks**
    
    Detects todos, deadlines, priorities and labels from any conversation or weekly planning text.
    
- **Team meetings & solo planning supported**
    
    Works equally well with multi-person discussions and single-person weekly plans.
    
- **Direct Trello integration**
    
    Tasks are formatted and pushed into your selected Trello list via API.
    
- **Deterministic LLM behavior**
    
    Uses a robust system prompt with strict JSON schema validation for predictable outputs.
    
- **Streamlit user interface**
    
    Paste a transcript, review the detected todos and confirm Trello creation.
    
- **Poetry-based project structure**
    
    Clean dependency management and reproducible environments.
    

---

## 🏁 Quick Start

### **Requirements**

- Python **3.13.4**
- Poetry installed
- Your own **OpenAI API key**
- A Trello account and API credentials

---

### 🔧 **Installation**

```bash
poetry install
```

---

### ▶️ **Run the Streamlit App**

```bash
poetry run streamlit run src/todoaiagent/streamlit/app.py
```

---

### 🔐 Environment Variables

Create a `.env` file in the project root with:

```
TRELLO_BASE_URL=
ID_LIST=
API_KEY=
TOKEN=
MAX_RETRIES=
TIMEOUT=

LLM_CHAT_PROVIDER="OPENAI"

SYSTEM_PROMPT_FILE=
PROMPT_DIR=
MAX_PROMPT_TOKENS=

TEMPERATURE=
OPENAI_MODEL_NAME=
```

> Important:
> 
> - You must provide your own **OpenAI API key**
> - LLM usage generates API costs depending on your model and volume
> - Avoid uploading transcripts containing sensitive personal data
> - This showcase is not intended for production use without review

---

## 🏗 Architecture

### **High-level flow**

```
Streamlit UI → LangChain Agent → System Prompt + LLM →
→ Structured Todos (Pydantic) → Trello Adapter → Trello API
```

### **Libraries used**

- LangChain
- httpx
- speechrecognition
- langchain-openai
- pydantic
- streamlit

---

## 📘 User Guide (How to Demo)

1. Paste or upload a transcript into the Streamlit app
2. Click “Generate Tasks”
3. Review the extracted todos
4. Confirm creation
5. The tasks appear instantly in your Trello board

Perfect for demos of:

- AI automation
- Agentic workflows
- Productivity tooling
- LLM integrations

---

## 🔒 Privacy & Costs Notice

- This demo processes the full transcript using OpenAI’s API.
- Do **not** upload transcripts containing personal, confidential or sensitive data.
- All API calls incur costs based on your OpenAI model settings — keep your key private.
- No data is stored by the demo; processing happens in memory during your session.

---

## 📍 Roadmap

- Voice input support (speech → transcript → todos)
- Support for additional task managers (Todoist, Notion, ClickUp)
- Multi-step agent behavior (analyze → plan → create)
- Better error handling and retry logic
- Example prompt pack for different industries

---

## 👤 Author

**Lukas Hamm**

🔗 [https://www.lukashamm.dev](https://www.lukashamm.dev/)

📧 lukas@lukashamm.dev

💼 https://www.linkedin.com/in/lukashamm-dev

---

## 🏷 GitHub Topics

`ai-agent` · `streamlit` · `langchain` · `todo-automation` · `trello-api` · `llm` · `pydantic` · `productivity-tools` · `meeting-automation`