from typing import Optional, TypedDict

from app.schemas.generation import (
    CodeSpecification,
    DesignSpecification,
    RepairSpecification,
    ValidationSpecification,
    WebsiteSpecification,
)


class WebsiteGenerationState(TypedDict):
    """
    Shared state for the website-generation LangGraph workflow.

    Each workflow node reads the data produced by previous agents and
    writes its result back into this shared state.
    """

    idea: str

    website_specification: Optional[WebsiteSpecification]

    design_specification: Optional[DesignSpecification]

    code_specification: Optional[CodeSpecification]

    validation_specification: Optional[ValidationSpecification]

    repair_specification: Optional[RepairSpecification]

    repair_attempts: int