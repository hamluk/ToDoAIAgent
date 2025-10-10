from todoaiagent.adapters.trello.models import TrelloCard
from todoaiagent.domain.models import Todo

def map_todos_to_trello_cards(todos: list[Todo], idList: str, label_map: dict[str, str]) -> list[TrelloCard]:
    trello_cards = []
    for todo in todos:
        trello_name = todo.title
        trello_desc = todo.description
        trello_due = todo.due_trello_format
        trello_labels = []

        trello_cards.append(TrelloCard(
                                idList=idList,
                                name=trello_name, 
                                desc=trello_desc, 
                                due=trello_due, 
                                idLabels=trello_labels))
    
    return trello_cards

