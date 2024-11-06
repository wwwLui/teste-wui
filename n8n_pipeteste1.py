from typing import List, Union, Generator, Iterator, Optional
import requests
import json
import time

class Pipeline:
    def __init__(self):
        self.name = "AIM - N8N Agent Pipeline2"
        self.api_url = "https://n8n.autointmind.com/webhook-test/62f78f96-6cae-4cfd-985d-27d2da8fd8b5"  # Set correct hostname
        self.verify_ssl = True
        self.debug = False

    async def on_startup(self):
        print(f"on_startup: {__name__}")

    async def on_shutdown(self):
        print(f"on_shutdown: {__name__}")

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        print(f"inlet: {__name__}")
        if self.debug:
            print(f"inlet: {__name__} - body:")
            print(body)
            print(f"inlet: {__name__} - user:")
            print(user)
        return body

    async def outlet(self, body: dict, user: Optional[dict] = None) -> dict:
        print(f"outlet: {__name__}")
        if self.debug:
            print(f"outlet: {__name__} - body:")
            print(body)
            print(f"outlet: {__name__} - user:")
            print(user)
        return body

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, Generator, Iterator]:
        print(f"pipe: {__name__}")
        if self.debug:
            print(f"pipe: {__name__} - received message from user: {user_message}")

        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            start_time = time.time()
            while time.time() - start_time < 60:  # aguardar por até 60 segundos
                if response.status_code == 200:
                    if response.json():
                        return response.json()
                time.sleep(1)  # aguardar por 1 segundo antes de verificar novamente
            return "Timeout error"
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return f"Workflow request failed with status code: {e.response.status_code}"
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}")
            return "Error connecting to the API"
        except requests.exceptions.Timeout as e:
            print(f"Timeout Error: {e}")
            return "Timeout error"
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return "Error parsing JSON"

retorno = Pipeline().pipe("mensagem", "modelo", [], {})
print(retorno)
