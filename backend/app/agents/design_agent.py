from app.schemas.generation import (
    DesignSpecification,
    WebsiteSpecification,
)
from app.services.llm_service import generate_design_content


async def design_agent(
    specification: WebsiteSpecification,
) -> DesignSpecification:
    """
    Convert structured website requirements into a detailed UI/UX
    design specification.

    The Design Agent is responsible for defining the visual structure,
    navigation, components, user experience, responsive behavior,
    typography, color palette, and accessibility requirements.
    """

    if specification is None:
        raise ValueError("Website specification is required.")

    design_specification = await generate_design_content(
        specification
    )

    if not isinstance(design_specification, DesignSpecification):
        raise TypeError(
            "Design generation service returned an invalid design specification."
        )

    return design_specification