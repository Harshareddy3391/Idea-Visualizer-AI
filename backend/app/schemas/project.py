from pydantic import BaseModel

from app.schemas.documentation import DocumentationSpecification
from app.schemas.generation import (
    CodeSpecification,
    DesignSpecification,
    RepairSpecification,
    ValidationSpecification,
    WebsiteSpecification,
)


class GeneratedWebsiteResult(BaseModel):
    """
    Complete result produced by the website-generation workflow.

    This schema represents the data required by the frontend and
    downstream services such as PDF generation.
    """

    success: bool
    website_specification: WebsiteSpecification
    design_specification: DesignSpecification
    code_specification: CodeSpecification
    validation_specification: ValidationSpecification
    repair_specification: RepairSpecification | None = None
    documentation_specification: DocumentationSpecification
    repair_attempts: int