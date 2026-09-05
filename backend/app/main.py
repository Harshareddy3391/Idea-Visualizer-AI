from fastapi import FastAPI

app = FastAPI(title="Idea Visualizer AI")


@app.get("/")
def root():
    return {"message": "Idea Visualizer AI Backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}