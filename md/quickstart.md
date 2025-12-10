# 🚀 Code Wizard - Quick Start Guide

Get up and running in 5 minutes!

---

## ⚡ Quick Setup (Choose Your OS)

### **Windows**

```batch
# 1. Run setup script
setup.bat

# 2. Download model (after setup completes)
pip install huggingface-hub
huggingface-cli download Qwen/Qwen2.5-Coder-7B-Instruct-GGUF ^
  qwen2.5-coder-7b-instruct-q5_k_m.gguf --local-dir ./models

# 3. Start server
python main.py

# 4. Open browser
# http://localhost:8000
```

### **macOS / Linux**

```bash
# 1. Run setup script
chmod +x setup.sh
./setup.sh

# 2. Download model (after setup completes)
pip install huggingface-hub
huggingface-cli download Qwen/Qwen2.5-Coder-7B-Instruct-GGUF \
  qwen2.5-coder-7b-instruct-q5_k_m.gguf --local-dir ./models

# 3. Start server
python main.py

# 4. Open browser
# http://localhost:8000
```

---

## 📋 Checklist

Before running:

- [ ] Python 3.8+ installed
- [ ] 8GB+ RAM available
- [ ] 5GB free disk space
- [ ] Virtual environment created
- [ ] Dependencies installed (requirements.txt)
- [ ] Model downloaded to models/
- [ ] Port 8000 is free

---

## 🎯 First Run

1. **Open Application**
   ```
   http://localhost:8000
   ```

2. **Select Language**
   - Click one of 6 language buttons
   - Example: Python (🐍)

3. **Describe Code**
   - Type: "Write a function to count vowels in a string"
   - Max 1000 characters

4. **Generate**
   - Click "Generate Code" button
   - Watch progress bar animate
   - Code appears in 2-4 seconds

5. **Copy & Use**
   - Click "Copy Code" button
   - Paste anywhere you need it
   - Code is production-ready!

---

## 📊 What Gets Created

After first run:

```
logs/
├── codewizard_20240115_090000.log  ← Detailed execution log
├── agent.log                        ← Agent-specific logs
└── app.log                          ← Application logs

models/
└── qwen2.5-coder-7b-instruct-q5_k_m.gguf  ← AI Model (4.7GB)
```

---

## 🔍 Check Everything Works

### Health Check
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "Code Wizard API",
  "timestamp": "2024-01-15T10:30:45.123456",
  "uptime": "0h 5m"
}
```

### Supported Languages
```bash
curl http://localhost:8000/api/languages
```

### Security Rules
```bash
curl http://localhost:8000/api/guardrails
```

---

## 💻 Test Code Generation

### Via Browser
1. Go to `http://localhost:8000`
2. Type prompt
3. Click "Generate Code"
4. See generated code
5. Click "Copy Code"

### Via API (curl)
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a function to check if a number is prime",
    "language": "python"
  }'
```

### Via Python
```python
import requests

response = requests.post(
    "http://localhost:8000/api/generate",
    json={
        "prompt": "Count vowels in a string",
        "language": "python"
    }
)

print(response.json()["code"])
```

### Via JavaScript
```javascript
fetch('http://localhost:8000/api/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: "Write a function to reverse a string",
    language: "javascript"
  })
})
.then(r => r.json())
.then(data => console.log(data.code))
```

---

## 🤖 Supported Languages

| Language | Button | Bot Name | Icon |
|----------|--------|----------|------|
| Python | Click | PyWizard | 🐍 |
| JavaScript | Click | ScriptMaster | ✨ |
| Java | Click | ByteForge | ☕ |
| C++ | Click | CppNinja | ⚡ |
| C | Click | CChain | 🔧 |
| SQL | Click | DataAlchemy | 🗄️ |

---

## 📝 Example Prompts

Try these prompts to see it in action:

### Python
```
- Write a function to check if a number is prime
- Create a function to reverse a string
- Build a fibonacci sequence generator
- Count occurrences of each character in a string
- Check if a string is a palindrome
```

### JavaScript
```
- Write a function to sort an array
- Create a debounce utility function
- Build a simple calculator
- Make a function to flatten nested arrays
- Create a promise-based sleep function
```

### Java
```
- Write a class for a simple calculator
- Create a function to find max element in array
- Build a bubble sort implementation
- Make a string palindrome checker
- Create a linked list implementation
```

### SQL
```
- Write a query to get top 10 customers by sales
- Create a query to find duplicate entries
- Write a join query for orders and customers
- Get products with sales above average
- Create a query to find customer with most orders
```

### C++
```
- Write a function to find GCD of two numbers
- Create a class for a simple queue
- Build a binary search implementation
- Make a factorial calculator
- Create a function to check if array is sorted
```

### C
```
- Write a function to reverse an array
- Create a function to find missing number
- Build a simple string manipulation function
- Make a factorial calculator
- Create a function to swap two numbers
```

---

## ⚙️ Configuration

### Change Port

Edit `main.py`:
```python
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8001,  # Change this
    log_level="info"
)
```

Then run:
```bash
python main.py
```

Access at: `http://localhost:8001`

### Change Model Path

Edit `agent.py`:
```python
MODEL_PATH = "./models/your-model-name.gguf"
```

### Adjust Generation Samples

Edit `agent.py`:
```python
NUM_SAMPLES = 9  # Change to 5, 7, 11, etc.
```

Fewer samples = Faster but potentially lower quality
More samples = Better quality but slower

---

## 🐛 Troubleshooting

### "Port 8000 already in use"
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### "Model not found"
Ensure model is in `./models/` directory:
```bash
ls -lh models/qwen2.5-coder-7b-instruct-q5_k_m.gguf
# Should show ~4.7GB
```

### "Out of memory"
Close other applications or use GPU:
```python
# In agent.py, change:
"n_gpu_layers": 35  # Use GPU layers
```

### "Generation timeout"
Model might be slow. Check:
```bash
# View logs for performance
tail -f logs/codewizard_*.log
```

### "Import error"
Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Next Steps

1. **Explore API**
   - Visit: `http://localhost:8000/docs`
   - See all endpoints
   - Try them in Swagger UI

2. **Check Logs**
   - Location: `logs/codewizard_*.log`
   - Contains all request/response details
   - Useful for debugging

3. **Read Full Documentation**
   - See `README.md` for comprehensive guide
   - Detailed architecture and workflows
   - Advanced configuration options

4. **Integrate with Your Project**
   - Use API endpoints
   - Parse JSON responses
   - Handle errors gracefully

5. **Customize**
   - Modify prompts for specific domains
   - Add more security patterns
   - Integrate with other tools

---

## 🎓 API Usage Examples

### Example 1: Python Function
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a function to find the longest word in a list",
    "language": "python"
  }'
```

### Example 2: SQL Query
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Get all customers who made purchases in last 30 days",
    "language": "sql"
  }'
```

### Example 3: JavaScript Function
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a function to deep clone an object",
    "language": "javascript"
  }'
```

---

## 📞 Getting Help

1. **Check Status**
   ```bash
   curl http://localhost:8000/health
   ```

2. **View Logs**
   ```bash
   tail -f logs/codewizard_*.log
   ```

3. **Read Documentation**
   - `README.md` - Complete documentation
   - `PROJECT_STRUCTURE.md` - File organization
   - API docs at `/docs`

4. **Check Security**
   ```bash
   curl http://localhost:8000/api/guardrails
   ```

---

## 🎉 You're Ready!

That's it! You now have a fully functional AI code generator.

**Key Features:**
- ✅ Generate code in 6 languages
- ✅ Self-consistency for quality
- ✅ Progress bar during generation
- ✅ Beautiful animated UI
- ✅ Timestamped detailed logs
- ✅ Security guardrails
- ✅ REST API

---

**Happy Coding! 🚀**

Need help? Check the full README.md for comprehensive documentation.

---

*Version 1.0.0 | Last Updated: January 2024*