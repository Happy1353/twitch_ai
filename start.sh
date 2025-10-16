#!/bin/bash

# Quick start script for Twitch AI Girl

echo "🎀 Twitch AI Girl - Quick Start"
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠ Virtual environment not found. Creating..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import twitchio" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check configuration
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found"
    echo "Please copy .env.example to .env and configure it"
    echo "Run: cp .env.example .env"
    exit 1
fi

# Run setup test
echo "🔍 Testing configuration..."
python utils/test_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🚀 Starting Twitch AI Girl..."
    echo "Press Ctrl+C to stop"
    echo ""
    python main.py
else
    echo ""
    echo "❌ Configuration test failed"
    echo "Please fix the errors above before starting"
    exit 1
fi

