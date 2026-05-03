from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.api.routes_gastric import router as gastric_router
from app.api.routes_auth import router as auth_router

app = FastAPI(title="AI Diagnostic System API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
# app.include_router(gastric_router, prefix="/api/gastric", tags=["Gastric Analysis"])

@app.get("/")
def root():
    return {"message": "Backend is running successfully"}