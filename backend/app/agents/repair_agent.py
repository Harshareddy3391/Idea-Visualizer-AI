from app.schemas.generation import (
    CodeSpecification,
    RepairSpecification,
    ValidationSpecification,
)
from app.services.llm_service import repair_generated_code


async def repair_agent(
    code_specification: CodeSpecification,
    validation_specification: ValidationSpecification,
) -> RepairSpecification:
    """
    Repair generated website code based on issues identified by the
    Validation Agent.

    The Repair Agent fixes critical errors and warnings while preserving
    the original website requirements and valid parts of the generated
    implementation.
    """

    if code_specification is None:
        raise ValueError("Code specification is required.")

    if validation_specification is None:
        raise ValueError("Validation specification is required.")

    if validation_specification.is_valid:
        raise ValueError(
            "Code repair is not required because the generated code is valid."
        )

    repair_result = await repair_generated_code(
        code_specification=code_specification,
        validation_specification=validation_specification,
    )

    if not isinstance(repair_result, RepairSpecification):
        raise TypeError(
            "Code repair service returned an invalid repair specification."
        )

    return repair_result