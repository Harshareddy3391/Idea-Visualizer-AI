from app.schemas.documentation import DocumentationSpecification
from app.schemas.generation import (
    DesignSpecification,
    RepairSpecification,
    ValidationSpecification,
    WebsiteSpecification,
)
from app.services.documentation_service import generate_documentation


async def documentation_agent(
    website_specification: WebsiteSpecification,
    design_specification: DesignSpecification,
    validation_specification: ValidationSpecification,
    repair_specification: RepairSpecification | None,
) -> DocumentationSpecification:
    """
    Generate structured client-facing documentation from the
    final website-generation results.
    """

    if website_specification is None:
        raise ValueError("Website specification is required.")

    if design_specification is None:
        raise ValueError("Design specification is required.")

    if validation_specification is None:
        raise ValueError("Validation specification is required.")

    documentation = await generate_documentation(
        website_specification=website_specification,
        design_specification=design_specification,
        validation_specification=validation_specification,
        repair_specification=repair_specification,
    )

    if not isinstance(documentation, DocumentationSpecification):
        raise TypeError(
            "Documentation service returned an invalid "
            "documentation specification."
        )

    return documentation