import os
import logging
from llama_cpp import Llama
from .config import MODEL_PATH, MODEL_PARAMS, NUM_SAMPLES, TEMPERATURES
from .prompts import SYSTEM_PROMPTS

logger = logging.getLogger(__name__)

class LocalLLM:
    """Interface to Qwen2.5-Coder-7B with Self-Consistency"""
    
    def __init__(self, model_path: str = MODEL_PATH):
        """Initialize the local model"""
        logger.info(f" Checking model at {model_path}...")
        
        # Check if model file exists
        if not os.path.exists(model_path):
            logger.error(f"Model file not found at: {model_path}")
            logger.error(f"Please ensure the model file exists in the correct location")
            logger.info(f"Download from: https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF")
            self.llm = None
            self.is_available = False
            return
        
        # Check file size
        file_size_gb = os.path.getsize(model_path) / (1024**3)
        logger.info(f"Model file size: {file_size_gb:.2f} GB")
        
        if file_size_gb < 3.0:
            logger.warning(f"  Model file seems too small ({file_size_gb:.2f} GB). It may be corrupted.")
        
        try:
            logger.info(" Loading model... This may take 1-2 minutes...")
            self.llm = Llama(**MODEL_PARAMS)
            self.is_available = True
            logger.info(" Model loaded successfully!")
        except Exception as e:
            logger.error(f" Error loading model: {e}")
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
            logger.warning("  LLM not available, using fallback template")
            return self._fallback_code(prompt, language)
        
        logger.info(f"Generating {num_samples} {language} solutions...")
        
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
                    logger.info(f"Sample {i+1}/{num_samples} generated (score: {score:.2f})")
            
            except Exception as e:
                logger.warning(f"Sample {i+1} failed: {e}")
                continue
        
        if not solutions:
            logger.warning("All samples failed, using fallback template")
            return self._fallback_code(prompt, language)
        
        best = max(solutions, key=lambda x: x['score'])
        logger.info(f" Best solution: Sample {best['sample']} (score: {best['score']:.2f})")
        
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
