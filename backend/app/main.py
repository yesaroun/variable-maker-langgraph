from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routers import variable

app = FastAPI(
    title="Variable Maker API",
    description="",
    version="1.0.0",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(variable.router, prefix="/variable", tags=["Variable"])


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Variable Maker API",
        "description": "",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "healthy",
    }
