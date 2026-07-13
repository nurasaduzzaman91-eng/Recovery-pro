from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import logging

from routes import users, injuries, exercises, analytics
from database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RecoveryPro API",
    description="AI-powered injury recovery tracker with predictive analytics",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(injuries.router, prefix="/api/injuries", tags=["injuries"])
app.include_router(exercises.router, prefix="/api/exercises", tags=["exercises"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

@app.get("/")
def read_root():
    return {
        "message": "Welcome to RecoveryPro API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.exception_handler(SQLAlchemyError)
async def sql_exception_handler(request, exc):
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error occurred"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
