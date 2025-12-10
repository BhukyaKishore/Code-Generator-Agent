#!/bin/bash

# Code Wizard - Setup Script
# Automates installation and setup process

set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║         CODE WIZARD - AUTOMATED SETUP SCRIPT           ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "🐍 Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "   Python version: $python_version"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "   Virtual environment already exists (skipping)"
else
    python -m venv venv
    echo "   ✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate
echo "   ✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null
echo "   ✅ pip upgraded"
echo ""

# Install dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt
echo "   ✅ Dependencies installed"
echo ""

# Create required directories
echo "📁 Creating required directories..."
mkdir -p logs
mkdir -p models
echo "   ✅ Created: logs/"
echo "   ✅ Created: models/"
echo ""

# Check for model file
echo "🤖 Checking for Qwen2.5-Coder model..."
MODEL_FILE="models/qwen2.5-coder-7b-instruct-q5_k_m.gguf"

if [ -f "$MODEL_FILE" ]; then
    file_size=$(du -h "$MODEL_FILE" | awk '{print $1}')
    echo "   ✅ Model found: $file_size"
else
    echo "   ⚠️  Model not found!"
    echo ""
    echo "   To download the model, run:"
    echo ""
    echo "   Option 1: Using huggingface-cli"
    echo "   $ pip install huggingface-hub"
    echo "   $ huggingface-cli download Qwen/Qwen2.5-Coder-7B-Instruct-GGUF \\"
    echo "     qwen2.5-coder-7b-instruct-q5_k_m.gguf --local-dir ./models"
    echo ""
    echo "   Option 2: Manual download"
    echo "   1. Visit: https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF"
    echo "   2. Download: qwen2.5-coder-7b-instruct-q5_k_m.gguf"
    echo "   3. Place in: ./models/"
    echo ""
fi
echo ""

# Verify installation
echo "✅ Verifying installation..."
python -c "from fastapi import FastAPI; from agent import CodeGeneratorAgent; print('   ✅ All imports successful')" 2>/dev/null || echo "   ⚠️  Warning: Could not verify all imports"
echo ""

# Display next steps
echo "╔════════════════════════════════════════════════════════╗"
echo "║              SETUP COMPLETE - NEXT STEPS               ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "1️⃣  Download AI Model (if not already done):"
echo "   huggingface-cli download Qwen/Qwen2.5-Coder-7B-Instruct-GGUF \\"
echo "   qwen2.5-coder-7b-instruct-q5_k_m.gguf --local-dir ./models"
echo ""
echo "2️⃣  Start the application:"
echo "   python main.py"
echo ""
echo "3️⃣  Open in browser:"
echo "   http://localhost:8000"
echo ""
echo "4️⃣  API Documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "📝 Logs will be saved to: logs/codewizard_YYYYMMDD_HHMMSS.log"
echo ""
echo "Happy coding! 🚀"