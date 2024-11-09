from typing import Optional, Callable, Awaitable
from pydantic import BaseModel, Field
import os
import time
import requests

class Pipe:
    class Valves(BaseModel):
        n8n_url: str = Field(
           default = "https://n8n.autointmind.com/webhook-test/get-test"   
        )

    def __init__(self):
        self.type = "pipe"
        self.id = "Pipeline_123"
        self.name = "Pipeline teste"
        self.valves = self.Valves()
        self.last_emit_time = 0

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
            __event_emitter__,
            "info",
            "/Calling Pipeline teste...",
            False,
        )

        messages = body.get("messages", [])

        if messages:
            question = messages[-1]["content"]
            try:
                headers = {
                    "Content-Type": "application/json"
                }
                response = requests.get(
                    self.valves.n8n_url,
                    headers=headers,
                    params={"sessionId": f"{__user__['id']} - {messages[0]['content'].split('Prompt: ')[-1][:100]}"}
                )
                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                await self.emit_status(
                    __event_emitter__,
                    "error",
                    f"Error during sequence execution: {str(e)}",
                    True,
                )
                return {"error": str(e)}
        else:
            await self.emit_status(__event_emitter__, "error", "No messages found in the request body", True)
            body["messages"].append(
                {
                    "role": "assistant",
                    "content": "No messages found in the request body",
                }
            )

        await self.emit_status(__event_emitter__, "info", "Complete", True)
        return None




