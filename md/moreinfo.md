# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API key (optional - has fallback)
export HUGGINGFACE_API_KEY="your_key"

# 3. Start backend
python main.py

# 4. Open index.html in browser
```

## 💡 **Usage Example**

**Input**: "Write a function that parses CSV and removes duplicates"

**Agent Process**:
1. 🤔 Thinks: "Need to handle file reading, duplicate detection, preserve order"
2. ⚡ Generates code with pandas/csv module
3. 🧪 Creates pytest tests
4. ✅ Runs tests → passes
5. ✨ Formats with Black
6. 📋 Returns production-ready code

**Copy button** → Ready to use!

## 🎨 **UI Highlights**

- **Gradient purple header** with memory counter
- **Real-time thinking bubbles** showing agent's process
- **Color-coded results**: Green for success, Yellow for warnings
- **Iteration counter** shows how many attempts it took
- **Error logs** expandable for debugging
- **Tools grid** showing what's available
- **Recent memory panel** for context awareness

## 📊 **Complete Workflow**
```
User Request
    ↓
Chain of Thought Planning (visible in UI)
    ↓
Code Generation (Qwen2.5-Coder-7B)
    ↓
Test Generation (automated)
    ↓
Run Tests
    ↓
Failed? → Analyze + Fix → Retry (max 5x)
    ↓
Success! → Format → Lint → Return
    ↓
Store in Memory (last 2)
    ↓
Display with Copy Option