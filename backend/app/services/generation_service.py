from app.graph.workflow import website_generation_workflow


async def generate_website(idea: str) -> dict:
    """
    Start the complete LangGraph website-generation workflow.

    The workflow executes the Requirement, Design, Code, Validation,
    Repair, and Documentation Agents and returns the final generated
    website data and client documentation.
    """

    idea = idea.strip()

    if not idea:
        raise ValueError("Website idea cannot be empty.")

    # Initial state contains only the information available
    # before the AI workflow starts.
    initial_state = {
        "idea": idea,
        "repair_attempts": 0,
    }

    # Execute the complete LangGraph workflow.
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

        "documentation_specification": (
            final_state["documentation_specification"].model_dump()
            if final_state.get("documentation_specification")
            else None
        ),

        "repair_attempts": final_state.get(
            "repair_attempts",
            0,
        ),
    }