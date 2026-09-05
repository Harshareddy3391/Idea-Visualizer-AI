import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

from app.schemas.generation import WebsiteSpecification


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not configured.")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")


async def generate_website_content(
    idea: str,
) -> WebsiteSpecification:
    """
    Convert a client's natural-language website idea into a structured
    website specification that can be consumed by the AI generation
    workflow.
    """

    if not idea or not idea.strip():
        raise ValueError("Website idea cannot be empty.")

    response = await client.responses.parse(
        model=MODEL_NAME,
        instructions=(
            "You are a senior website requirements analyst. "
            "Analyze the client's website idea and convert it into "
            "a complete, practical website specification. "
            "Do not invent unnecessary functionality. "
            "Preserve the client's actual requirements. "
            "When a requirement is not explicitly specified, "
            "make a reasonable professional assumption."
        ),
        input=idea.strip(),
        text_format=WebsiteSpecification,
    )

    if response.output_parsed is None:
        raise RuntimeError(
            "The AI model did not return a valid website specification."
        )

    return response.output_parsed