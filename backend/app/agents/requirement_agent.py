from app.schemas.generation import WebsiteSpecification
from app.services.llm_service import generate_website_content


async def requirement_agent(
    idea: str,
) -> WebsiteSpecification:
    """
    Analyze the client's website idea and convert it into a structured
    website specification.

    The Requirement Agent is responsible for understanding the client's
    intent and identifying the website purpose, target audience, pages,
    sections, features, content requirements, visual style, colors,
    and responsive requirements.
    """

    if not idea or not idea.strip():
        raise ValueError("Website idea is required.")

    website_specification = await generate_website_content(
        idea=idea.strip()
    )

    if not isinstance(website_specification, WebsiteSpecification):
        raise TypeError(
            "Requirement generation service returned an invalid "
            "website specification."
        )

    return website_specification