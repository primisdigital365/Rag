import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from chat import router as chat_router
from voice_chat import router as voice_router
from rag_engine import start_loading_vectorstore, initialize_gemini


# App Initialization
app = FastAPI(title="Support AI Bot")


# Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Startup Events
@app.on_event("startup")
async def startup_tasks():
    # Initialize RAG system
    logger.info("🚀 Starting RAG system...")
    initialize_gemini()
    start_loading_vectorstore()

    # Initialize Database
    try:
        from database import engine, Base
        import models  # Ensures models are registered
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Database tables synchronized")
    except Exception as e:
        logger.error(f"⚠ DB initialization failed: {e}")


# Routers
app.include_router(chat_router)
app.include_router(voice_router)


# Root Redirect
@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")


