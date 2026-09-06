from app.schemas.generation import (
    CodeSpecification,
    DesignSpecification,
    WebsiteSpecification,
)
from app.services.llm_service import generate_code_content


async def code_agent(
    website_specification: WebsiteSpecification,
    design_specification: DesignSpecification,
) -> CodeSpecification:
    """
    Generate the frontend implementation from the website requirements
    and UI/UX design specification.

    The Code Agent is responsible for converting approved requirements
    and design decisions into HTML, CSS, and JavaScript.
    """

    if website_specification is None:
        raise ValueError("Website specification is required.")

    if design_specification is None:
        raise ValueError("Design specification is required.")

    code_specification = await generate_code_content(
        website_specification=website_specification,
        design_specification=design_specification,
    )

    if not isinstance(code_specification, CodeSpecification):
        raise TypeError(
            "Code generation service returned an invalid code specification."
        )

    return code_specification