from app.schemas.generation import (
    CodeSpecification,
    ValidationSpecification,
    WebsiteSpecification,
)
from app.services.llm_service import validate_generated_code


async def validation_agent(
    website_specification: WebsiteSpecification,
    code_specification: CodeSpecification,
) -> ValidationSpecification:
    """
    Validate generated website code against the original requirements.

    The Validation Agent checks whether the generated HTML, CSS,
    JavaScript, and required functionality satisfy the website
    specification.
    """

    if website_specification is None:
        raise ValueError("Website specification is required.")

    if code_specification is None:
        raise ValueError("Code specification is required.")

    validation_result = await validate_generated_code(
        website_specification=website_specification,
        code_specification=code_specification,
    )

    if not isinstance(validation_result, ValidationSpecification):
        raise TypeError(
            "Code validation service returned an invalid validation specification."
        )

    return validation_result