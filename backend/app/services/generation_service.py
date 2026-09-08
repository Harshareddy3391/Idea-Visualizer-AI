from app.graph.workflow import website_generation_workflow


async def generate_website(idea: str) -> dict:
    """
    Start the LangGraph website-generation workflow for a client idea.

    The workflow executes the Requirement, Design, Code, Validation,
    and Repair Agents and returns the final generated website data.
    """

    idea = idea.strip()

    if not idea:
        raise ValueError("Website idea cannot be empty.")

    initial_state = {
        "idea": idea,
        "repair_attempts": 0,
    }

    final_state = await website_generation_workflow.ainvoke(
        initial_state
    )

    return {
        "success": True,
        "website_specification": (
            final_state["website_specification"].model_dump()
            if final_state.get("website_specification")
            else None
        ),
        "design_specification": (
            final_state["design_specification"].model_dump()
            if final_state.get("design_specification")
            else None
        ),
        "code_specification": (
            final_state["code_specification"].model_dump()
            if final_state.get("code_specification")
            else None
        ),
        "validation_specification": (
            final_state["validation_specification"].model_dump()
            if final_state.get("validation_specification")
            else None
        ),
        "repair_specification": (
            final_state["repair_specification"].model_dump()
            if final_state.get("repair_specification")
            else None
        ),
        "repair_attempts": final_state.get("repair_attempts", 0),
    }