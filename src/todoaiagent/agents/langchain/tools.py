from datetime import date, timedelta

from langchain_core.output_parsers import PydanticOutputParser

from todoaiagent.agents.factorys.llm_factory import get_llm_chat_provider
from todoaiagent.agents.langchain.models import TrelloTaskList
from langchain_core.prompts.chat import ChatPromptTemplate

from todoaiagent.agents.prompts.loader import build_todo_chat_messages
from todoaiagent.config import LLMSettings


def create_tasks_from_transcript_chain(transcript: str, llm_settings: LLMSettings) -> TrelloTaskList:
    """
    Creates tasks from a given transcript
    Invokes the create-task-chain to analyze a given transcript and create tasks form it.

    Args:
        transcript (str): the transcript as string to analyze and create tasks from
        llm_settings: llm specific settings

    Returns:
        TrelloTaskList: A list of TrelloTask objects

    """
    today = date.today()
    monday = today - timedelta(days=today.weekday())

    llm_chat_provider = get_llm_chat_provider(llm_settings)

    parser = PydanticOutputParser(pydantic_object=TrelloTaskList)

    prompt_from_yaml = build_todo_chat_messages(settings=llm_settings)

    chat_prompt = ChatPromptTemplate(prompt_from_yaml)

    chain = chat_prompt | llm_chat_provider | parser

    # Todo: Find a way to put all of this directly into the prompt building function
    llm_result = chain.invoke({
        "today": monday.isoformat(),
        "transcript": transcript,
        "format_instructions": parser.get_format_instructions()
    })

    todos = TrelloTaskList(tasks=llm_result.tasks)

    return todos

