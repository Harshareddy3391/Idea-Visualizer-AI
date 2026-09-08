from fastapi import APIRouter, HTTPException, status

from app.schemas.generation import GenerateRequest
from app.services.generation_service import generate_website

router = APIRouter()


@router.post(
    "/generate",
    status_code=status.HTTP_200_OK,
    summary="Generate website",
)
async def generate(request: GenerateRequest):
    """
    Accepts a client's website idea and starts the AI website-generation
    pipeline.

    The API layer is responsible only for request validation, invoking the
    generation service, and returning the service result.
    """

    try:
        return await generate_website(request.idea)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Website generation failed: {exc}",
        ) from exc