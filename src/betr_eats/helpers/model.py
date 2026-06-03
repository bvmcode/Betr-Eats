import os
from openai import AsyncOpenAI
from typing import Optional


class Model:
    def __init__(self, model_id: str, api_key: Optional[str] = None):
        self.model_id = model_id
        if api_key is None:
            api_key = os.getenv("HF_TOKEN")
        self.client = AsyncOpenAI(
            base_url="https://router.huggingface.co/v1", api_key=api_key
        )

    async def generate_text(self, prompt: str):
        completion = await self.client.chat.completions.create(
            model=self.model_id, messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
