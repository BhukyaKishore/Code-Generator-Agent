import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
