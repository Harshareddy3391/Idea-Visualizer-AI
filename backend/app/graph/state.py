from typing import NotRequired, TypedDict

from app.schemas.generation import (
    CodeSpecification,
    DesignSpecification,
    RepairSpecification,
    ValidationSpecification,
    WebsiteSpecification,
)


class WebsiteGenerationState(TypedDict):
    """
    Shared state for the complete website-generation LangGraph workflow.

    The client idea and repair-attempt counter are provided when the
    workflow starts. The remaining fields are progressively populated
    by the Requirement, Design, Code, Validation, and Repair Agents.
    """

    # Original website idea provided by the client.
    idea: str

    # Structured requirements produced by the Requirement Agent.
    website_specification: NotRequired[
        WebsiteSpecification
    ]

    # UI/UX design produced by the Design Agent.
    design_specification: NotRequired[
        DesignSpecification
    ]

    # Generated HTML, CSS, and JavaScript produced by the Code Agent.
    code_specification: NotRequired[
        CodeSpecification
    ]

    # Validation result produced by the Validation Agent.
    validation_specification: NotRequired[
        ValidationSpecification
    ]

    # Repair result produced by the Repair Agent.
    repair_specification: NotRequired[
        RepairSpecification
    ]

    # Number of repair attempts performed by the workflow.
    repair_attempts: int