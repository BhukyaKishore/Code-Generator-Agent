from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from datetime import datetime
from pathlib import Path
import logging

from agent_v2 import CodeGeneratorAgent

from .config import BOT_NAMES, SUPPORTED_LANGUAGES, startup_time
from .models import CodeGenerationRequest, CodeGenerationResponse, HealthResponse
from .utils import validate_prompt, validate_language, SECURITY_PATTERNS

logger = logging.getLogger(__name__)

router = APIRouter()

# ============================================================================
# AGENT INITIALIZATION
# ============================================================================

try:
    logger.info("🔄 Initializing Code Generator Agent...")
    agent = CodeGeneratorAgent()
    logger.info("✅ Agent initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize agent: {e}", exc_info=True)
    agent = None

# ============================================================================
# ROUTES
# ============================================================================

@router.get("/", tags=["Root"])
async def root():
    """Serve the main HTML page"""
    logger.info("📄 Root endpoint accessed - serving index.html")
    # Assuming index.html is in the project root
    return FileResponse("index.html", media_type="text/html")

@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    uptime = datetime.now() - startup_time
    uptime_str = f"{uptime.seconds // 3600}h {(uptime.seconds % 3600) // 60}m"
    
    logger.info("💚 Health check requested")
    return {
        "status": "healthy" if agent else "degraded",
        "service": "Code Wizard API",
        "timestamp": datetime.now().isoformat(),
        "uptime": uptime_str
    }

@router.post("/api/generate", response_model=CodeGenerationResponse, tags=["Generation"])
async def generate_code(request: CodeGenerationRequest):
    """
    Generate code based on prompt and language
    """
    
    start_time = datetime.now()
    logger.info("=" * 80)
    logger.info("📥 NEW CODE GENERATION REQUEST")
    logger.info("=" * 80)
    
    try:
        # Log request details
        logger.info(f"🔤 Language: {request.language}")
        logger.info(f"📝 Prompt: {request.prompt[:100]}...")
        
        # Validate language
        if not validate_language(request.language):
            logger.error(f"❌ Invalid language: {request.language}")
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language. Supported: {', '.join(SUPPORTED_LANGUAGES)}"
            )
        
        # Validate prompt
        validation = validate_prompt(request.prompt)
        if not validation['valid']:
            logger.warning(f"⚠️ Validation failed: {validation['message']}")
            raise HTTPException(
                status_code=400,
                detail=validation['message']
            )
        
        # Check if agent is initialized
        if not agent:
            logger.error("❌ Agent not initialized - service unavailable")
            raise HTTPException(
                status_code=503,
                detail="Code generation service is currently unavailable"
            )
        
        logger.info(f"🚀 Starting code generation for {request.language}...")
        
        # Generate code using agent
        result = agent.generate_code(
            prompt=request.prompt,
            language=request.language
        )
        
        generation_time = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"✅ Code generated successfully in {generation_time:.2f}s")
        logger.info(f"📊 Generated code length: {len(result['code'])} characters")
        logger.info("=" * 80)
        
        return {
            "code": result['code'],
            "language": request.language,
            "prompt": request.prompt,
            "timestamp": datetime.now().isoformat(),
            "bot_name": BOT_NAMES.get(request.language, "CodeWizard"),
            "status": "success",
            "generation_time": generation_time
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error generating code: {str(e)}", exc_info=True)
        logger.info("=" * 80)
        raise HTTPException(
            status_code=500,
            detail="An error occurred during code generation. Please try again."
        )

@router.get("/api/languages", tags=["Info"])
async def get_languages():
    """Get list of supported languages and their bot names"""
    logger.info("📚 Languages endpoint accessed")
    return {
        "languages": SUPPORTED_LANGUAGES,
        "bots": BOT_NAMES,
        "count": len(SUPPORTED_LANGUAGES)
    }

@router.get("/api/guardrails", tags=["Info"])
async def get_guardrails():
    """Get list of applied security guardrails"""
    logger.info("🛡️ Guardrails endpoint accessed")
    return {
        "guardrails": [
            "No SQL injection patterns",
            "No malicious code execution",
            "No buffer overflow attempts",
            "No credential exposure",
            "No system command injection",
            "No privilege escalation",
            "No command chaining"
        ],
        "max_prompt_length": 1000,
        "security_patterns_count": len(SECURITY_PATTERNS)
    }

@router.get("/api/logs", tags=["Info"])
async def get_recent_logs():
    """Get list of recent log files"""
    logger.info("📋 Logs endpoint accessed")
    log_dir = Path("logs")
    
    if not log_dir.exists():
        return {"logs": []}
    
    log_files = sorted(log_dir.glob("*.log"), reverse=True)[:10]
    return {
        "logs": [f.name for f in log_files],
        "total": len(list(log_dir.glob("*.log")))
    }
