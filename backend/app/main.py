
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chat import router as chat_router
from app.database.database import engine, Base
from app.database import models


app = FastAPI(
    title="AgentOS AI Agent",
    description="Part 1 - Basic AI Agent",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "AgentOS AI Agent is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "AgentOS AI Agent"
    }


@app.get("/database-test")
def database_test():
    from sqlalchemy import text

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "success",
        "message": "Database connection successful"
    }
