"""
FastAPI Backend for Code Wizard - Multi-Language Code Generator
Handles routing, validation, and agent orchestration
Enhanced with timestamped logging per run
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import logging
import os
from datetime import datetime
import re
from pathlib import Path
from agent_v2 import CodeGeneratorAgent

# ============================================================================
# LOGGING CONFIGURATION WITH TIMESTAMPS
# ============================================================================

def setup_logging():
    """Setup logging with timestamp-based filenames"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create timestamped log filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"codewizard_{timestamp}.log"
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler with timestamp
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return log_file

log_file = setup_logging()
logger = logging.getLogger(__name__)

logger.info("=" * 80)
logger.info("🚀 CODE WIZARD API - APPLICATION STARTUP")
logger.info("=" * 80)
logger.info(f"📝 Log File: {log_file}")
logger.info(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================================================
# FASTAPI APP SETUP
# ============================================================================

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

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class CodeGenerationRequest(BaseModel):
    """Request model for code generation"""
    prompt: str
    language: str
    
    class Config:
        example = {
            "prompt": "Write a function to count vowels in a string",
            "language": "python"
        }

class CodeGenerationResponse(BaseModel):
    """Response model for code generation"""
    code: str
    language: str
    prompt: str
    timestamp: str
    bot_name: str
    status: str
    generation_time: float

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    timestamp: str
    uptime: str

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
# CONSTANTS
# ============================================================================

BOT_NAMES = {
    "python": "PyWizard",
    "javascript": "ScriptMaster",
    "java": "ByteForge",
    "cpp": "CppNinja",
    "c": "CChain",
    "sql": "DataAlchemy"
}

SUPPORTED_LANGUAGES = list(BOT_NAMES.keys())

# Application startup time
startup_time = datetime.now()

# ============================================================================
# GUARDRAILS & VALIDATION
# ============================================================================

SECURITY_PATTERNS = [
    r'drop\s+table',
    r'delete\s+from',
    r'truncate\s+table',
    r'exec\s*\(',
    r'eval\s*\(',
    r'system\s*\(',
    r'os\.system',
    r'subprocess',
    r'__import__',
    r'base64\s*decode',
    r'password\s*=',
    r'api[_-]?key',
    r'secret\s*=',
    r'rm\s+-rf',
    r'chmod\s+777',
    r'sudo',
    r'curl.*exec',
    r'wget.*exec',
]

def validate_prompt(prompt: str) -> dict:
    """
    Validate prompt against security guardrails
    Returns: {'valid': bool, 'message': str}
    """
    
    if not prompt or len(prompt.strip()) == 0:
        logger.warning("❌ Empty prompt received")
        return {
            'valid': False,
            'message': 'Prompt cannot be empty'
        }
    
    if len(prompt) > 1000:
        logger.warning(f"⚠️ Prompt exceeds max length: {len(prompt)} chars")
        return {
            'valid': False,
            'message': 'Prompt exceeds maximum length of 1000 characters'
        }
    
    prompt_lower = prompt.lower()
    
    for pattern in SECURITY_PATTERNS:
        if re.search(pattern, prompt_lower):
            logger.warning(f"🛡️ SECURITY: Restricted pattern detected: {pattern}")
            return {
                'valid': False,
                'message': '⚠️ Request contains restricted patterns. Please modify your request.'
            }
    
    logger.info("✅ Prompt validation passed")
    return {'valid': True, 'message': 'Validation passed'}

def validate_language(language: str) -> bool:
    """Validate if language is supported"""
    is_valid = language.lower() in SUPPORTED_LANGUAGES
    if not is_valid:
        logger.warning(f"❌ Unsupported language requested: {language}")
    return is_valid

# ============================================================================
# ROUTES
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Serve the main HTML page"""
    logger.info("📄 Root endpoint accessed - serving index.html")
    return FileResponse("index.html", media_type="text/html")

@app.get("/health", response_model=HealthResponse, tags=["Health"])
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

@app.post("/api/generate", response_model=CodeGenerationResponse, tags=["Generation"])
async def generate_code(request: CodeGenerationRequest):
    """
    Generate code based on prompt and language
    
    **Parameters:**
    - prompt: Description of the code to generate
    - language: Programming language (python, javascript, java, cpp, c, sql)
    
    **Returns:**
    - code: Generated code
    - language: Programming language used
    - prompt: Original prompt
    - timestamp: Generation timestamp
    - bot_name: Name of the bot used
    - status: Generation status
    - generation_time: Time taken to generate (seconds)
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

@app.get("/api/languages", tags=["Info"])
async def get_languages():
    """Get list of supported languages and their bot names"""
    logger.info("📚 Languages endpoint accessed")
    return {
        "languages": SUPPORTED_LANGUAGES,
        "bots": BOT_NAMES,
        "count": len(SUPPORTED_LANGUAGES)
    }

@app.get("/api/guardrails", tags=["Info"])
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

@app.get("/api/logs", tags=["Info"])
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

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError"""
    logger.error(f"❌ ValueError: {exc}")
    return {
        "detail": "Invalid input provided",
        "error_type": "ValueError"
    }

# ============================================================================
# STARTUP & SHUTDOWN
# ============================================================================

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

# ============================================================================
# MAIN
# ============================================================================

# if __name__ == "__main__":
#     import uvicorn
    
#     logger.info("🔥 Starting FastAPI server...")
#     logger.info("🌐 Server: http://0.0.0.0:8000")
#     logger.info("📚 API Docs: http://localhost:8000/docs")
#     logger.info("📝 Swagger UI: http://localhost:8000/swagger-ui.html")
    
#     uvicorn.run(
#         app,
#         host="0.0.0.0",
#         port=8000,
#         log_level="info"
#     )