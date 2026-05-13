from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.banking_routes import router as banking_router
from backend.app.api.chat_routes import router as chat_router

app = FastAPI(
    title="AMENet Chatbot Mock Banking API",
    description="API bancaire simulée pour le prototype de chatbot assistant bancaire.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(banking_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "AMENet Chatbot Mock Banking API",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }
