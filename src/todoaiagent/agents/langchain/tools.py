from langchain_mistralai import ChatMistralAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from datetime import date

import os

from todoaiagent.agents.langchain.models import TrelloTaskList

def create_tasks_from_transkript_chain(transkript: str) -> TrelloTaskList:
    """Creates tasks from a given transkript

    Invokes the create-task-chain to analyze a given transkript and create tasks form it.

    Args:
        transkript (str): the transkript as string to analyze and create tasks from

    Returns:
        TrelloTaskList: A list of TrelloTask objects

    """
    today = date.today()

    chat_prompt = ChatPromptTemplate([
        ("system", """You are a helpful assistant that analyses a given transkript and creates todo tasks from it.
         For finding the due date use today's date {today} as a reference.
         Put the extracted information for the task into following format: {format_instruction}
         """),
        ("human", "Create task for: {transkript}")
    ])
    
    llm_chat = ChatMistralAI(model_name=os.getenv("LLM_MISTRAL_MODEL"), api_key=os.getenv("MISTRAL_API_KEY"))

    llm_chat.with_structured_output(TrelloTaskList)
    
    parser = JsonOutputParser(pydantic_object=TrelloTaskList)

    chain = chat_prompt | llm_chat | parser

    todos = TrelloTaskList(tasks=chain.invoke({
        "today": today.isoformat(),
        "transkript": transkript,
        "format_instruction": parser.get_format_instructions()
        }).get("tasks"))

    return todos

