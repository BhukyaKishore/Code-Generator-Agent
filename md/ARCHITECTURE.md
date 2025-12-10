# Code Wizard - Complete Architecture & Technical Design

---

## 🏗️ High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          CLIENT LAYER                           │
│                     Modern Web Browser                          │
│                    (Chrome, Firefox, Safari)                    │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                    HTTP/REST API (JSON)
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                            │
│                      FastAPI Server                             │
│   ┌────────────────────────────────────────────────────────┐   │
│   │ • Request Routing & Validation                         │   │
│   │ • Security Guardrails                                  │   │
│   │ • Error Handling                                       │   │
│   │ • Logging & Monitoring                                 │   │
│   └────────────────────────────────────────────────────────┘   │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                    Python Object Interface
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INTELLIGENCE LAYER                           │
│                  Code Generator Agent                           │
│   ┌────────────────────────────────────────────────────────┐   │
│   │ Self-Consistency Generation Engine                     │   │
│   │ • 9x LLM Sampling                                     │   │
│   │ • Quality Scoring                                      │   │
│   │ • Code Validation                                      │   │
│   └────────────────────────────────────────────────────────┘   │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                    GGUF Model Inference
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MODEL LAYER                                │
│           Qwen2.5-Coder-7B (GGUF Quantized)                    │
│              4.7GB Local Model File                             │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ Transformer Architecture                               │   │
│  │ • 7 Billion Parameters                                 │   │
│  │ • 4096 Token Context Window                            │   │
│  │ • Trained on Code + General Knowledge                  │   │
│  └────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Component Architecture

### Layer 1: Frontend (Presentation Layer)

```
index.html
│
├── HTML Structure
│   ├── Header (Logo, Status)
│   ├── Main Container
│   │   ├── Left Panel (Input)
│   │   │   ├── Language Selector
│   │   │   ├── Prompt Textarea
│   │   │   ├── Generate Button
│   │   │   └── Progress Bar
│   │   │
│   │   └── Right Panel (Output)
│   │       ├── Code Display
│   │       ├── Copy Button
│   │       └── Clear Button
│   │
│   └── Background (Animations)
│       └── 3D Blob Effects
│
├── CSS (Styling)
│   ├── Custom Properties (Colors)
│   ├── Grid Layout (Responsive)
│   ├── Animations (@keyframes)
│   ├── Gradient Effects
│   └── Glassmorphism
│
└── JavaScript (Interactivity)
    ├── State Management
    ├── Event Listeners
    ├── Fetch API Calls
    ├── DOM Manipulation
    └── Animation Control
```

**Technologies:**
- HTML5 (Semantic markup)
- CSS3 (Modern styling)
- Vanilla JavaScript (No frameworks)
- Fetch API (Network requests)

---

### Layer 2: Backend (API Layer)

```
main.py (FastAPI Application)
│
├── Middleware
│   ├── CORS Configuration
│   ├── Request Logging
│   └── Error Handling
│
├── Routes
│   ├── GET  /                 → Serve index.html
│   ├── GET  /health           → Health status
│   ├── POST /api/generate     → Code generation
│   ├── GET  /api/languages    → Language info
│   ├── GET  /api/guardrails   → Security rules
│   └── GET  /api/logs         → Log listing
│
├── Models (Pydantic)
│   ├── CodeGenerationRequest
│   ├── CodeGenerationResponse
│   └── HealthResponse
│
├── Validation Layer
│   ├── validate_prompt()
│   ├── validate_language()
│   └── Security Pattern Detection
│
├── Logging System
│   ├── File Handler (logs/)
│   ├── Console Handler
│   └── Timestamped Filenames
│
└── Error Handling
    ├── HTTP Exception Handlers
    ├── Graceful Errors
    └── Detailed Logging
```

**Key Technologies:**
- FastAPI (Async Python Web Framework)
- Uvicorn (ASGI Server)
- Pydantic (Data Validation)
- Python logging (Monitoring)

---

### Layer 3: Intelligence Layer (Agent)

```
agent.py (Code Generation Agent)
│
├── CodeGeneratorAgent
│   └── generate_code(prompt, language)
│       └── Orchestrates LLM operations
│
├── LocalLLM
│   ├── Model Loading
│   │   ├── Load GGUF file
│   │   ├── Configure parameters
│   │   └── Initialize llama-cpp
│   │
│   ├── Self-Consistency Engine
│   │   ├── Loop 9 iterations
│   │   ├── Vary temperature (0.1-0.9)
│   │   ├── LLM Inference
│   │   ├── Code Extraction
│   │   ├── Quality Scoring
│   │   └── Store Solutions
│   │
│   ├── Code Validation
│   │   ├── Extract from response
│   │   ├── Remove markdown
│   │   ├── Syntax validation
│   │   └── Length checking
│   │
│   ├── Scoring System
│   │   ├── Code length bonus
│   │   ├── Function definition bonus
│   │   ├── Logic keywords bonus
│   │   ├── Documentation bonus
│   │   ├── Type hints bonus
│   │   ├── Prompt matching bonus
│   │   └── Bad pattern penalties
│   │
│   └── Fallback System
│       ├── Template matching
│       ├── Language-specific boilerplate
│       └── Ready-to-run code
│
├── Language Configurations
│   ├── python { prompts, validators }
│   ├── javascript { prompts, validators }
│   ├── java { prompts, validators }
│   ├── cpp { prompts, validators }
│   ├── c { prompts, validators }
│   └── sql { prompts, validators }
│
└── System Prompts
    └── Customized for each language
        ├── Examples
        ├── Best practices
        ├── Syntax rules
        └── Code style guidelines
```

**Key Technologies:**
- llama-cpp-python (LLM inference)
- Python (Core logic)
- GGUF Model Format (Quantized model)

---

### Layer 4: Model Layer

```
Qwen2.5-Coder-7B (GGUF Format)
│
├── Model Specifications
│   ├── Architecture: Transformer
│   ├── Parameters: 7 Billion
│   ├── Quantization: Q5_K_M (5-bit)
│   ├── File Size: 4.7 GB
│   └── Context: 4096 tokens
│
├── Training Data
│   ├── Code samples (GitHub, etc.)
│   ├── General knowledge
│   ├── Programming languages (6+)
│   └── Documentation & comments
│
└── Capabilities
    ├── Code generation
    ├── Code completion
    ├── Multi-language support
    └── Error detection
```

---

## 🔄 Request-Response Flow Diagram

```
┌─────────────┐
│ User Opens  │
│  Browser    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│ Frontend Loads (index.html)         │
│ • 3D background animations start    │
│ • UI becomes interactive            │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ User Interaction                    │
│ 1. Select language (6 options)      │
│ 2. Type prompt (max 1000 chars)     │
│ 3. Click "Generate Code" button     │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────┐
│ Browser: Prepare Request                            │
│ • Validate input locally                            │
│ • Start progress bar animation                      │
│ • Disable generate button                           │
│ • Create JSON payload                               │
└──────┬────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────┐
│ HTTP POST /api/generate                             │
│ {                                                   │
│   "prompt": "...",                                  │
│   "language": "python"                              │
│ }                                                   │
└──────┬────────────────────────────────────────────┘
       │ (100-200ms)
       ▼
┌──────────────────────────────────────────────────────┐
│ FastAPI Route Handler (main.py)                      │
│ ├─ Log request: timestamp, IP, payload              │
│ ├─ Validate language (check supported list)         │
│ ├─ Validate prompt:                                 │
│ │  ├─ Check length (< 1000 chars)                  │
│ │  ├─ Run 16 security patterns                      │
│ │  └─ Reject if unsafe                              │
│ ├─ Start timer for generation time                  │
│ └─ Call CodeGeneratorAgent.generate_code()          │
└──────┬───────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│ Agent: Code Generation (agent.py)                    │
│ ├─ Load LLM (if first run)                          │
│ └─ Self-Consistency Loop (9 iterations):            │
│    │                                                 │
│    ├─ Iteration 1:                                  │
│    │  ├─ Temperature: 0.1 (conservative)            │
│    │  ├─ Build system + user prompt                 │
│    │  ├─ LLM Inference (500-1000ms)                │
│    │  │  └─ Generate text tokens iteratively       │
│    │  ├─ Extract code from response                │
│    │  ├─ Validate syntax (ast.parse for Python)   │
│    │  ├─ Score: 8.5                                │
│    │  └─ Store: {code, score}                      │
│    │                                                 │
│    ├─ Iteration 2:                                  │
│    │  ├─ Temperature: 0.2                           │
│    │  ├─ [Same process as above]                    │
│    │  ├─ Score: 7.2                                │
│    │  └─ Store: {code, score}                      │
│    │                                                 │
│    ├─ ... (Iterations 3-8)                          │
│    │                                                 │
│    └─ Iteration 9:                                  │
│       ├─ Temperature: 0.9 (creative)               │
│       ├─ [Same process as above]                    │
│       ├─ Score: 6.5                                │
│       └─ Store: {code, score}                      │
│                                                     │
│ ├─ Find best solution (max score = 9.1)            │
│ └─ Return best code                                │
└──────┬───────────────────────────────────────────────┘
       │ (1500-2500ms total)
       ▼
┌──────────────────────────────────────────────────────┐
│ Response Construction                               │
│ {                                                   │
│   "code": "def count_vowels(...)",                  │
│   "language": "python",                             │
│   "prompt": "count vowels...",                      │
│   "timestamp": "2024-01-15T10:30:45...",           │
│   "bot_name": "PyWizard",                           │
│   "status": "success",                              │
│   "generation_time": 2.34                           │
│ }                                                   │
│                                                     │
│ Log: "✅ Code generated in 2.34s, 234 chars"       │
└──────┬───────────────────────────────────────────────┘
       │ (HTTP 200)
       ▼
┌──────────────────────────────────────────────────────┐
│ Browser: Handle Response                            │
│ ├─ Receive JSON response                            │
│ ├─ Stop progress bar animation                      │
│ ├─ Display generated code                           │
│ ├─ Show code in right panel                         │
│ ├─ Enable copy button                               │
│ ├─ Enable clear button                              │
│ └─ Re-enable generate button                        │
└──────┬───────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│ User Views Code                                      │
│ Options:                                             │
│ 1. Copy to clipboard (one-click)                     │
│ 2. Clear and try new prompt                          │
│ 3. Switch language and retry                         │
└──────────────────────────────────────────────────────┘
```

---

## 🔐 Security Architecture

```
Security Layers:

Input Reception
    ↓
┌─────────────────────────────────┐
│ Layer 1: Length Validation      │ ← Max 1000 chars
├─────────────────────────────────┤
│ Layer 2: Pattern Detection      │ ← 16 Regex patterns
├─────────────────────────────────┤
│ Layer 3: Language Validation    │ ← Whitelist check
├─────────────────────────────────┤
│ Layer 4: Sanitization           │ ← Additional cleanup
├─────────────────────────────────┤
│ Layer 5: Logging                │ ← Security audit trail
└─────────────────────────────────┘
    ↓
Approved → Code Generation
Rejected → Error Response (403/400)
```

**Blocked Patterns (16 Rules):**
```
SQL Injection:
  • DROP TABLE
  • DELETE FROM
  • TRUNCATE TABLE

Code Execution:
  • eval()
  • exec()
  • system()
  • os.system()
  • __import__

Credentials:
  • password =
  • api_key
  • secret =

System Commands:
  • rm -rf
  • chmod 777
  • sudo
  • curl exec
  • wget exec
```

---

## 📊 Data Flow Diagrams

### Self-Consistency Sampling Flow

```
Input Prompt + Language
    ↓
┌────────────────────────────────────┐
│ Sample 1 (Temp 0.1)               │
├────────────────────────────────────┤
│ • LLM Inference                     │
│ • Token generation                  │
│ • Extract: "def count_vowels..."   │
│ • Validate: ✓                      │
│ • Score: 8.5                        │
│ • Store: {code: "...", score: 8.5} │
└────────────────────────────────────┘
    ↓
┌────────────────────────────────────┐
│ Sample 2 (Temp 0.2)               │
├────────────────────────────────────┤
│ • [Process similar to above]       │
│ • Score: 7.2                        │
└────────────────────────────────────┘
    ↓
    ... (Samples 3-8)
    ↓
┌────────────────────────────────────┐
│ Sample 9 (Temp 0.9)               │
├────────────────────────────────────┤
│ • [Process similar to above]       │
│ • Score: 6.5                        │
└────────────────────────────────────┘
    ↓
┌────────────────────────────────────┐
│ Selection                           │
├────────────────────────────────────┤
│ Solutions = [                       │
│   {score: 8.5, code: "..."},       │
│   {score: 7.2, code: "..."},       │
│   {score: 9.1, code: "..."} ← MAX  │
│   ...                              │
│ ]                                  │
│                                    │
│ best = max(solutions, key=score)   │
│ return best['code']                 │
└────────────────────────────────────┘
    ↓
Best Code Solution
```

### Code Scoring Process

```
Generated Code
    ↓
┌──────────────────────────────────────┐
│ Scoring Evaluation                   │
├──────────────────────────────────────┤
│                                      │
│ ✓ Length check (50-1000)    → +2.0  │
│ ✓ Function definition        → +3.0  │
│ ✓ Return statement           → +2.0  │
│ ✓ Documentation/Comments     → +1.0  │
│ ✓ Type hints                 → +1.0  │
│ ✓ Logic keywords (if,for)   → +2.0  │
│ ✓ Prompt keyword match       → +0.5x │
│                                      │
│ Penalties:                           │
│ ✗ TODO/FIXME patterns        → -5.0  │
│ ✗ Incomplete code            → -5.0  │
│                                      │
├──────────────────────────────────────┤
│ Total Score = Bonuses - Penalties   │
│ Range: 0.0 to 15.0+                 │
└──────────────────────────────────────┘
    ↓
Score: 9.1 (Excellent)
```

---

## 🔄 Token Flow in LLM Inference

```
Input Tokens
    ├─ System Prompt: ~400-500 tokens
    │  "You are an expert Python programmer..."
    │
    ├─ User Prompt: ~100-200 tokens
    │  "Write a function to count vowels..."
    │
    └─ Context: ~50-100 tokens
       Previous conversation, if any

    ↓ (Token Embedding)
    
Transformer Layers (7B Parameters)
    ├─ Layer 1: Self-attention
    ├─ Layer 2: Feed-forward
    ├─ ...
    └─ Layer 32: Output projection

    ↓ (Token Prediction)
    
Output Tokens (Generated)
    ├─ Token 1: "def"
    ├─ Token 2: "count_vowels"
    ├─ Token 3: "("
    ├─ Token 4: "text"
    ├─ ...
    ├─ Token N: ")"
    └─ Token N+1: <END>

    ↓ (Post-processing)
    
Generated Code String
    "def count_vowels(text: str) -> int:
        vowels = "aeiouAEIOU"
        return sum(1 for c in text if c in vowels)"
```

**Token Estimation:**
```
System Prompt:     ~450 tokens
User Prompt:       ~150 tokens
Generated Code:    ~200-600 tokens
────────────────────────────────
Per Sample:        ~800-1200 tokens
9 Samples:         ~7200-10800 tokens
```

---

## 📈 Performance Metrics

### Generation Timeline

```
Request → Response Timeline:

T=0ms     │ Request received
T=50ms    │ Validation (length, security patterns)
T=100ms   │ Language check, agent initialization
T=500ms   │ LLM model loaded (first run only)
T=1000ms  │ Sample 1 LLM inference
T=1200ms  │ Sample 1 code extraction & scoring
T=1400ms  │ Sample 2 LLM inference
T=1600ms  │ Sample 2 code extraction & scoring
...
T=2500ms  │ Sample 9 complete
T=2550ms  │ Select best solution
T=2600ms  │ Response serialization
T=2650ms  │ Response sent to client

Total: ~2.65 seconds (average)
```

### Resource Usage

```
At Startup:
├─ Python process: ~100MB
├─ FastAPI framework: ~50MB
└─ Minimal memory used

When Model Loads:
├─ LLM model: ~4.7GB (GGUF file)
├─ Inference buffers: ~300-500MB
└─ Total: ~5.0-5.2GB

During Generation:
├─ Active inference: ~200-300MB
├─ Temporary buffers: ~300-500MB
├─ Total peak: ~5.5GB

After Generation:
├─ Model stays in memory
├─ Next generation is faster
└─ Memory: ~5.0GB (sustained)
```

### CPU Usage

```
Idle:
├─ CPU usage: <1%
└─ Memory: ~100MB

During Inference:
├─ CPU usage: 60-90% (8 threads)
├─ Temperature per thread: Varies
└─ Memory: ~5.5GB

After Generation:
├─ CPU usage: <5%
└─ Model remains cached
```

---

## 🔧 Configuration Parameters

### Model Parameters

```python
MODEL_PARAMS = {
    "model_path": "./models/qwen2.5-coder-7b-instruct-q5_k_m.gguf",
    "n_ctx": 4096,              # Context window (tokens)
    "n_threads": 8,             # CPU threads
    "n_gpu_layers": 0,          # GPU layers (0=CPU only)
    "verbose": False            # Debug output
}
```

### Generation Parameters

```python
GENERATION_CONFIG = {
    "max_tokens": 1500,         # Max output length
    "temperature": 0.1-0.9,     # Varies per sample
    "top_p": 0.9,              # Nucleus sampling
    "repeat_penalty": 1.15,    # Avoid repetition
    "num_samples": 9            # Self-consistency samples
}
```

### Stopping Criteria

```python
stop=["Prompt:", "\n\n\n\n", "Output:"]

Stops generation when:
1. One of stop words is generated
2. Max tokens reached
3. Special token generated
```

---

## 📊 Logging Architecture

```
Application
    │
    ├─ [File Handler]
    │   └─ logs/codewizard_20240115_090000.log
    │       ├─ DEBUG level
    │       ├─ Detailed format
    │       └─ Persistent storage
    │
    ├─ [File Handler]
    │   └─ logs/agent.log
    │       ├─ Agent-specific events
    │       └─ Generation metrics
    │
    └─ [Console Handler]
        ├─ INFO level
        ├─ Real-time output
        └─ User feedback
```

**Log Format:**
```
2024-01-15 09:00:00 - [INFO] - __main__ - Message here

Components:
├─ Timestamp (YYYY-MM-DD HH:MM:SS)
├─ Log Level (DEBUG, INFO, WARNING, ERROR)
├─ Logger Name (module name)
└─ Message (event details)
```

---

## 🎯 Design Principles

### 1. **Separation of Concerns**
- Frontend (UI) ← HTTP → Backend (API) ← Python → Intelligence (Agent) ← Inference → Model

### 2. **Stateless Design**
- Each request is independent
- No session state required
- Scalable to multiple instances

### 3. **Security First**
- Multiple validation layers
- Pattern-based detection
- Whitelisting approach

### 4. **Performance Optimization**
- Model cached in memory
- Efficient token processing
- Minimal I/O overhead

### 5. **Observability**
- Comprehensive logging
- Request tracing
- Performance metrics

### 6. **Reliability**
- Fallback templates
- Error handling
- Graceful degradation

---

## 🚀 Scalability Considerations

### Horizontal Scaling

```
Load Balancer
    ├─ Server 1 (FastAPI + LLM)
    ├─ Server 2 (FastAPI + LLM)
    ├─ Server 3 (FastAPI + LLM)
    └─ Server N (FastAPI + LLM)

Shared:
    └─ Logs (Centralized logging)
```

### Caching Strategy

```
Level 1: Browser Cache
    └─ Static assets (index.html, CSS, JS)

Level 2: API Response Cache
    └─ Identical prompts return cached results

Level 3: Model Cache
    └─ LLM stays in memory (persistent)
```

### Database Integration (Future)

```
Would enable:
├─ Request history
├─ User preferences
├─ Usage analytics
├─ Code snippets library
└─ Execution logs
```

---

*Architecture Version 1.0 | Last Updated: January 2024*