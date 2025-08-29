import httpx

def create_httpx_client(timeout: float, base_url: str) ->httpx.Client:
    """ creates httpx client with  """
    def log_request(request: httpx.Request):
        print(f"Request event hook: {request.method} {request.url} - Waiting for response")

    def log_response(response: httpx.Response):
        request = response.request
        print(f"Resonse event hook: {request.method} {request.url} - Status {response.status_code}")

    return httpx.Client(timeout=timeout, base_url=base_url)
    