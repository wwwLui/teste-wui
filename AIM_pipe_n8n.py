from typing import List, Union, Generator, Iterator, Optional
from pprint import pprint
import requests, json, warnings
from typing import Optional, Callable, Awaitable
from pydantic import BaseModel, Field
import os
import time
import requests
# Uncomment to disable SSL verification warnings if needed.
# warnings.filterwarnings('ignore', message='Unverified HTTPS request')

class Pipeline:
    def __init__(self):
        self.name = "N8N Agent Pipeline"
        self.api_url = "https://n8n.autointmind.com/webhook-test/62f78f96-6cae-4cfd-985d-27d2da8fd8b5"     # Set correct hostname
       # self.api_key = ""                                    # Insert your actual API key here
        self.verify_ssl = True
        self.debug = False
        # Please note that N8N do not support stream reponses

    async def emit_status(
        self,
        __event_emitter__: Callable[[dict], Awaitable[None]],
        level: str,
        message: str,
        done: bool,
    ):
        current_time = time.time()
        if (
            __event_emitter__
            and self.valves.enable_status_indicator
            and (
                current_time - self.last_emit_time >= self.valves.emit_interval or done
            )
        ):
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "status": "complete" if done else "in_progress",
                        "level": level,
                        "description": message,
                        "done": done,
                    },
                }
            )
            self.last_emit_time = current_time

    async def pipe(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __event_emitter__: Callable[[dict], Awaitable[None]] = None,
        __event_call__: Callable[[dict], Awaitable[dict]] = None,
    ) -> Optional[dict]:
        await self.emit_status(
            __event_emitter__, "info", "/Calling N8N Workflow...", False
        )

        messages = body.get("messages", [])

        # Verify a message is available
        if messages:
            question = messages[-1]["content"]
            if "Prompt: " in question:
                question = question.split("Prompt: ")[-1]
            try:
                # Invoke N8N workflow
                headers = {
                  #  "Authorization": f"Bearer {self.valves.n8n_bearer_token}",
                    "Content-Type": "application/json",
                }
                payload = {"sessionId": f"{__user__['id']} - {messages[0]['content'].split('Prompt: ')[-1][:100]}"}
                payload[self.valves.input_field] = question
                response = requests.post(
                    self.valves.n8n_url, json=payload, headers=headers
                )
                if response.status_code == 200:
                    n8n_response = response.json()[self.valves.response_field]
                else:
                    raise Exception(f"Error: {response.status_code} - {response.text}")

                # Set assitant message with chain reply
                body["messages"].append({"role": "assistant", "content": n8n_response})
            except Exception as e:
                await self.emit_status(
                    __event_emitter__,
                    "error",
                    f"Error during sequence execution: {str(e)}",
                    True,
                )
                return {"error": str(e)}
        # If no message is available alert user
        else:
            await self.emit_status(
                __event_emitter__,
                "error",
                "No messages found in the request body",
                True,
            )
            body["messages"].append(
                {
                    "role": "assistant",
                    "content": "No messages found in the request body",
                }
            )

        await self.emit_status(__event_emitter__, "info", "Complete", True)
        return n8n_response
