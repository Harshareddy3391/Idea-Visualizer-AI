from langgraph.graph import END, START, StateGraph

from app.agents.code_agent import code_agent
from app.agents.design_agent import design_agent
from app.agents.repair_agent import repair_agent
from app.agents.requirement_agent import requirement_agent
from app.agents.validation_agent import validation_agent
from app.graph.state import WebsiteGenerationState


MAX_REPAIR_ATTEMPTS = 3


async def requirement_node(
    state: WebsiteGenerationState,
) -> dict:
    """
    Execute the Requirement Agent and store the structured website
    requirements in the workflow state.
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
    Execute the Design Agent using the requirements produced by the
    Requirement Agent.
    """

    website_specification = state.get("website_specification")

    if website_specification is None:
        raise ValueError("Website specification is missing.")

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
    Execute the Code Agent using the website requirements and design
    specification.
    """

    website_specification = state.get("website_specification")
    design_specification = state.get("design_specification")

    if website_specification is None:
        raise ValueError("Website specification is missing.")

    if design_specification is None:
        raise ValueError("Design specification is missing.")

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
    Execute the Validation Agent against the generated website code.
    """

    website_specification = state.get("website_specification")
    code_specification = state.get("code_specification")

    if website_specification is None:
        raise ValueError("Website specification is missing.")

    if code_specification is None:
        raise ValueError("Code specification is missing.")

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
    Execute the Repair Agent when validation identifies problems.
    """

    code_specification = state.get("code_specification")
    validation_specification = state.get(
        "validation_specification"
    )

    if code_specification is None:
        raise ValueError("Code specification is missing.")

    if validation_specification is None:
        raise ValueError("Validation specification is missing.")

    repair_specification = await repair_agent(
        code_specification=code_specification,
        validation_specification=validation_specification,
    )

    return {
        "code_specification": {
            "html": repair_specification.html,
            "css": repair_specification.css,
            "javascript": repair_specification.javascript,
        },
        "repair_specification": repair_specification,
        "repair_attempts": state["repair_attempts"] + 1,
    }


def validation_router(
    state: WebsiteGenerationState,
) -> str:
    """
    Decide whether the workflow should finish or send the generated
    code to the Repair Agent.
    """

    validation_specification = state.get(
        "validation_specification"
    )

    if validation_specification is None:
        raise ValueError("Validation specification is missing.")

    if validation_specification.is_valid:
        return "end"

    if state["repair_attempts"] >= MAX_REPAIR_ATTEMPTS:
        return "end"

    return "repair"


def build_workflow():
    """
    Build and compile the LangGraph website-generation workflow.
    """

    workflow = StateGraph(WebsiteGenerationState)

    workflow.add_node("requirement", requirement_node)
    workflow.add_node("design", design_node)
    workflow.add_node("code", code_node)
    workflow.add_node("validation", validation_node)
    workflow.add_node("repair", repair_node)

    workflow.add_edge(START, "requirement")
    workflow.add_edge("requirement", "design")
    workflow.add_edge("design", "code")
    workflow.add_edge("code", "validation")

    workflow.add_conditional_edges(
        "validation",
        validation_router,
        {
            "repair": "repair",
            "end": END,
        },
    )

    workflow.add_edge("repair", "validation")

    return workflow.compile()


website_generation_workflow = build_workflow()