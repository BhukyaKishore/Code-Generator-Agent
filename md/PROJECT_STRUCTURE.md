# Code Wizard - Project Structure & Files

## 📁 Complete File Organization

```
code-wizard/
├── 📄 main.py                          # FastAPI backend with routes
├── 📄 agent.py                         # AI agent for code generation
├── 🌐 index.html                       # Frontend UI with 3D animations
│
├── 📋 requirements.txt                 # Python package dependencies
├── 🔧 setup.sh                         # Automated setup script (Linux/macOS)
├── 🔧 setup.bat                        # Automated setup script (Windows)
│
├── 📚 README.md                        # Complete project documentation
├── 📚 PROJECT_STRUCTURE.md             # This file
│
├── 📁 logs/                            # Generated log files
│   ├── codewizard_20240115_090000.log
│   ├── codewizard_20240115_091530.log
│   └── codewizard_20240115_092245.log
│
├── 📁 models/                          # AI Model storage
│   └── qwen2.5-coder-7b-instruct-q5_k_m.gguf (4.7GB)
│
└── 📁 venv/                            # Python virtual environment
    ├── bin/
    ├── lib/
    └── pyvenv.cfg
```

---

## 📄 File Descriptions

### 1. **main.py** (FastAPI Backend)
**Size:** ~8KB  
**Lines:** ~400

**Purpose:** RESTful API server handling HTTP requests

**Key Components:**
```python
- Logging setup with timestamped files
- FastAPI application and middleware
- Request/Response models (Pydantic)
- API routes (generate, health, languages, guardrails, logs)
- Security validation layer
- Error handling
- Startup/shutdown events
```

**Key Functions:**
```
setup_logging()           → Creates timestamped log files
validate_prompt()         → Security pattern detection
validate_language()       → Language support check
generate_code()           → Main endpoint (POST /api/generate)
health_check()           → Health status endpoint
get_languages()          → List supported languages
get_guardrails()         → Security rules info
get_recent_logs()        → Log file listing
```

**Logging Output:**
```
logs/codewizard_20240115_090000.log
- Each run creates a new file
- Timestamp format: YYYYMMDD_HHMMSS
- Detailed request/response logging
- Security event logging
- Generation time tracking
```

---

### 2. **agent.py** (Code Generation Agent)
**Size:** ~12KB  
**Lines:** ~550

**Purpose:** AI-powered code generation with self-consistency prompting

**Key Components:**
```python
- LocalLLM class (Qwen2.5-Coder interface)
- CodeGeneratorAgent class
- Language-specific configurations
- System prompts for each language
- Code scoring algorithm
- Self-consistency generation loop
- Fallback templates
- Code validation pipeline
```

**Key Classes:**
```
LocalLLM:
  - __init__()                           → Load GGUF model
  - generate_with_self_consistency()    → 9-sample generation
  - _generate_single()                  → Single LLM call
  - _extract_code()                     → Parse output
  - _score_code()                       → Quality scoring
  - _fallback_code()                    → Backup templates

CodeGeneratorAgent:
  - __init__()                           → Initialize LLM
  - generate_code()                     → Main API call
```

**Supported Languages:**
```
"python"      → PyWizard (Python)
"javascript"  → ScriptMaster (JavaScript)
"java"        → ByteForge (Java)
"cpp"         → CppNinja (C++)
"c"           → CChain (C)
"sql"         → DataAlchemy (SQL)
```

**Self-Consistency Algorithm:**
```
For each of 9 iterations:
  1. Set temperature (0.1 to 0.9)
  2. Call LLM with system + user prompt
  3. Extract code from response
  4. Validate code syntax
  5. Score code quality
  6. Store: {code, score, sample_num}

Select best:
  best = max(solutions, key=score)
  return best['code']
```

**Scoring Criteria (Max ~15 points):**
```
Optimal length (50-1000 chars)  → +2.0 pts
Function/Class definition       → +3.0 pts
Return statement                → +2.0 pts
Comments/Documentation          → +1.0 pts
Type hints                       → +1.0 pts
Logic keywords (if, for, etc)   → +2.0 pts
Prompt keyword matching         → +0.5 pts per match
─────────────────────────────────────────
Penalties:
- TODO/FIXME patterns           → -5.0 pts
- Incomplete code               → -5.0 pts
```

---

### 3. **index.html** (Frontend UI)
**Size:** ~18KB  
**Lines:** ~650

**Purpose:** Beautiful user interface with animations and 3D effects

**Key Sections:**
```html
- HTML5 structure
- CSS3 styling (custom properties, gradients, animations)
- JavaScript event handlers (no frameworks)
- 3D blob animations
- Progress bar with gradient
- Language selector buttons
- Code editor textarea
- Code output display
- Copy functionality
```

**Technology Stack:**
```
HTML5:
  - Semantic markup
  - Accessible form elements
  - Responsive layout

CSS3:
  - Custom properties (--primary, --secondary, etc)
  - Gradient backgrounds
  - Animations (@keyframes)
  - Backdrop filters (glassmorphism)
  - Responsive grid layout

JavaScript:
  - Fetch API for HTTP requests
  - Event listeners
  - DOM manipulation
  - State management (local state object)
  - Timer-based animations
  - Clipboard API
```

**Animation Effects:**
```
Blob Animations:
  - 3 floating gradient blobs
  - 8-12 second animation cycles
  - Mix blend mode (multiply)
  - Staggered delays

Button Effects:
  - Hover: scale up (1.05)
  - Hover: shadow glow
  - Active: scale down (0.95)
  - Disabled: opacity 0.6

Progress Bar:
  - Gradient fill
  - Smooth width transition
  - Glow shadow effect
  - Incremental fill on load

Text Effects:
  - Gradient text (background-clip)
  - Fade-in animations
  - Slide-in transitions
```

**Features:**
```
Language Selection:
  - 6 button grid (responsive)
  - Active state highlight
  - Icon + label per language
  - Personality (PyWizard, etc)

Code Input:
  - Textarea with placeholder examples
  - Max 1000 character validation
  - Focus effects
  - Character counter

Code Output:
  - Scrollable code display
  - Syntax highlighting via CSS
  - Copy button with feedback
  - Clear button to reset

Progress Bar:
  - Visible during generation
  - Animated fill (0-100%)
  - Glow effect
  - Smooth transitions
```

---

### 4. **requirements.txt** (Dependencies)
**Size:** ~1KB

**Purpose:** Python package specifications for pip

**Packages:**
```
fastapi==0.104.1              # Web framework
uvicorn==0.24.0               # ASGI server
python-multipart==0.0.6       # Multipart form handling
pydantic==2.5.0               # Data validation
pydantic-core==2.14.1         # Pydantic core
llama-cpp-python==0.2.19      # LLM inference
python-dotenv==1.0.0          # Environment variables
typing-extensions==4.8.0      # Type hints
numpy==1.24.3                 # Numerical arrays (optional)
huggingface-hub==0.19.4       # Model downloading (optional)
```

**Installation:**
```bash
pip install -r requirements.txt
```

---

### 5. **setup.sh** (Linux/macOS Setup)
**Size:** ~3KB
**Purpose:** Automated environment setup

**Steps:**
```
1. Check Python version
2. Create virtual environment
3. Activate venv
4. Upgrade pip
5. Install dependencies
6. Create log/ and models/ directories
7. Verify installation
8. Display next steps
```

**Usage:**
```bash
chmod +x setup.sh
./setup.sh
```

---

### 6. **setup.bat** (Windows Setup)
**Size:** ~3KB
**Purpose:** Automated environment setup for Windows

**Steps:**
```
1. Check Python version
2. Create virtual environment
3. Activate venv
4. Upgrade pip
5. Install dependencies
6. Create logs\ and models\ directories
7. Verify installation
8. Display next steps
```

**Usage:**
```
setup.bat
```

---

### 7. **README.md** (Main Documentation)
**Size:** ~45KB
**Lines:** ~1500+

**Contents:**
```
- Overview & features
- Complete architecture diagram
- System components breakdown
- AI model information
- Installation & setup guide
- Usage instructions (user & dev)
- Security & guardrails
- Logging system details
- API documentation (all endpoints)
- Technical workflow diagrams
- Performance metrics
- Troubleshooting guide
- Monitoring & debugging
- Future enhancements
- Learning resources
```

**Sections:**
1. Overview
2. Architecture
3. System Components (Frontend, Backend, Agent)
4. AI Model & Methodology
5. Installation & Setup
6. Usage Guide
7. Security & Guardrails
8. Logging System
9. API Documentation
10. Technical Workflow
11. Performance & Optimization
12. Troubleshooting
13. Learning Resources

---

### 8. **PROJECT_STRUCTURE.md** (This File)
**Purpose:** File organization and descriptions

**Contents:**
```
- Complete directory structure
- File descriptions and purposes
- Component relationships
- Data flow diagrams
- Technology stack overview
```

---

## 🔄 Data Flow

```
User → index.html
     ↓
[User Input: Language + Prompt]
     ↓
JavaScript Fetch API
     ↓
POST /api/generate
     ↓
main.py::generate_code()
     ├─ Validate language
     ├─ Validate prompt
     ├─ Log request
     ├─ Call agent.generate_code()
     │   ├─ Load LLM model
     │   ├─ Self-consistency loop (9x)
     │   │   ├─ Generate with temperature
     │   │   ├─ Extract code
     │   │   └─ Score quality
     │   ├─ Select best solution
     │   └─ Log generation stats
     └─ Return response
         └─ JSON: {code, language, time, bot_name}
     ↓
JavaScript receives response
     ↓
[Display code + stop progress bar]
     ↓
User → Copy Code → Clipboard
```

---

## 📊 File Statistics

```
Project Size Breakdown:

Source Code:
  - main.py          ~8 KB  (~400 lines)
  - agent.py         ~12 KB (~550 lines)
  - index.html       ~18 KB (~650 lines)
  ────────────────────────────
  Total Code:        ~38 KB (~1600 lines)

Documentation:
  - README.md        ~45 KB (~1500 lines)
  - PROJECT_STRUCTURE.md  ~8 KB (~300 lines)
  ────────────────────────────
  Total Docs:        ~53 KB (~1800 lines)

Configuration:
  - requirements.txt  ~1 KB  (~25 lines)
  - setup.sh         ~3 KB  (~90 lines)
  - setup.bat        ~3 KB  (~90 lines)
  ────────────────────────────
  Total Config:      ~7 KB  (~205 lines)

────────────────────────────────
Project Total:       ~98 KB (~3605 lines)

Models:
  - qwen2.5-coder-7b (GGUF)  ~4.7 GB

Logs Generated Per Run:
  - Per execution: ~5-15 KB
  - 30 days: ~150-450 MB (at 1 run/hour)
```

---

## 🔗 Component Relationships

```
Frontend (index.html)
    ↓
    └─ Makes API calls to:
       ├─ main.py::generate_code()
       ├─ main.py::get_languages()
       └─ main.py::health_check()

main.py
    ├─ Imports: agent.py::CodeGeneratorAgent
    ├─ Uses: pydantic (validation)
    ├─ Uses: fastapi (routing)
    ├─ Generates: logs/codewizard_*.log
    └─ Handles HTTP requests

agent.py
    ├─ Uses: llama-cpp-python (LLM inference)
    ├─ Loads: models/qwen2.5-coder-7b-instruct-q5_k_m.gguf
    ├─ Generates: logs/agent.log
    └─ Returns: Generated code

Logs:
    ├─ main.py → logs/codewizard_TIMESTAMP.log
    ├─ agent.py → logs/agent.log
    └─ Accessible via GET /api/logs
```

---

## 🚀 Deployment Structure

```
Production Deployment:

├── Code Files
│   ├── main.py (API backend)
│   ├── agent.py (AI logic)
│   └── index.html (frontend)
│
├── Configuration
│   ├── requirements.txt
│   └── .env (environment variables)
│
├── Data Directories
│   ├── logs/ (readable/writable)
│   └── models/ (readable)
│
├── Virtual Environment
│   └── venv/
│
└── Process
    └── gunicorn / uvicorn (production ASGI server)
```

---

## 📝 Summary

**Total Files:** 8 main files
- 3 source code files
- 2 documentation files
- 3 configuration/setup files

**Total Lines of Code:** ~1,600
**Total Documentation:** ~1,800 lines
**Model Size:** 4.7 GB (loaded once)
**Memory Usage:** ~5.5 GB during generation
**Generation Time:** 2-4 seconds (average)

---

*Last Updated: January 2024*
*Version: 1.0.0*