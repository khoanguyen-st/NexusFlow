from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health, projects, search, plans

app = FastAPI(
    title="NexusFlow AI",
    description="AI-powered code analysis and implementation planning",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(plans.router, prefix="/api/plans", tags=["Plans"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "NexusFlow AI",
        "version": "0.1.0",
        "docs": "/docs",
    }
