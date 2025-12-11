import logging
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from langchain_community.llms import LlamaCpp
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain import hub

from .config import MODEL_PATH, LANGUAGE_CONFIGS
from .llm import LocalLLM

logger = logging.getLogger(__name__)

class CodeGeneratorAgent:
    """Multi-language code generator agent with LangChain"""
    
    def __init__(self, model_path: str = MODEL_PATH):
        """Initialize the agent"""
        logger.info("="*80)
        logger.info("🤖 Initializing Code Generator Agent...")
        logger.info("="*80)
        
        self.local_llm = LocalLLM(model_path)
        self.is_ready = self.local_llm.is_available
        
        if not self.is_ready:
            logger.error("Agent initialization failed - model not available")
            logger.error("Running in FALLBACK mode - will use templates only")
            self.agent_executor = None
        else:
            # Create LangChain agent with tools
            self._setup_agent(model_path)
            logger.info("Agent ready and operational!")
    
    def _setup_agent(self, model_path: str):
        """Setup LangChain agent with tools"""
        
        # Define tools for the agent
        def code_generation_tool(input_str: str) -> str:
            """Generate code based on prompt and language"""
            try:
                parts = input_str.split("|", 1)
                if len(parts) == 2:
                    language, prompt = parts
                    language = language.strip().lower()
                    prompt = prompt.strip()
                else:
                    language = "python"
                    prompt = input_str.strip()
                
                result = self.generate_code(prompt, language)
                return result['code']
            except Exception as e:
                return f"Error generating code: {str(e)}"
        
        def language_info_tool(language: str) -> str:
            """Get information about supported languages"""
            if language.lower() in LANGUAGE_CONFIGS:
                config = LANGUAGE_CONFIGS[language.lower()]
                return f"Language: {config['name']}, Extension: {config['extension']}, Comment: {config['comment']}"
            else:
                supported = ", ".join(LANGUAGE_CONFIGS.keys())
                return f"Unsupported language. Supported languages: {supported}"
        
        # Create tool objects
        tools = [
            Tool(
                name="CodeGenerator",
                func=code_generation_tool,
                description="Generate code in specified language. Input format: 'language|prompt' (e.g., 'python|sort array') or just 'prompt' for Python"
            ),
            Tool(
                name="LanguageInfo",
                func=language_info_tool,
                description="Get information about a programming language. Input: language name"
            )
        ]
        
        try:
            # Initialize LLM for agent using LlamaCpp wrapper
            llm = LlamaCpp(
                model_path=model_path,
                n_ctx=4096,
                n_threads=8,
                n_gpu_layers=0,
                temperature=0.7,
                max_tokens=2000,
                verbose=False
            )
            
            # Get the ReAct prompt template
            prompt = hub.pull("hwchase17/react")
            
            # Create the agent
            agent = create_react_agent(llm, tools, prompt)
            
            # Create an agent executor
            self.agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                verbose=True,
                handle_parsing_errors=True
            )
            logger.info("✅ LangChain agent configured successfully")
        except Exception as e:
            logger.error(f"⚠️  Agent executor setup failed: {e}")
            self.agent_executor = None
    
    def generate_code(self, prompt: str, language: str = "python") -> Dict[str, Any]:
        """
        Generate code for given prompt and language
        
        Args:
            prompt: Description of code to generate
            language: Programming language (python, javascript, java, cpp, c, sql)
        
        Returns:
            Dictionary with generated code and metadata
        """
        
        if language not in LANGUAGE_CONFIGS:
            logger.warning(f"  Unsupported language: {language}, defaulting to Python")
            language = "python"
        
        logger.info(f" Generating {language} code")
        logger.info(f" Prompt: {prompt[:100]}...")
        
        code = self.local_llm.generate_with_self_consistency(prompt, language)
        
        status = "success" if self.is_ready else "fallback"
        logger.info(f" Code generation complete (status: {status})")
        
        return {
            "code": code,
            "language": language,
            "prompt": prompt,
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "model_available": self.is_ready
        }
    
    def run_agent(self, query: str) -> str:
        """Run the agent with a query"""
        if not self.agent_executor:
            return "Agent executor not available. Model not loaded or agent setup failed."
        
        try:
            result = self.agent_executor.invoke({"input": query})
            return result["output"]
        except Exception as e:
            logger.error(f" Agent execution error: {e}")
            return f"Error: {str(e)}"
    
    def health_check(self) -> Dict[str, Any]:
        """Check agent health status"""
        return {
            "status": "healthy" if self.is_ready else "degraded",
            "model_available": self.is_ready,
            "model_path": MODEL_PATH,
            "model_exists": os.path.exists(MODEL_PATH),
            "agent_executor_available": self.agent_executor is not None,
            "supported_languages": list(LANGUAGE_CONFIGS.keys()),
            "timestamp": datetime.now().isoformat()
        }
