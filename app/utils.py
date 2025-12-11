import re
import logging
from .config import SUPPORTED_LANGUAGES

logger = logging.getLogger(__name__)

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
