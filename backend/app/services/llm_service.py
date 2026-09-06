import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

from app.schemas.generation import (
    CodeSpecification,
    DesignSpecification,
    RepairSpecification,
    ValidationSpecification,
    WebsiteSpecification,
)


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not configured.")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")


async def generate_website_content(
    idea: str,
) -> WebsiteSpecification:
    """
    Convert the client's natural-language idea into a structured
    website specification.

    This function is used by the Requirement Agent.
    """

    if not idea or not idea.strip():
        raise ValueError("Website idea cannot be empty.")

    response = await client.responses.parse(
        model=MODEL_NAME,
        instructions=(
            "You are a senior website requirements analyst. "
            "Analyze the client's website idea and convert it into "
            "a complete structured website specification. "
            "Preserve the client's requirements and make reasonable "
            "professional assumptions where details are missing."
        ),
        input=idea.strip(),
        text_format=WebsiteSpecification,
    )

    if response.output_parsed is None:
        raise RuntimeError(
            "The AI model did not return a valid website specification."
        )

    return response.output_parsed


async def generate_design_content(
    specification: WebsiteSpecification,
) -> DesignSpecification:
    """
    Convert structured website requirements into a detailed UI/UX
    design specification.

    This function is used by the Design Agent.
    """

    if specification is None:
        raise ValueError("Website specification is required.")

    response = await client.responses.parse(
        model=MODEL_NAME,
        instructions=(
            "You are a senior UI/UX designer. "
            "Create a production-ready website design specification "
            "from the provided website requirements. "
            "Define the layout, navigation, typography, color palette, "
            "components, user experience, responsive behavior, and "
            "accessibility requirements. "
            "Keep every design decision aligned with the requirements."
        ),
        input=specification.model_dump_json(),
        text_format=DesignSpecification,
    )

    if response.output_parsed is None:
        raise RuntimeError(
            "The AI model did not return a valid design specification."
        )

    return response.output_parsed


async def generate_code_content(
    website_specification: WebsiteSpecification,
    design_specification: DesignSpecification,
) -> CodeSpecification:
    """
    Generate the frontend implementation from the approved website
    requirements and UI/UX design specification.

    This function is used by the Code Agent.
    """

    if website_specification is None:
        raise ValueError("Website specification is required.")

    if design_specification is None:
        raise ValueError("Design specification is required.")

    input_data = (
        "WEBSITE REQUIREMENTS:\n"
        f"{website_specification.model_dump_json(indent=2)}\n\n"
        "UI/UX DESIGN SPECIFICATION:\n"
        f"{design_specification.model_dump_json(indent=2)}"
    )

    response = await client.responses.parse(
        model=MODEL_NAME,
        instructions=(
            "You are a senior frontend engineer. "
            "Generate a complete production-ready frontend implementation "
            "from the provided website requirements and UI/UX design "
            "specification. "
            "Return semantic HTML, maintainable CSS, and functional "
            "JavaScript. "
            "Ensure the implementation is responsive, accessible, and "
            "faithful to the requirements and design. "
            "Do not include explanations outside the requested code fields."
        ),
        input=input_data,
        text_format=CodeSpecification,
    )

    if response.output_parsed is None:
        raise RuntimeError(
            "The AI model did not return a valid code specification."
        )

    return response.output_parsed


async def validate_generated_code(
    website_specification: WebsiteSpecification,
    code_specification: CodeSpecification,
) -> ValidationSpecification:
    """
    Validate generated frontend code against the original website
    requirements.

    This function is used by the Validation Agent.
    """

    if website_specification is None:
        raise ValueError("Website specification is required.")

    if code_specification is None:
        raise ValueError("Code specification is required.")

    input_data = (
        "WEBSITE REQUIREMENTS:\n"
        f"{website_specification.model_dump_json(indent=2)}\n\n"
        "GENERATED CODE:\n"
        f"{code_specification.model_dump_json(indent=2)}"
    )

    response = await client.responses.parse(
        model=MODEL_NAME,
        instructions=(
            "You are a senior frontend code reviewer and QA engineer. "
            "Validate the generated website implementation against the "
            "provided website requirements. "
            "Check HTML structure, CSS implementation, JavaScript "
            "implementation, requirement coverage, responsiveness, "
            "and obvious functional problems. "
            "Separate critical errors from non-critical warnings. "
            "Set is_valid to true only when the implementation is "
            "sufficiently correct and all important requirements are met."
        ),
        input=input_data,
        text_format=ValidationSpecification,
    )

    if response.output_parsed is None:
        raise RuntimeError(
            "The AI model did not return a valid validation specification."
        )

    return response.output_parsed



async def repair_generated_code(
    code_specification: CodeSpecification,
    validation_specification: ValidationSpecification,
) -> RepairSpecification:
    """
    Repair generated frontend code based on issues identified by the
    Validation Agent.

    This function preserves valid parts of the existing implementation
    while fixing the errors required for the website to pass validation.
    """

    if code_specification is None:
        raise ValueError("Code specification is required.")

    if validation_specification is None:
        raise ValueError("Validation specification is required.")

    input_data = (
        "GENERATED CODE:\n"
        f"{code_specification.model_dump_json(indent=2)}\n\n"
        "VALIDATION RESULT:\n"
        f"{validation_specification.model_dump_json(indent=2)}"
    )

    response = await client.responses.parse(
        model=MODEL_NAME,
        instructions=(
            "You are a senior frontend engineer responsible for repairing "
            "AI-generated website code. "
            "Review the generated HTML, CSS, and JavaScript together with "
            "the validation result. "
            "Fix all critical errors and address relevant warnings. "
            "Preserve functionality that is already correct. "
            "Do not remove required website features merely to avoid errors. "
            "Return the complete corrected HTML, CSS, JavaScript, and a "
            "list describing the changes that were applied."
        ),
        input=input_data,
        text_format=RepairSpecification,
    )

    if response.output_parsed is None:
        raise RuntimeError(
            "The AI model did not return a valid repair specification."
        )

    return response.output_parsed