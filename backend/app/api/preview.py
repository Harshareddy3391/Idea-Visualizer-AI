from fastapi import APIRouter,HTTPException,status

from pydantic import BaseModel,Field

router=APIRouter()


class PreviewRequest(BaseModel):

     """
    Request payload containing the generated frontend code
    that should be rendered in the client-side preview.
    """

     html: str = Field(
        ...,
        min_length=1,
        description="Generated HTML code",
     )

     css: str = Field(
        ...,
        min_length=1,
        description="Generated CSS code",
     )

     javascript: str = Field(
        default="",
        description="Generated JavaScript code",
     )



@router.post("/preview",status_code=status.HTTP_200_OK,
             summary="prepare website preview")
async def create_preview(request:PreviewRequest):
      """
    Prepare generated HTML, CSS, and JavaScript for the
    frontend live-preview environment.

    The backend does not execute AI-generated JavaScript.
    The generated code is returned to the frontend, where it
    will be rendered inside a sandboxed iframe.
    """


      if not request.html.strip():
            raise HTTPException(
                  status_code=status.HTTP_400_BAD_REQUEST,
                  detail="HTML code cannot be empty."
            )

      if not request.css.strip():
            raise HTTPException(
                  status_code=status.HTTP_400_BAD_REQUEST,
                  detail="CSS code cannot be empty."
            )
      return {
            "sucess":True,
            "preview":{
                  "html":request.html,
                  "css":request.css,
                  "javascript":request.javascript
            }
      }


     