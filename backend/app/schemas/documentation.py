from pydantic import BaseModel, Field


class DocumentationSpecification(BaseModel):
    """
    Structured client-facing documentation produced by the
    Documentation Agent.

    This specification contains the information required to create
    the final professional PDF project report.
    """

    project_title: str = Field(
        description="Title of the generated website project"
    )

    project_overview: str = Field(
        description="Professional overview of the website project"
    )

    client_requirements: list[str] = Field(
        description="Important requirements provided by the client"
    )

    target_audience: list[str] = Field(
        description="Target users or audience of the website"
    )

    pages: list[str] = Field(
        description="Pages implemented in the generated website"
    )

    features: list[str] = Field(
        description="Features implemented in the generated website"
    )

    website_structure: list[str] = Field(
        description="Important sections and structural elements of the website"
    )

    design_decisions: list[str] = Field(
        description="Important UI/UX and visual design decisions"
    )

    technology_used: list[str] = Field(
        description="Technologies used to implement the generated website"
    )

    responsive_behavior: list[str] = Field(
        description="Responsive behavior implemented for different screen sizes"
    )

    accessibility_features: list[str] = Field(
        description="Accessibility features implemented in the website"
    )

    validation_summary: list[str] = Field(
        description="Summary of the final website validation results"
    )

    repair_summary: list[str] = Field(
        description="Summary of repairs applied to the generated website"
    )

    final_summary: str = Field(
        description="Professional final summary of the completed website"
    )