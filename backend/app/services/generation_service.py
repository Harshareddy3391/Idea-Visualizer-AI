from app.services.llm_service import generate_website_content


async def generate_website(idea: str) -> dict:
    """
    Process a website-generation request and return the structured
    website specification.
    """

    idea = idea.strip()

    if not idea:
        raise ValueError("Website idea cannot be empty.")

    specification = await generate_website_content(idea)

    return {
        "success": True,
        "specification": specification.model_dump(),
    }