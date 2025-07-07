#!/bin/bash

# Install missing dependencies for NutriMate
echo "🔧 Installing missing dependencies..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "📁 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install missing dependencies
echo "📦 Installing missing LangChain and Redis dependencies..."
pip install langchain-pinecone==0.1.1
pip install langchain-community==0.1.16  
pip install redis==5.0.1

# Install all dependencies from requirements.txt
echo "📦 Installing all dependencies from requirements.txt..."
pip install -r requirements.txt

echo "✅ Dependencies installation complete!"
echo ""
echo "Now you can run tests with:"
echo "  source venv/bin/activate"
echo "  pytest"
