from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_gastric import router as gastric_router

app = FastAPI(title="AI Diagnostic System API")

# Setup CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gastric_router, prefix="/api/gastric", tags=["Gastric Analysis"])

@app.get("/")
def root():
    return {"message": "Backend is running successfully"}