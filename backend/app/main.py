from fastapi import FastAPI
from app.routes import dataset
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DataGlance API", description="DataGlance backend api")

app.include_router(dataset.router, prefix="/dataset", tags=["dataset"])
# app.include_router(genai.router, prefix="/genai", tags=["genai"])
# app.include_router(visualization.router, prefix="/visualize", tags=["visualize"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to DataGlance API"}
