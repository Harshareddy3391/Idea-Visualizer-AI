from fastapi import FastAPI
from app.api.generation import router as generation_router

app = FastAPI(
    title="Idea Visualizer AI",
)


@app.get("/")
def root():
    """
    Return a basic message confirming that the backend is running.
    """

    return {
        "message": "Idea Visualizer AI Backend is running"
    }


@app.get("/health")
def health():
    """
    Return the backend health status.
    """

    return {
        "status": "ok"
    }


# Register the website-generation API routes.
app.include_router(
    generation_router,
    prefix="/api",
    tags=["Generation"],
)