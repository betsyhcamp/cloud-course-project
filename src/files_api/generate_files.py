from typing import (
    Literal,
    Tuple,
    Union,
)

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

# from pyexpat.errors import messages

SYSTEM_PROMPT = "You are an autocompletion tool that produces text files given constraints."


async def get_text_chat_completion(prompt: str) -> str:
    """Generate a text chat completion from a given prompt."""
    print("in get_text_completion function")
    client = AsyncOpenAI(base_url="http://localhost:5005", api_key="mocked_key")

    # get chat completion
    response: ChatCompletion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_tokens=100,  # limit number tokens/credits used
        n=1,  # number responses returned
    )
    print("In get_text_chat_completion, response:", response)
    return response.choices[0].message.content or ""


async def generate_image(prompt: str) -> Union[str, None]:
    """Generate an image from a given prompt."""
    # get the OpenAI client
    client = AsyncOpenAI()

    # get image from OpenAI
    image_response = await client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return image_response.data[0].url or None


async def generate_text_to_speech(
    prompt: str,
    response_format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm"] = "mp3",
) -> Tuple[bytes, str]:
    """
    Generate text-to-speech audio from a given prompt.

    Returns the audio content as bytes and the MIME type as a string.
    """

    # get OpenAI client
    client = AsyncOpenAI()

    # get audio response
    audio_response = await client.audio.speech.with_raw_response.create(
        model="tts-1",
        voice="echo",
        input=prompt,
        response_format=response_format,
    )

    # Get audio as bytes
    file_content_bytes: bytes = audio_response.content
    file_mime_type: str = audio_response.headers.get("Content-Type")

    return file_content_bytes, file_mime_type
