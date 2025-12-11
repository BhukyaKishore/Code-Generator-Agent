import logging
import os
from datetime import datetime
from pathlib import Path

# ============================================================================
# LOGGING CONFIGURATION
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
    # Reset handlers to avoid duplication if reloaded
    if root_logger.handlers:
        root_logger.handlers = []
        
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
