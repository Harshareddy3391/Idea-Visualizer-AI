from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    idea: str = Field(
        ...,
        min_length=10,
        max_length=10000,
        description="Client's website idea",
    )


class WebsiteSpecification(BaseModel):  
    """
    Structured website requirements produced by the Requirement Agent.
    This schema is consumed by the Design Agent and Code Agent.
    """

    website_name: str = Field(
        description="Name or title of the proposed website"
    )

    purpose: str = Field(
        description="Primary purpose of the website"
    )

    target_audience: list[str] = Field(
        description="Primary target audiences"
    )

    pages: list[str] = Field(
        description="Pages required for the website"
    )

    sections: list[str] = Field(
        description="Important sections required across the website"
    )

    features: list[str] = Field(
        description="Functional features required by the client"
    )

    content_requirements: list[str] = Field(
        description="Content that should be present on the website"
    )

    visual_style: str = Field(
        description="Overall visual style and design direction"
    )

    color_preferences: list[str] = Field(
        description="Requested or recommended colors"
    )

    responsive_requirements: list[str] = Field(
        description="Responsive behavior requirements"
    )







class DesignSpecification(BaseModel):
    """
    Structured UI/UX decisions produced from the website requirements.
    This schema is consumed by the Code Agent.
    """
    layout: str = Field(
        description="Overall website layout structure"
    )

    navigation: list[str] = Field(
        description="Website navigation structure"
    )

    typography: str = Field(
        description="Typography style and hierarchy"
    )

    color_palette: list[str] = Field(
        description="Primary, secondary, and accent colors"
    )

    components: list[str] = Field(
        description="UI components required for the website"
    )

    user_experience: list[str] = Field(
        description="Important UX interactions and principles"
    )

    responsive_design: list[str] = Field(
        description="Responsive behavior across different screen sizes"
    )

    accessibility: list[str] = Field(
        description="Accessibility requirements"
    )


class CodeSpecification(BaseModel):
    """
    Generated frontend source code produced by the Code Agent.
    The Validation Agent consumes this schema to verify the implementation.
    """
    html: str = Field(
        description="Complete HTML structure of the generated website"
    )

    css: str = Field(
        description="Complete CSS styles for the generated website"
    )

    javascript: str = Field(
        description="Complete JavaScript functionality for the generated website"
    )


class ValidationSpecification(BaseModel):
    """
    Structured validation result produced by the Validation Agent.

    The Repair Agent uses this result to identify and fix problems
    found in the generated website code.
    """

    is_valid: bool = Field(
        description="Whether the generated website code passes validation"
    )

    errors: list[str] = Field(
        description="Critical errors that must be fixed"
    )

    warnings: list[str] = Field(
        description="Non-critical issues that should be reviewed"
    )

    html_valid: bool = Field(
        description="Whether the generated HTML is valid"
    )

    css_valid: bool = Field(
        description="Whether the generated CSS is valid"
    )

    javascript_valid: bool = Field(
        description="Whether the generated JavaScript is valid"
    )

    requirements_met: bool = Field(
        description="Whether the generated website satisfies the requested requirements"
    )



class RepairSpecification(BaseModel):
    """
    Structured repair result produced by the Repair Agent.

    The result contains the corrected frontend implementation after
    addressing issues identified by the Validation Agent.
    """

    html: str = Field(
        description="Corrected HTML structure of the website"
    )

    css: str = Field(
        description="Corrected CSS styles for the website"
    )

    javascript: str = Field(
        description="Corrected JavaScript functionality for the website"
    )

    changes: list[str] = Field(
        description="List of fixes applied to the generated website"
    )


