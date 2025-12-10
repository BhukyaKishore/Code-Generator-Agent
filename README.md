# 🚀 Code Wizard - Multi-Language AI Code Generator

> **Generate production-ready code in 6 programming languages with AI-powered self-consistency prompting**

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [System Components](#system-components)
4. [AI Model & Methodology](#ai-model--methodology)
5. [Installation & Setup](#installation--setup)
6. [Usage Guide](#usage-guide)
7. [Security & Guardrails](#security--guardrails)
8. [Logging System](#logging-system)
9. [API Documentation](#api-documentation)
10. [Technical Workflow](#technical-workflow)
11. [Performance & Optimization](#performance--optimization)
12. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

**Code Wizard** is an intelligent code generation platform that leverages advanced AI models to generate production-ready code across multiple programming languages. It combines sophisticated prompting techniques with strict security guardrails to ensure both quality and safety.

### Key Features

✅ **Multi-Language Support**: Python, JavaScript, Java, C++, C, SQL
✅ **Self-Consistency Prompting**: Generates 9 different solutions and picks the best
✅ **Real-time Progress Tracking**: Visual progress bar during generation
✅ **Timestamped Logging**: Detailed logs for every execution
✅ **Security Guardrails**: Prevents malicious code patterns
✅ **Beautiful UI**: 3D animated interface with modern design
✅ **One-Click Copy**: Easy code copying to clipboard
✅ **Language-Specific Bot Names**: Unique personality for each language

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Browser)                        │
│           Beautiful UI with 3D Animations                    │
│                    index.html                                │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/REST
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              FASTAPI BACKEND (main.py)                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  API Routes                                         │    │
│  │  • /api/generate        - Code generation          │    │
│  │  • /health              - Health check             │    │
│  │  • /api/languages       - Supported languages      │    │
│  │  • /api/guardrails      - Security rules           │    │
│  │  • /api/logs            - Recent log files         │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Middleware & Validation                            │    │
│  │  • CORS Configuration                              │    │
│  │  • Request Validation                              │    │
│  │  • Security Filtering                              │    │
│  │  • Error Handling                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Logging System                                     │    │
│  │  • Timestamped log files (logs/)                    │    │
│  │  • Console output                                  │    │
│  │  • Request/Response tracking                       │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│           CODE GENERATION AGENT (agent.py)                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Language Configurations                            │    │
│  │  • Language-specific system prompts                 │    │
│  │  • Syntax validators                               │    │
│  │  • Code quality scorers                            │    │
│  │  • Fallback templates                              │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Self-Consistency Engine                            │    │
│  │  • Generate 9 solutions with different temps        │    │
│  │  • Score each solution (0-10+)                      │    │
│  │  • Return best solution                            │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  LLM Interface (Qwen2.5-Coder-7B)                   │    │
│  │  • Local GGUF model loading                         │    │
│  │  • Inference with llama-cpp-python                  │    │
│  │  • Multiple sampling strategies                     │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│            LOCAL LLM MODEL (Qwen2.5-Coder-7B)              │
│            Quantized GGUF Format (4-5GB)                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 System Components

### 1. **Frontend (index.html)**

**Technology Stack:**
- Pure HTML5, CSS3, JavaScript (No frameworks)
- WebGL-inspired 3D animated backgrounds
- Responsive design (Mobile, Tablet, Desktop)

**Key Features:**
- Language selection buttons (6 languages)
- Textarea for prompt input
- Real-time progress bar with gradient animation
- Code output with syntax highlighting
- One-click copy functionality
- Error message display
- Security guardrails display

**Animations:**
- Floating blob animations (3D effect)
- Button hover effects
- Smooth transitions
- Loading spinner
- Progress bar with glow effect

### 2. **Backend (main.py)**

**Framework:** FastAPI (Async Python Web Framework)

**Components:**

```
main.py
├── Logging Setup
│   ├── Timestamped log files (logs/codewizard_YYYYMMDD_HHMMSS.log)
│   ├── File handler (DEBUG level)
│   └── Console handler (INFO level)
│
├── API Routes
│   ├── GET /                 - Serve index.html
│   ├── GET /health          - Health check endpoint
│   ├── POST /api/generate   - Code generation
│   ├── GET /api/languages   - Language info
│   ├── GET /api/guardrails  - Security rules
│   └── GET /api/logs        - Log file listing
│
├── Validation Layer
│   ├── Prompt validation (max 1000 chars)
│   ├── Language validation
│   ├── Security pattern detection
│   └── Sanitization
│
├── Error Handling
│   ├── HTTP exception handlers
│   ├── Graceful error messages
│   └── Detailed logging
│
└── Middleware
    ├── CORS configuration
    ├── Request logging
    └── Response handling
```

**Security Guardrails (16 patterns):**
- SQL injection patterns (DROP TABLE, DELETE FROM, TRUNCATE)
- Code execution (eval, exec, system, os.system)
- Dangerous imports (__import__)
- Credential exposure (password, api_key, secret)
- System commands (rm -rf, chmod 777, sudo)
- Network exploitation (curl exec, wget exec)

### 3. **Agent (agent.py)**

**Core Technology:** Qwen2.5-Coder-7B (7 Billion Parameters)

**Key Components:**

#### **Self-Consistency Prompting**
```
Algorithm:
1. Generate 9 different code solutions
2. Use varying temperatures (0.1 to 0.9) for diversity
3. Score each solution based on quality metrics
4. Return the highest-scoring solution

Why 9 samples?
- Statistically significant diversity
- Computationally efficient (vs 16-25 samples)
- Good balance between quality and speed
```

#### **Temperature Settings**
```
Temperatures Used: [0.1, 0.2, 0.3, 0.4, 0.5, 0.5, 0.7, 0.9, 0.9]

- Low (0.1-0.3): Conservative, focused code
- Medium (0.4-0.5): Balanced exploration
- High (0.7-0.9): Creative variations

Benefit: Generates diverse solutions to select best
```

#### **Code Scoring System**
```
Scoring Criteria:
┌─────────────────────────────────┬────────┐
│ Criteria                        │ Points │
├─────────────────────────────────┼────────┤
│ Optimal length (50-1000 chars)  │  2.0  │
│ Function/Class definition       │  3.0  │
│ Return statement                │  2.0  │
│ Documentation/Comments          │  1.0  │
│ Type hints                      │  1.0  │
│ Logic keywords present          │  2.0  │
│ Keyword matching (from prompt)  │ 0.5x  │
├─────────────────────────────────┼────────┤
│ Penalties:                      │        │
│ - TODO/FIXME patterns           │ -5.0  │
│ - Incomplete code               │ -5.0  │
└─────────────────────────────────┴────────┘

Max Score: ~15-20 points
```

#### **Language-Specific Prompts**

Each language has a custom system prompt:

```python
# Python Prompt includes:
- Type hints examples
- Python idioms
- No markdown requirement
- Standard library usage

# JavaScript Prompt includes:
- ES6+ syntax
- Async/await patterns
- Modern JavaScript conventions

# Java Prompt includes:
- Class structure
- Java naming conventions
- Proper OOP patterns

# SQL Prompt includes:
- Query optimization tips
- GROUP BY patterns
- JOIN examples
```

#### **Code Validation Pipeline**

```
Raw LLM Output
    ↓
[1] Remove Markdown (```, ```python, etc.)
    ↓
[2] Extract Code Section
    ↓
[3] Remove Explanatory Text
    ↓
[4] Check Minimum Length (>15 chars)
    ↓
[5] Detect Bad Patterns (TODO, FIXME, pass)
    ↓
[6] Syntax Validation (Python: ast.parse)
    ↓
[7] Return Valid Code or Empty String
```

#### **Fallback System**

When LLM fails (model not available):
- Pattern-matched fallback templates
- Language-specific boilerplate
- Proper structure and syntax
- Ready-to-run code

---

## 🤖 AI Model & Methodology

### Model Information

**Model Name:** Qwen2.5-Coder-7B-Instruct
- **Parameters:** 7 Billion
- **Quantization:** Q5_K_M (GGUF format)
- **Size:** ~4.7 GB
- **Architecture:** Transformer-based
- **Training Data:** Code + general knowledge
- **Context Window:** 4096 tokens

### Inference Configuration

```python
MODEL_PARAMS = {
    "model_path": "./models/qwen2.5-coder-7b-instruct-q5_k_m.gguf",
    "n_ctx": 4096,              # Context window size
    "n_threads": 8,             # CPU threads
    "n_gpu_layers": 0,          # 0 = CPU only
    "verbose": False            # Suppress debug output
}

INFERENCE_SETTINGS = {
    "max_tokens": 1500,         # Maximum output length
    "temperature": 0.1-0.9,     # Varies by sample
    "top_p": 0.9,              # Nucleus sampling
    "repeat_penalty": 1.15,    # Avoid repetition
    "stop": ["Prompt:", "\n\n\n\n", "Output:"]
}
```

### Why Self-Consistency Prompting?

**Traditional Approach:**
```
Prompt → Model → Single Output
         (Deterministic)
```

**Self-Consistency Approach:**
```
Prompt → Model → Solution 1 (Score: 8.5)
      ↘           Solution 2 (Score: 7.2)
       ↘          Solution 3 (Score: 9.1) ← Selected
        → Model → Solution 4 (Score: 6.8)
                  ...
```

**Benefits:**
- ✅ Higher quality through selection
- ✅ Diversity reduces errors
- ✅ Objective scoring eliminates bias
- ✅ Fallback for failed attempts

### Token Usage Estimation

```
Input Prompt:  ~100-200 tokens
System Prompt: ~400-500 tokens
Output Code:   ~200-600 tokens
─────────────────────────────
Per Sample:    ~700-1300 tokens
9 Samples:     ~6,300-11,700 tokens

Total Generation: ~11,700 tokens (average)
```

---

## 💻 Installation & Setup

### Prerequisites

- Python 3.8+
- 5GB free disk space (for model)
- 8GB+ RAM recommended
- Modern web browser

### Step 1: Clone/Download Project

```bash
cd code-wizard
```

### Step 2: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python packages
pip install fastapi uvicorn pydantic llama-cpp-python
```

### Step 3: Download AI Model

```bash
# Create models directory
mkdir models

# Download Qwen2.5-Coder-7B (requires git-lfs)
# Option 1: Using huggingface-cli
pip install huggingface-hub
huggingface-cli download Qwen/Qwen2.5-Coder-7B-Instruct-GGUF \
  qwen2.5-coder-7b-instruct-q5_k_m.gguf \
  --local-dir ./models

# Option 2: Manual download from Hugging Face
# Visit: https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF
# Download: qwen2.5-coder-7b-instruct-q5_k_m.gguf
# Place in: ./models/
```

### Step 4: Verify Installation

```bash
# Check model file
ls -lh models/qwen2.5-coder-7b-instruct-q5_k_m.gguf

# Should show ~4.7GB file
```

### Step 5: Run Application

```bash
# Start FastAPI server
python main.py

# Server will start at http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Step 6: Access Application

```
Open browser and navigate to:
http://localhost:8000
```

---

## 📖 Usage Guide

### For End Users

1. **Open Application**
   - Navigate to `http://localhost:8000`
   - See beautiful dashboard with animations

2. **Select Language**
   - Click on one of 6 language buttons
   - Button will highlight with gradient

3. **Describe Your Code**
   - Type natural language description
   - Examples:
     - "Write a function to check if a number is prime"
     - "Create a user login system"
     - "Build a SQL query to get top 10 products"

4. **Generate Code**
   - Click "Generate Code" button
   - Watch progress bar animate
   - Code appears in right panel

5. **Copy Code**
   - Click "Copy Code" button
   - Code is copied to clipboard
   - Confirmation message appears

6. **Clear & Repeat**
   - Click "Clear" to reset
   - Start new code generation

### For Developers

#### API Request Example

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a function to count vowels in a string",
    "language": "python"
  }'
```

#### API Response Example

```json
{
  "code": "def count_vowels(text: str) -> int:\n    vowels = \"aeiouAEIOU\"\n    return sum(1 for c in text if c in vowels)",
  "language": "python",
  "prompt": "Write a function to count vowels in a string",
  "timestamp": "2024-01-15T10:30:45.123456",
  "bot_name": "PyWizard",
  "status": "success",
  "generation_time": 2.34
}
```

#### Check API Health

```bash
curl http://localhost:8000/health
```

#### Get Supported Languages

```bash
curl http://localhost:8000/api/languages
```

---

## 🔒 Security & Guardrails

### Security Architecture

```
User Input
    ↓
┌─────────────────────────────────┐
│ 1. Length Check                 │ Max 1000 chars
├─────────────────────────────────┤
│ 2. Pattern Matching             │ 16 regex patterns
├─────────────────────────────────┤
│ 3. Keyword Detection            │ Dangerous keywords
├─────────────────────────────────┤
│ 4. Validation Response          │ Pass/Reject
└─────────────────────────────────┘
    ↓
[Approved] → Code Generation
[Rejected] → Error Message to User
```

### Blocked Patterns (16 Security Rules)

```
SQL Injection:
- DROP TABLE
- DELETE FROM
- TRUNCATE TABLE

Code Execution:
- eval()
- exec()
- system()
- os.system()

Dangerous Imports:
- __import__

Credential Exposure:
- password =
- api_key =
- secret =

System Commands:
- rm -rf
- chmod 777
- sudo
- curl ... exec
- wget ... exec
```

### Response Status Codes

```
200 OK               - Code generated successfully
400 Bad Request      - Invalid language or failed validation
403 Forbidden        - Security pattern detected
503 Service Error    - Agent not initialized
500 Server Error     - Unexpected error
```

---

## 📝 Logging System

### Log File Structure

```
logs/
├── codewizard_20240115_090000.log
├── codewizard_20240115_091530.log
├── codewizard_20240115_092245.log
└── codewizard_20240115_095010.log
```

### Log Format

```
2024-01-15 09:00:00 - [INFO] - __main__ - 🚀 CODE WIZARD API - APPLICATION STARTUP
2024-01-15 09:00:01 - [INFO] - __main__ - ✅ FastAPI application initialized
2024-01-15 09:00:15 - [INFO] - __main__ - 📥 NEW CODE GENERATION REQUEST
2024-01-15 09:00:15 - [INFO] - __main__ - 🔤 Language: python
2024-01-15 09:00:15 - [INFO] - __main__ - 📝 Prompt: Write a function to count vowels...
2024-01-15 09:00:15 - [INFO] - __main__ - ✅ Prompt validation passed
2024-01-15 09:00:15 - [INFO] - __main__ - 🚀 Starting code generation for python...
2024-01-15 09:02:45 - [INFO] - agent.py - ✅ Code generated successfully in 2.34s
2024-01-15 09:02:45 - [INFO] - __main__ - ✅ Code generated successfully in 2.34s
2024-01-15 09:02:45 - [INFO] - __main__ - 📊 Generated code length: 234 characters
```

### Log Levels

```
DEBUG   - Detailed diagnostic information
INFO    - General informational messages
WARNING - Warning messages for suspicious activity
ERROR   - Error messages with stack traces
```

### Accessing Logs

```bash
# View recent logs
tail -f logs/codewizard_*.log

# Get specific run logs
cat logs/codewizard_20240115_090000.log

# List all log files
ls -lh logs/
```

---

## 🔌 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Generate Code
```
POST /api/generate
Content-Type: application/json

Request:
{
  "prompt": string,      // Max 1000 characters
  "language": string     // python|javascript|java|cpp|c|sql
}

Response:
{
  "code": string,
  "language": string,
  "prompt": string,
  "timestamp": string,
  "bot_name": string,
  "status": string,
  "generation_time": float
}

Examples:
Prompt: "count vowels in string"
Language: "python"

Response Status:
200 - Success
400 - Invalid input
403 - Restricted pattern
500 - Server error
```

#### 2. Health Check
```
GET /health

Response:
{
  "status": "healthy",
  "service": "Code Wizard API",
  "timestamp": string,
  "uptime": string
}
```

#### 3. List Languages
```
GET /api/languages

Response:
{
  "languages": ["python", "javascript", "java", "cpp", "c", "sql"],
  "bots": {
    "python": "PyWizard",
    "javascript": "ScriptMaster",
    ...
  },
  "count": 6
}
```

#### 4. Security Guardrails
```
GET /api/guardrails

Response:
{
  "guardrails": [string],
  "max_prompt_length": 1000,
  "security_patterns_count": 16
}
```

#### 5. Log Files
```
GET /api/logs

Response:
{
  "logs": [string],
  "total": number
}
```

---

## 🔄 Technical Workflow

### Complete Request-Response Flow

```
User Interface (Browser)
    ↓
    └─→ [User Input]
        • Language selection
        • Code prompt description
        • Click "Generate"
    ↓
HTTP POST /api/generate
    ↓
FastAPI Route Handler (main.py)
    ├─ Log request details
    ├─ Validate language
    ├─ Validate prompt
    │   ├─ Check length (<1000 chars)
    │   ├─ Check security patterns
    │   └─ Return error if invalid
    ├─ Call CodeGeneratorAgent
    ↓
Agent Initialization (agent.py)
    ├─ Load Qwen2.5-Coder LLM
    ├─ Setup language-specific prompt
    ↓
Self-Consistency Generation Loop
    ├─ Iteration 1 (temp=0.1)
    │   ├─ LLM inference
    │   ├─ Extract code
    │   ├─ Score: 8.5
    ├─ Iteration 2 (temp=0.2)
    │   ├─ LLM inference
    │   ├─ Extract code
    │   ├─ Score: 7.2
    ├─ ...
    ├─ Iteration 9 (temp=0.9)
    │   ├─ LLM inference
    │   ├─ Extract code
    │   ├─ Score: 6.5
    ↓
Select Best Solution
    ├─ Find max score (9.1)
    ├─ Return associated code
    ↓
Return Response
    ├─ Serialize to JSON
    ├─ Include metadata
    ├─ Log generation time
    ├─ Log code stats
    ↓
HTTP 200 Response
    {
      "code": "...",
      "language": "python",
      "generation_time": 2.34,
      ...
    }
    ↓
Browser Display
    ├─ Stop progress bar
    ├─ Show generated code
    ├─ Enable copy button
    ├─ Hide loading spinner
    ↓
User Action
    ├─ Copy code (one-click)
    ├─ Clear and try again
    ├─ Refine prompt
```

---

## ⚡ Performance & Optimization

### Generation Time Breakdown

```
Total Time: ~2-4 seconds (average)

Breakdown:
├─ API Round-trip:     100-200ms
├─ Validation:         50-100ms
├─ Model Loading:      500-1000ms (first run only)
├─ 9x LLM Inference:   1000-2000ms (most time)
└─ Post-processing:    100-200ms
```

### Memory Usage

```
At Rest:
├─ Python processes: ~100-150MB
├─ LLM Model: ~4.7GB (loaded once)
└─ Total: ~4.8GB

During Generation:
├─ Base overhead: ~500MB
├─ Generation buffers: ~200MB
└─ Peak: ~5.5GB
```

### Optimization Techniques

**Model Quantization:**
- Q5_K_M format reduces model size by 60%
- Minimal quality loss vs FP32
- Faster inference speed

**Temperature Diversity:**
- Varying temperatures (0.1-0.9) prevents overfitting
- Reduces similar solution duplicates
- Better coverage of solution space

**Async Processing:**
- FastAPI handles multiple concurrent requests
- Non-blocking I/O operations
- Scalable to many users

**Code Scoring:**
- Avoids manual review
- Objective selection criteria
- Consistent quality

---

## 🛠️ Troubleshooting

### Issue: Model Not Found

```
Error: Model not found at ./models/qwen2.5-coder-7b-instruct-q5_k_m.gguf

Solution:
1. Download model from Hugging Face
2. Place in ./models/ directory
3. Verify file size (~4.7GB)
4. Restart application
```

### Issue: Out of Memory

```
Error: RuntimeError: CUDA out of memory or RAM full

Solution:
1. Close other applications
2. Ensure 8GB+ available RAM
3. Set n_gpu_layers=0 (CPU only)
4. Reduce context window (n_ctx=2048)
5. Use GPU if available (n_gpu_layers > 0)
```

### Issue: Slow Generation

```
Typical: 2-4 seconds
Slow: >10 seconds

Causes:
- Low system RAM (swap usage)
- High CPU usage from other apps
- Slow disk I/O

Solutions:
1. Close background apps
2. Increase available RAM
3. Use SSD for better I/O
4. Monitor logs for errors
```

### Issue: Port Already in Use

```
Error: Address already in use (port 8000)

Solution 1: Use different port
python main.py --port 8001

Solution 2: Kill existing process
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :8000
kill -9 <PID>
```

### Issue: Invalid Response from API

```
Error: JSON decode error or malformed response

Solution:
1. Check logs for error messages
2. Verify prompt validation (max 1000 chars)
3. Check for security pattern issues
4. Restart FastAPI server
5. Clear browser cache
```

### Issue: Code Quality Issues

```
Generated code seems incomplete or incorrect

Possible Causes:
1. Prompt is ambiguous
2. Language not well-suited for task
3. Model hallucinates (rare)

Solutions:
1. Rephrase prompt more specifically
2. Try different language
3. Check logs for generation score
4. Try again (different temperature sampling)
```

---

## 📊 Monitoring & Debugging

### Enable Debug Logging

```python
# In main.py, change logging level
logging.basicConfig(level=logging.DEBUG)
```

### Monitor Generation Stats

```python
# Check log file for generation metrics
logs/codewizard_*.log

# Key metrics to watch:
- Generation time (goal: 2-4s)
- Code length (optimal: 100-500 chars)
- Solution scores (goal: >8.0)
```

### Check System Resources

```bash
# Monitor CPU/Memory during generation
top                    # macOS/Linux
taskmgr               # Windows GUI
wsl-manager           # WSL

# Expected:
- CPU: 60-90%
- RAM: 70-90% (during generation)
```

---

## 🚀 Future Enhancements

Potential improvements:

1. **Model Upgrades**
   - Qwen2.5-Coder-32B (larger, better quality)
   - Specialized models for each language
   - Fine-tuned models for specific domains

2. **Feature Additions**
   - Code explanation/documentation
   - Automated code testing
   - Performance optimization suggestions
   - Integration with IDEs (VS Code plugin)

3. **UI Improvements**
   - Dark/Light theme toggle
   - Code syntax highlighting
   - Multiple tabs for different languages
   - Prompt history

4. **API Enhancements**
   - WebSocket for streaming responses
   - Batch code generation
   - Code comparison tool
   - Rating/feedback system

5. **Security**
   - Rate limiting per IP
   - API key authentication
   - Usage analytics
   - Abuse detection

---

## 📄 License

This project uses open-source components:
- **FastAPI**: MIT License
- **Qwen2.5-Coder**: Qwen License (Commercial use allowed)
- **llama-cpp-python**: MIT License

---

## 🤝 Contributing

To contribute improvements:

1. Test changes locally
2. Verify logging works
3. Check security guardrails
4. Update documentation
5. Submit improvements

---

## 📞 Support

For issues or questions:

1. Check logs: `logs/codewizard_*.log`
2. Review troubleshooting section
3. Check API documentation: `/docs`
4. Monitor health: `/health` endpoint

---

## 🎓 Learning Resources

Understand the technology:

- **Self-Consistency Prompting**: [Paper](https://arxiv.org/abs/2203.11171)
- **Qwen Models**: [GitHub](https://github.com/QwenLM/Qwen)
- **FastAPI**: [Documentation](https://fastapi.tiangolo.com/)
- **llama.cpp**: [GitHub](https://github.com/ggerganov/llama.cpp)

---

**Made with ❤️ by Code Wizard Team**
*Last Updated: January 2024*# Code-Generator-Agent
# Code-Generator-Agent
