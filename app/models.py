from pydantic import BaseModel
from typing import Optional

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
