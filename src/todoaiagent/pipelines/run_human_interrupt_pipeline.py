import os

from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

from todoaiagent.adapters.trello.client import TrelloClient
from todoaiagent.agents.prompts.user import prompt
from todoaiagent.pipelines.create_todos_pipeline import create_todos_pipeline_graph
from todoaiagent.services.todo_service import TodoService

if __name__ == "__main__":
    load_dotenv()

    # config
    checkpointer = MemorySaver()
    config = {"configurable": {"thread_id": "thread-1"}}

    # initial state values
    initial_state = {
        "transkript": prompt,  # original transkript
        "todos": None,
        "human_feedback": None,
        "status": "pending",
    }

    graph = create_todos_pipeline_graph(checkpointer)

    interrupted_pipeline = graph.invoke(initial_state, config=config)

    interrupt_payload = interrupted_pipeline.get("__interrupt__")

    print("!! Human Feedback Required !!")
    print(interrupt_payload[0].value["question"])
    for todo in interrupt_payload[0].value["details"].tasks:
        print(f"* {todo}")

    human_feedback = input("\nDo you accept the created todos? Type 'y' to continue, type 'n' to abort:")
    proceed = False
    if human_feedback == "y":
        proceed = True

    final_pipeline = graph.invoke(Command(resume=proceed), config=config)

    if final_pipeline.get("status") == "rejected":
        print("Creation of todos rejected by human")

    else:
        trello_base_url = os.getenv("TRELLO_BASE_URL")
        id_list = os.getenv("ID_LIST")
        api_key = os.getenv("API_KEY")
        api_token = os.getenv("TOKEN")
        max_retries = int(os.getenv("MAX_RETRIES"))
        timeout = int(os.getenv("TIMEOUT"))

        pmt_client = TrelloClient(trello_base_url, api_key, api_token, max_retries, timeout)
        todoservice = TodoService(pmt_client)

        trello_todos = todoservice.createTodo(final_pipeline.get("todos").tasks, id_list)

        print("Creation of todos accepted by human")

    print("Process ended!")
