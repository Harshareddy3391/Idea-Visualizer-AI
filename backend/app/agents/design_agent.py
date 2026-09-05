from app.schemas.generation import DesignSpecification,WebsiteSpecification

from app.services.llm_service import generate_website_content


async def design_agent(specification:WebsiteSpecification)->DesignSpecification:
       """
    Convert website requirements into a structured UI/UX design plan.

    The design agent determines the visual and interaction structure
    that the code-generation agent will use later.
    """
       if not specification:
              raise ValueError("Website specification is required.")

       return generate_website_content(specification) 