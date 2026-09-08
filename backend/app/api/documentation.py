from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.schemas.project import GeneratedWebsiteResult
from app.services.documentation_pdf_service import generate_documentation_pdf


router = APIRouter()


@router.post(
    "/documentation/pdf",
    status_code=status.HTTP_200_OK,
    summary="Generate project documentation PDF",
)
async def generate_documentation_pdf_endpoint(
    result: GeneratedWebsiteResult,
):
    """
    Generate a client-facing PDF from the complete website-generation
    result produced by the LangGraph workflow.
    """

    try:
        pdf_path = generate_documentation_pdf(
            result.documentation_specification
        )

        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=pdf_path.name,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PDF generation failed: {exc}",
        ) from exc