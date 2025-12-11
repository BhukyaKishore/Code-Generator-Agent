import uvicorn
from app import app

if __name__ == "__main__":
    import uvicorn
    import logging
    
    # Configure logging for uvicorn to match our app's logging if needed
    # But for now, we rely on app's logging configuration
    
    print("🔥 Starting FastAPI server...")
    print("🌐 Server: http://0.0.0.0:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
