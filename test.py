from typing import List, Union, Generator, Iterator, Any
from schemas import OpenAIChatMessage
import requests
import json
from urllib.parse import urlparse
from pydantic import BaseModel
import os
import uuid

class N8NAPIClient:
    def __init__(self, N8N_API_BASE_URL: str) -> None:
        if not N8N_API_BASE_URL.startswith(('http://', 'https://')):
            N8N_API_BASE_URL = 'https://' + N8N_API_BASE_URL
        self.n8n_base_url = N8N_API_BASE_URL
     #   self.n8n_api_key = N8N_API_KEY

    def get_workflow(self, workflow_id: str) -> dict[str, Any]:
        return self.GET(path=f'/api/v1/workflows/{workflow_id}')

    def get_execution(self, workflow_id: str, execution_id: str):
        return self.GET(path=f'/api/v1/executions/{execution_id}')

    def trigger_webhook(self, webhook_id: str, input: str):
        return self.POST(path=f'/webhook-test/{webhook_id}', data=input)

    def chat(self, webhook: str, session_id: str, input: str):
        return self.POST(path=f'/webhook/{webhook}/chat', data=json.dumps({
            "action": "sendMessage",
            "sessionId": session_id,
            "chatInput": input,
        }))

    def POST(self, path: str, data: str) -> None:
        headers = {
            'content-type': 'application/json',
           # "x-n8n-api-key": self.n8n_api_key,
           # "cookie": f'n8n-auth={self.n8n_api_key}'
        }
        url = f'{self.n8n_base_url}{"//" if not path.startswith("/") else ""}{path}'

        # Validate URL
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError(f"Invalid URL: {url}. Make sure it includes a scheme (http:// or https://) and a domain.")

        resp = requests.post(url, headers=headers, data=data)
        resp.raise_for_status()
        return resp.json()

    def GET(self, path: str) -> None:
        headers = {
            #"x-n8n-api-key": self.n8n_api_key,
           # "cookie": f'n8n-auth={self.n8n_api_key}'
        }
        url = f'{self.n8n_base_url}{"//" if not path.startswith("/") else ""}{path}'

        # Validate URL
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError(f"Invalid URL: {url}. Make sure it includes a scheme (http:// or https://) and a domain.")

        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()


class Pipeline:
    class Values(BaseModel):
        N8N_API_BASE_URL: str = ""
    # N8N_API_KEY: str = ""
       # N8N_WORKFLOW_ID: str = ""

    def __init__(self):
        self.name = "AIM - N8n teste"
        self.values = self.Values(
            **{
                'N8N_API_BASE_URL': os.getenv("N8N_API_BASE_URL", "https://n8n.autointmind.com/webhook-test/get-test/"),
                #'N8N_API_KEY': os.getenv("N8N_API_KEY", "n8n_api_hj123712863kj123y781237612--------------"),
               # 'N8N_WORKFLOW_ID': os.getenv("N8N_WORKFLOW_ID", "Kasdfasdf121232"),
            }
        )
        self.n8n = N8NAPIClient(N8N_API_BASE_URL=self.values.N8N_API_BASE_URL)

    async def on_startup(self):
        print(f"on_startup:{self.name}")
        pass

    async def on_shutdown(self):
        print(f"on_shutdown:{self.name}")
        pass

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        session_id = str(uuid.uuid4())  
        
        # Trigger the n8n webhook and pass user input
        response = self.n8n.chat(webhook='https://n8n.autointmind.com/webhook-test/get-test', session_id=session_id, input=user_message)
        
        # Return the output from the webhook
        return response['output']
