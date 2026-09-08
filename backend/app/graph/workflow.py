from langgraph.graph import END, START, StateGraph

from app.agents.code_agent import code_agent
from app.agents.design_agent import design_agent
from app.agents.repair_agent import repair_agent
from app.agents.requirement_agent import requirement_agent
from app.agents.validation_agent import validation_agent
from app.graph.state import WebsiteGenerationState
from app.schemas.generation import CodeSpecification


# Maximum number of times the Repair Agent can attempt to fix
# invalid generated website code.
MAX_REPAIR_ATTEMPTS = 3


async def requirement_node(
    state: WebsiteGenerationState,
) -> dict:
    """
    Execute the Requirement Agent.

    Converts the client's natural-language website idea into a
    structured website specification.
    """

    website_specification = await requirement_agent(
        state["idea"]
    )

    return {
        "website_specification": website_specification,
    }


async def design_node(
    state: WebsiteGenerationState,
) -> dict:
    """
    Execute the Design Agent.

    Uses the structured website requirements to create the
    UI/UX and visual design specification.
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
        "design_specification": design_specification,
    }


async def code_node(
    state: WebsiteGenerationState,
) -> dict:
    """
    Execute the Code Agent.

    Generates the HTML, CSS, and JavaScript implementation
    from the website requirements and design specification.
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
        "code_specification": code_specification,
    }


async def validation_node(
    state: WebsiteGenerationState,
) -> dict:
    """
    Execute the Validation Agent.

    Checks the generated HTML, CSS, and JavaScript against
    the original website requirements.
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
        "validation_specification": validation_specification,
    }


async def repair_node(
    state: WebsiteGenerationState,
) -> dict:
    """
    Execute the Repair Agent.

    Repairs invalid generated website code using the issues
    identified by the Validation Agent.
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

    # Convert the repaired code into CodeSpecification so that
    # the next Validation Agent execution receives the same
    # structured type as the original Code Agent output.
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


def validation_router(
    state: WebsiteGenerationState,
) -> str:
    """
    Decide what happens after validation.

    If the generated website is valid, the workflow ends.

    If the website is invalid and repair attempts remain,
    the workflow sends the code to the Repair Agent.

    If the maximum repair attempts have been reached,
    the workflow ends with the latest generated code.
    """

    validation_specification = state.get(
        "validation_specification"
    )

    if validation_specification is None:
        raise ValueError(
            "Validation specification is missing."
        )

    # Website passed validation.
    if validation_specification.is_valid:
        return "end"

    # Prevent an infinite repair loop.
    if state["repair_attempts"] >= MAX_REPAIR_ATTEMPTS:
        return "end"

    # Send invalid code to the Repair Agent.
    return "repair"


def build_workflow():
    """
    Build and compile the complete LangGraph website-generation
    workflow.

    Workflow:

        Requirement
            ↓
        Design
            ↓
        Code
            ↓
        Validation
            ↓
        Repair ──────┐
            ↑        │
            └────────┘

    The workflow ends when validation succeeds or when the
    maximum repair attempts are reached.
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

    # Initial workflow entry point.
    workflow.add_edge(
        START,
        "requirement",
    )

    # Main generation pipeline.
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

    # Decide whether to finish or repair the generated code.
    workflow.add_conditional_edges(
        "validation",
        validation_router,
        {
            "repair": "repair",
            "end": END,
        },
    )

    # After repairing, validate the repaired code again.
    workflow.add_edge(
        "repair",
        "validation",
    )

    # Compile the workflow into an executable LangGraph.
    return workflow.compile()


# Compiled workflow used by the generation service.
website_generation_workflow = build_workflow()