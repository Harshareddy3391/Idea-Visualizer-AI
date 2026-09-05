from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    idea: str = Field(
        ...,
        min_length=10,
        max_length=10000,
        description="Client's website idea",
    )


class WebsiteSpecification(BaseModel):
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