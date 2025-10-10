import time
from typing import Sequence

import httpx
from todoaiagent.adapters.trello.mapper import map_todos_to_trello_cards
from todoaiagent.adapters.trello.models import TrelloCard
from todoaiagent.domain.models import Todo
from todoaiagent.domain.ports import IProjectManagementClient
from todoaiagent.rest_interface.http import create_httpx_client

class TrelloClient(IProjectManagementClient):
    def __init__(self, base_url: str, api_key: str, api_token: str, max_retries: int = 3, timeout: int = 4):
        self.base_url = base_url
        self.max_retries = max_retries
        self.timeout = timeout
        self.auth = {"key": api_key, "token": api_token}
        self.http_client = create_httpx_client(base_url=base_url, timeout=timeout)
        self.label_map = {
            "private": "68b01257013ede507ac29309",
            "office": "68b01257013ede507ac2930e",
            "customer": "68b01257013ede507ac2930c"
        }

    def create_tasks(self, todo_list: Sequence[Todo], idList:str, with_retry: bool = False) -> list[TrelloCard]:
        trello_cards = map_todos_to_trello_cards(todo_list, idList, self.label_map)

        url = f"{self.base_url}/cards"

        headers = {
            "Accept": "application/json"
            }

        for card in trello_cards:     
            query = {
                "idList": card.idList,
                "name": card.name,
                "desc": card.desc,
                "due": card.due,
            }
          
            params = {**query, **self.auth}
            try:
                self._request(headers=headers, request_method="POST", url=url, params=params, data=None, retry_enabled=with_retry)
            except Exception as e:
                raise

        return trello_cards
            

    def _request(self, headers: dict, request_method: str, url: str, params: dict, data, retry_enabled: bool = False):
        retries = 0

        while True:
            try:
                response = self.http_client.request(method=request_method, url=url, params=params, data=data)

                # retry strategie for the request
                if retry_enabled:
                    if response.status_code in (429, 503) and retries < self.max_retries:
                        delay = min(2 ** retries, 8)
                        print(f"Retrying {url} (atempt {retries} / {self.max_retries}) afer {delay}s...")
                        time.sleep(delay)
                        retries += 1
                        continue

                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as e:
                if retry_enabled:
                    if retries >= self.max_retries:
                        print(f"Error on HTTP request with status {e}") 
                    time.sleep(2 ** retries)
                    retries += 1
                else:
                    print(f"Error on HTTP request with status {e}") 
                    raise
            except httpx.RequestError as e:
                # retry strategie for the request
                if retry_enabled:
                    if retries >= self.max_retries:
                        print(f"Error on HTTP request, max retries exceeded! {e}")
                    time.sleep(2 ** retries)
                    retries += 1
                else:
                    print(f"Error on HTTP request! Check request or try again later! {e}")
                    raise
