"""
Multi-Language Code Generator Agent with Local Qwen Model
Supports: Python, JavaScript, Java, C++, C, SQL
Uses Self-Consistency Prompting for high-quality code generation
"""

import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from dotenv import load_dotenv
from llama_cpp import Llama
from langchain_community.llms import LlamaCpp
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain import hub

# Load environment variables
load_dotenv()

# ============================================================================
# LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

MODEL_PATH = "./models/qwen2.5-coder-7b-instruct-q5_k_m.gguf"

MODEL_PARAMS = {
    "model_path": MODEL_PATH,
    "n_ctx": 4096,
    "n_threads": 8,
    "n_gpu_layers": 0,
    "verbose": False
}

NUM_SAMPLES = 9
TEMPERATURES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.5, 0.7, 0.9, 0.9]

# ============================================================================
# LANGUAGE-SPECIFIC CONFIGURATIONS
# ============================================================================

LANGUAGE_CONFIGS = {
    "python": {
        "name": "Python",
        "extension": ".py",
        "comment": "#",
        "syntax_check": "import ast; ast.parse(code)"
    },
    "javascript": {
        "name": "JavaScript",
        "extension": ".js",
        "comment": "//",
        "syntax_check": "basic"
    },
    "java": {
        "name": "Java",
        "extension": ".java",
        "comment": "//",
        "syntax_check": "basic"
    },
    "cpp": {
        "name": "C++",
        "extension": ".cpp",
        "comment": "//",
        "syntax_check": "basic"
    },
    "c": {
        "name": "C",
        "extension": ".c",
        "comment": "//",
        "syntax_check": "basic"
    },
    "sql": {
        "name": "SQL",
        "extension": ".sql",
        "comment": "--",
        "syntax_check": "basic"
    }
}

# ============================================================================
# SYSTEM PROMPTS FOR EACH LANGUAGE
# ============================================================================

SYSTEM_PROMPTS = {
    "python": """You are an expert Python programmer. Generate complete, working Python code.

STRICT RULES:
- Output ONLY executable Python code
- NO explanations, NO markdown (```), NO text
- Start with 'def', 'class', or 'import'
- Write complete functions with proper logic
- NO placeholders like "TODO" or "pass"
- Use type hints when possible

EXAMPLES:

Prompt: count vowels in string
Output:
def count_vowels(text: str) -> int:
    vowels = "aeiouAEIOU"
    return sum(1 for c in text if c in vowels)

Prompt: check if number is prime
Output:
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True""",

    "javascript": """You are an expert JavaScript programmer. Generate complete, working JavaScript code.

STRICT RULES:
- Output ONLY executable JavaScript code
- NO explanations, NO markdown, NO text
- Start with 'function', 'const', 'class', or 'var'
- Write complete functions with proper logic
- NO placeholders or incomplete code
- Use modern ES6+ syntax

EXAMPLES:

Prompt: count vowels in string
Output:
function countVowels(text) {
    const vowels = "aeiouAEIOU";
    return [...text].filter(c => vowels.includes(c)).length;
}

Prompt: check if number is prime
Output:
function isPrime(n) {
    if (n < 2) return false;
    if (n === 2) return true;
    if (n % 2 === 0) return false;
    for (let i = 3; i <= Math.sqrt(n); i += 2) {
        if (n % i === 0) return false;
    }
    return true;
}""",

    "java": """You are an expert Java programmer. Generate complete, working Java code.

STRICT RULES:
- Output ONLY executable Java code
- NO explanations, NO markdown, NO text
- Include proper class structure
- Follow Java naming conventions
- NO placeholders or incomplete code

EXAMPLES:

Prompt: count vowels in string
Output:
public class VowelCounter {
    public static int countVowels(String text) {
        int count = 0;
        String vowels = "aeiouAEIOU";
        for (char c : text.toCharArray()) {
            if (vowels.indexOf(c) != -1) count++;
        }
        return count;
    }
}

Prompt: check if number is prime
Output:
public class PrimeChecker {
    public static boolean isPrime(int n) {
        if (n < 2) return false;
        if (n == 2) return true;
        if (n % 2 == 0) return false;
        for (int i = 3; i <= Math.sqrt(n); i += 2) {
            if (n % i == 0) return false;
        }
        return true;
    }
}""",

    "cpp": """You are an expert C++ programmer. Generate complete, working C++ code.

STRICT RULES:
- Output ONLY executable C++ code
- NO explanations, NO markdown, NO text
- Include necessary headers (#include)
- Write complete functions with proper logic
- NO placeholders or incomplete code

EXAMPLES:

Prompt: count vowels in string
Output:
#include <string>
#include <cctype>
using namespace std;

int countVowels(const string& text) {
    int count = 0;
    string vowels = "aeiouAEIOU";
    for (char c : text) {
        if (vowels.find(c) != string::npos) count++;
    }
    return count;
}

Prompt: check if number is prime
Output:
#include <cmath>
using namespace std;

bool isPrime(int n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    for (int i = 3; i <= sqrt(n); i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}""",

    "c": """You are an expert C programmer. Generate complete, working C code.

STRICT RULES:
- Output ONLY executable C code
- NO explanations, NO markdown, NO text
- Include necessary headers (#include)
- Write complete functions with proper logic
- NO placeholders or incomplete code

EXAMPLES:

Prompt: count vowels in string
Output:
#include <stdio.h>
#include <string.h>

int countVowels(const char* text) {
    int count = 0;
    const char* vowels = "aeiouAEIOU";
    for (int i = 0; text[i]; i++) {
        if (strchr(vowels, text[i])) count++;
    }
    return count;
}

Prompt: check if number is prime
Output:
#include <math.h>

int isPrime(int n) {
    if (n < 2) return 0;
    if (n == 2) return 1;
    if (n % 2 == 0) return 0;
    for (int i = 3; i <= sqrt(n); i += 2) {
        if (n % i == 0) return 0;
    }
    return 1;
}""",

    "sql": """You are an expert SQL specialist. Generate complete, working SQL queries.

STRICT RULES:
- Output ONLY executable SQL code
- NO explanations, NO markdown, NO text
- Write complete queries with proper syntax
- NO placeholders or incomplete code
- Follow SQL best practices

EXAMPLES:

Prompt: select all users
Output:
SELECT * FROM users
WHERE status = 'active'
ORDER BY created_at DESC
LIMIT 100;

Prompt: count records by category
Output:
SELECT 
    category,
    COUNT(*) as count,
    AVG(price) as avg_price
FROM products
GROUP BY category
ORDER BY count DESC;"""
}

# ============================================================================
# LOCAL LLM WITH SELF-CONSISTENCY
# ============================================================================

class LocalLLM:
    """Interface to Qwen2.5-Coder-7B with Self-Consistency"""
    
    def __init__(self, model_path: str = MODEL_PATH):
        """Initialize the local model"""
        logger.info(f"🔍 Checking model at {model_path}...")
        
        # Check if model file exists
        if not os.path.exists(model_path):
            logger.error(f"❌ Model file not found at: {model_path}")
            logger.error(f"📁 Please ensure the model file exists in the correct location")
            logger.info(f"💡 Download from: https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF")
            self.llm = None
            self.is_available = False
            return
        
        # Check file size
        file_size_gb = os.path.getsize(model_path) / (1024**3)
        logger.info(f"📦 Model file size: {file_size_gb:.2f} GB")
        
        if file_size_gb < 3.0:
            logger.warning(f"⚠️  Model file seems too small ({file_size_gb:.2f} GB). It may be corrupted.")
        
        try:
            logger.info("⏳ Loading model... This may take 1-2 minutes...")
            self.llm = Llama(**MODEL_PARAMS)
            self.is_available = True
            logger.info("✅ Model loaded successfully!")
        except Exception as e:
            logger.error(f"❌ Error loading model: {e}")
            logger.error("Possible issues:")
            logger.error("  1. Insufficient RAM (need ~8GB for 7B model)")
            logger.error("  2. Corrupted model file - try re-downloading")
            logger.error("  3. Incompatible model format")
            self.llm = None
            self.is_available = False
    
    def generate_with_self_consistency(
        self, 
        prompt: str, 
        language: str,
        num_samples: int = NUM_SAMPLES
    ) -> str:
        """Generate code using self-consistency prompting"""
        
        if not self.is_available or not self.llm:
            logger.warning("⚠️  LLM not available, using fallback template")
            return self._fallback_code(prompt, language)
        
        logger.info(f"🚀 Generating {num_samples} {language} solutions...")
        
        solutions = []
        system_prompt = SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS["python"])
        
        for i in range(num_samples):
            temp = TEMPERATURES[i % len(TEMPERATURES)]
            
            full_prompt = f"""{system_prompt}

Prompt: {prompt}
Output:"""
            
            try:
                response = self.llm(
                    full_prompt,
                    max_tokens=1500,
                    temperature=temp,
                    top_p=0.9,
                    repeat_penalty=1.15,
                    echo=False,
                    stop=["Prompt:", "\n\n\n\n"]
                )
                
                code = self._extract_code(response['choices'][0]['text'].strip(), language)
                
                if code:
                    score = self._score_code(code, prompt, language)
                    solutions.append({
                        'code': code,
                        'score': score,
                        'sample': i + 1
                    })
                    logger.info(f"✓ Sample {i+1}/{num_samples} generated (score: {score:.2f})")
            
            except Exception as e:
                logger.warning(f"⚠️  Sample {i+1} failed: {e}")
                continue
        
        if not solutions:
            logger.warning("⚠️  All samples failed, using fallback template")
            return self._fallback_code(prompt, language)
        
        best = max(solutions, key=lambda x: x['score'])
        logger.info(f"🏆 Best solution: Sample {best['sample']} (score: {best['score']:.2f})")
        
        return best['code']
    
    def _extract_code(self, response: str, language: str) -> str:
        """Extract valid code from response"""
        
        if not response:
            return ""
        
        # Remove markdown
        for marker in ["```python", "```javascript", "```java", "```cpp", "```c", "```sql", "```"]:
            if marker in response:
                start = response.find(marker) + len(marker)
                end = response.find("```", start)
                if end != -1:
                    response = response[start:end].strip()
        
        lines = response.split('\n')
        code_lines = []
        found_code = False
        
        for line in lines:
            if not found_code:
                if any(line.strip().startswith(kw) for kw in ['def ', 'class ', 'function', 'import ', 'from ', 'public ', '#include', 'SELECT', 'CREATE']):
                    found_code = True
                else:
                    continue
            code_lines.append(line)
        
        code = '\n'.join(code_lines).strip()
        
        if not code or len(code) < 15:
            return ""
        
        bad_patterns = ['TODO', 'FIXME', 'placeholder', 'implement', 'pass  #']
        if any(p.lower() in code.lower() for p in bad_patterns):
            return ""
        
        if language == "python":
            try:
                import ast
                ast.parse(code)
                return code
            except SyntaxError:
                return ""
        
        return code
    
    def _score_code(self, code: str, prompt: str, language: str) -> float:
        """Score code quality"""
        
        score = 0.0
        length = len(code)
        
        if 50 < length < 1000:
            score += 2.0
        elif 30 < length < 1500:
            score += 1.0
        
        if 'def ' in code or 'function' in code or 'class ' in code:
            score += 3.0
        
        if 'return ' in code:
            score += 2.0
        
        if '"""' in code or "'''" in code or '//' in code or '--' in code:
            score += 1.0
        
        logic_keywords = ['if ', 'for ', 'while ', 'try:', 'with ', 'SELECT', 'WHERE']
        if any(kw in code for kw in logic_keywords):
            score += 2.0
        
        for pattern in ['TODO', 'FIXME', 'pass\n', '...']:
            if pattern in code:
                score -= 5.0
        
        prompt_words = [w for w in prompt.lower().split() if len(w) > 3]
        code_lower = code.lower()
        matches = sum(1 for word in prompt_words if word in code_lower)
        score += matches * 0.5
        
        return max(0.0, score)
    
    def _fallback_code(self, prompt: str, language: str) -> str:
        """Generate fallback code based on language templates"""
        
        templates = {
            "python": f'''# {prompt}
def main():
    """Main function"""
    # Implementation here
    pass

if __name__ == "__main__":
    main()''',
            
            "javascript": f'''// {prompt}
function main() {{
    // Implementation here
    return result;
}}

main();''',
            
            "java": f'''// {prompt}
public class Solution {{
    public static void main(String[] args) {{
        // Implementation here
    }}
}}''',
            
            "cpp": f'''// {prompt}
#include <iostream>
using namespace std;

int main() {{
    // Implementation here
    return 0;
}}''',
            
            "c": f'''// {prompt}
#include <stdio.h>

int main() {{
    // Implementation here
    return 0;
}}''',
            
            "sql": f'''-- {prompt}
SELECT * FROM table_name
WHERE condition = true
LIMIT 10;'''
        }
        
        return templates.get(language, templates["python"])

# ============================================================================
# CODE GENERATOR AGENT
# ============================================================================

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
            logger.error("❌ Agent initialization failed - model not available")
            logger.error("🔧 Running in FALLBACK mode - will use templates only")
            self.agent_executor = None
        else:
            # Create LangChain agent with tools
            self._setup_agent(model_path)
            logger.info("✅ Agent ready and operational!")
    
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
            logger.warning(f"⚠️  Unsupported language: {language}, defaulting to Python")
            language = "python"
        
        logger.info(f"🚀 Generating {language} code")
        logger.info(f"📝 Prompt: {prompt[:100]}...")
        
        code = self.local_llm.generate_with_self_consistency(prompt, language)
        
        status = "success" if self.is_ready else "fallback"
        logger.info(f"✅ Code generation complete (status: {status})")
        
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
            logger.error(f"❌ Agent execution error: {e}")
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

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Initialize agent
    agent = CodeGeneratorAgent()
    
    # Health check
    health = agent.health_check()
    print("\n" + "="*80)
    print("🏥 HEALTH CHECK")
    print("="*80)
    for key, value in health.items():
        print(f"{key}: {value}")
    
    if not agent.is_ready:
        print("\n⚠️  WARNING: Agent running in FALLBACK mode")
        print("Generated code will be templates only")
        print("\nTo fix:")
        print(f"1. Download model to: {MODEL_PATH}")
        print("2. Ensure model file is complete (~5GB)")
        print("3. Restart the agent")
    else:
        # Example usage
        print("\n" + "="*80)
        print("📝 EXAMPLE: Code Generation")
        print("="*80 + "\n")
        
        result = agent.generate_code(
            prompt="create a function to check if a string is palindrome",
            language="python"
        )
        
        print(f"Language: {result['language']}")
        print(f"Status: {result['status']}")
        print(f"Prompt: {result['prompt']}")
        print(f"\nGenerated Code:\n{'-'*80}\n{result['code']}\n{'-'*80}")