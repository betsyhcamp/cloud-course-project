from typing import (
    Literal,
    Tuple,
    Union,
)

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion
from pyexpat.errors import messages

SYSTEM_PROMPT = "You are an autocompletion tool that produces text files given constraints."


async def get_text_chat_completion(prompt: str) -> str:
    """Generate a text chat completion from a given prompt."""

    client = AsyncOpenAI()

    # get chat completion
    response: ChatCompletion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_tokens=100,
        n=1,  # number responses returned
    )

    return response.choices[0].message.content or ""
