from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

from .config import SUPPORTED_LANGUAGES, startup_time
from .utils import SECURITY_PATTERNS
from .routes import router, agent

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    app = FastAPI(
        title="Code Wizard API",
        description="Multi-Language Code Generator with AI",
        version="1.0.0"
    )
    
    logger.info("✅ FastAPI application initialized")
    
    # CORS Configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    logger.info("✅ CORS middleware configured")
    
    # Include routes
    app.include_router(router)
    
    # Register events
    @app.on_event("startup")
    async def startup_event():
        """Run on application startup"""
        logger.info("✨ " + "=" * 76 + " ✨")
        logger.info("✨ CODE WIZARD API - FULLY OPERATIONAL")
        logger.info("✨ " + "=" * 76 + " ✨")
        logger.info(f"🌐 Supported Languages: {', '.join(SUPPORTED_LANGUAGES)}")
        logger.info(f"🤖 Agent Status: {'✅ Ready' if agent else '❌ Failed'}")
        logger.info(f"🔐 Security Patterns: {len(SECURITY_PATTERNS)} rules loaded")
        logger.info(f"📍 API Documentation: http://localhost:8000/docs")
        logger.info("✨ " + "=" * 76 + " ✨")

    @app.on_event("shutdown")
    async def shutdown_event():
        """Run on application shutdown"""
        logger.info("=" * 80)
        logger.info("👋 CODE WIZARD API - SHUTTING DOWN")
        logger.info("=" * 80)
        uptime = datetime.now() - startup_time
        logger.info(f"⏱️ Session Duration: {uptime}")
        logger.info("=" * 80)

    # Exception handlers
    @app.exception_handler(ValueError)
    async def value_error_handler(request, exc):
        """Handle ValueError"""
        logger.error(f"❌ ValueError: {exc}")
        return {
            "detail": "Invalid input provided",
            "error_type": "ValueError"
        }
        
    return app

app = create_app()
