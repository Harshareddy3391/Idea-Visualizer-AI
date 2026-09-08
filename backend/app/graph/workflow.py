from langgraph.graph import END, START, StateGraph

from app.agents.code_agent import code_agent
from app.agents.design_agent import design_agent
from app.agents.documentation_agent import documentation_agent
from app.agents.repair_agent import repair_agent
from app.agents.requirement_agent import requirement_agent
from app.agents.validation_agent import validation_agent
from app.graph.state import WebsiteGenerationState
from app.schemas.generation import CodeSpecification


MAX_REPAIR_ATTEMPTS = 3


async def requirement_node(state: WebsiteGenerationState) -> dict:
    """
    Execute the Requirement Agent.

    Converts the client's natural-language website idea into a
    structured website specification.
    """

    website_specification = await requirement_agent(
        state["idea"]
    )

    return {
        "website_specification": website_specification
    }


async def design_node(state: WebsiteGenerationState) -> dict:
    """
    Execute the Design Agent.

    Uses the structured website requirements to create the
    UI/UX design specification.
    """

    website_specification = state.get(
        "website_specification"
    )

    if website_specification is None:
        raise ValueError(
            "Website specification is missing."
        )

    design_specification = await design_agent(
        website_specification
    )

    return {
        "design_specification": design_specification
    }


async def code_node(state: WebsiteGenerationState) -> dict:
    """
    Execute the Code Agent.

    Generates HTML, CSS, and JavaScript from the website
    requirements and UI/UX design specification.
    """

    website_specification = state.get(
        "website_specification"
    )

    design_specification = state.get(
        "design_specification"
    )

    if website_specification is None:
        raise ValueError(
            "Website specification is missing."
        )

    if design_specification is None:
        raise ValueError(
            "Design specification is missing."
        )

    code_specification = await code_agent(
        website_specification=website_specification,
        design_specification=design_specification,
    )

    return {
        "code_specification": code_specification
    }


async def validation_node(
    state: WebsiteGenerationState,
) -> dict:
    """
    Execute the Validation Agent.

    Validates the generated website code against the
    original website requirements.
    """

    website_specification = state.get(
        "website_specification"
    )

    code_specification = state.get(
        "code_specification"
    )

    if website_specification is None:
        raise ValueError(
            "Website specification is missing."
        )

    if code_specification is None:
        raise ValueError(
            "Code specification is missing."
        )

    validation_specification = await validation_agent(
        website_specification=website_specification,
        code_specification=code_specification,
    )

    return {
        "validation_specification": validation_specification
    }


async def repair_node(
    state: WebsiteGenerationState,
) -> dict:
    """
    Execute the Repair Agent.

    Repairs invalid generated website code using the
    issues identified by the Validation Agent.
    """

    code_specification = state.get(
        "code_specification"
    )

    validation_specification = state.get(
        "validation_specification"
    )

    if code_specification is None:
        raise ValueError(
            "Code specification is missing."
        )

    if validation_specification is None:
        raise ValueError(
            "Validation specification is missing."
        )

    repair_specification = await repair_agent(
        code_specification=code_specification,
        validation_specification=validation_specification,
    )

    repaired_code = CodeSpecification(
        html=repair_specification.html,
        css=repair_specification.css,
        javascript=repair_specification.javascript,
    )

    return {
        "code_specification": repaired_code,
        "repair_specification": repair_specification,
        "repair_attempts": state["repair_attempts"] + 1,
    }


async def documentation_node(
    state: WebsiteGenerationState,
) -> dict:
    """
    Execute the Documentation Agent.

    Creates structured client-facing documentation after the
    final website has completed the validation and repair cycle.
    """

    website_specification = state.get(
        "website_specification"
    )

    design_specification = state.get(
        "design_specification"
    )

    validation_specification = state.get(
        "validation_specification"
    )

    repair_specification = state.get(
        "repair_specification"
    )

    if website_specification is None:
        raise ValueError(
            "Website specification is missing."
        )

    if design_specification is None:
        raise ValueError(
            "Design specification is missing."
        )

    if validation_specification is None:
        raise ValueError(
            "Validation specification is missing."
        )

    documentation_specification = await documentation_agent(
        website_specification=website_specification,
        design_specification=design_specification,
        validation_specification=validation_specification,
        repair_specification=repair_specification,
    )

    return {
        "documentation_specification": (
            documentation_specification
        )
    }


def validation_router(
    state: WebsiteGenerationState,
) -> str:
    """
    Decide whether the workflow should proceed to documentation
    or send the generated code to the Repair Agent.
    """

    validation_specification = state.get(
        "validation_specification"
    )

    if validation_specification is None:
        raise ValueError(
            "Validation specification is missing."
        )

    # If the website is valid, generate documentation.
    if validation_specification.is_valid:
        return "documentation"

    # Stop repairing after the maximum number of attempts.
    if state["repair_attempts"] >= MAX_REPAIR_ATTEMPTS:
        return "documentation"

    # Website is invalid and another repair attempt is allowed.
    return "repair"


def build_workflow():
    """
    Build and compile the complete LangGraph website-generation workflow.

    Workflow:

    Requirement
        ↓
    Design
        ↓
    Code
        ↓
    Validation
        ↓
    Repair (if required)
        ↓
    Validation
        ↓
    Documentation
        ↓
    END
    """

    workflow = StateGraph(
        WebsiteGenerationState
    )

    # Register workflow nodes.
    workflow.add_node(
        "requirement",
        requirement_node,
    )

    workflow.add_node(
        "design",
        design_node,
    )

    workflow.add_node(
        "code",
        code_node,
    )

    workflow.add_node(
        "validation",
        validation_node,
    )

    workflow.add_node(
        "repair",
        repair_node,
    )

    workflow.add_node(
        "documentation",
        documentation_node,
    )

    # Main workflow.
    workflow.add_edge(
        START,
        "requirement",
    )

    workflow.add_edge(
        "requirement",
        "design",
    )

    workflow.add_edge(
        "design",
        "code",
    )

    workflow.add_edge(
        "code",
        "validation",
    )

    # Validation decides whether to repair or document.
    workflow.add_conditional_edges(
        "validation",
        validation_router,
        {
            "repair": "repair",
            "documentation": "documentation",
        },
    )

    # After repair, validate the repaired code again.
    workflow.add_edge(
        "repair",
        "validation",
    )

    # Documentation is the final workflow stage.
    workflow.add_edge(
        "documentation",
        END,
    )

    return workflow.compile()


# Compiled workflow used by the generation service.
website_generation_workflow = build_workflow()