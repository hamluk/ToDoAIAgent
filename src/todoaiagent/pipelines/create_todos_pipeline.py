from typing import TypedDict, Literal, Annotated

from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from langgraph.types import interrupt

from todoaiagent.agents.langchain.models import TrelloTaskList
from todoaiagent.streamlit.app import trello_todos


def update_status(old: Literal[str], new: str) -> str:
    if old == "rejected":
        return old

    return new


class TaskState(TypedDict):
    transkript: str # original transkript
    todos: TrelloTaskList | None
    human_feedback: bool | None
    status: Annotated[
        Literal["pending", "rejected", "approved"],
        update_status
    ]


def create_tasks_from_tanskript(state: TaskState):

    return {"todos": trello_todos}


def get_human_feedback(state: TaskState):
    feedback = interrupt({
        "question": "Please check the following task before proceeding"
                    " with the creation in the Project Management Tool.",
        "details": state["todos"]
    })

    return {"human_feedback": feedback}


def router(state: TaskState):
    if state.get("human_feedback"):
        return "approved"

    return "rejected"


def approve(state: TaskState):
    return {"status": "approved"}


def cancel(state: TaskState):
    return {"status": "rejected"}


def create_todos_pipeline_graph(checkpointer: MemorySaver):
    graph_builder = StateGraph(TaskState)

    graph_builder.add_node("create_tasks", create_tasks_from_tanskript)
    graph_builder.add_node("human_feedback", get_human_feedback)
    graph_builder.add_node("router", router)
    graph_builder.add_node("approved", approve)
    graph_builder.add_node("canceled", cancel)

    graph_builder.add_edge(START, "create_tasks")
    graph_builder.add_edge("create_tasks", "human_feedback")
    # graph_builder.add_edge("human_feedback", "router")
    graph_builder.add_conditional_edges("human_feedback", router, {
        "approved": "approved",
        "rejected": "canceled"
    })
    graph_builder.add_edge("approved", END)
    graph_builder.add_edge("canceled", END)

    return graph_builder.compile(checkpointer=checkpointer)
