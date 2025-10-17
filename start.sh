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

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Configuration test failed"
    echo "Please fix the errors above before starting"
    exit 1
fi

# Launch mode selection
echo ""
echo "🎮 Выберите режим запуска:"
echo "1) 🚀 Стандартный режим (бот + аватар)"
echo "2) 🤖 Только бот (без аватара)"
echo ""

read -p "Введите номер режима (1-2): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Запуск в стандартном режиме..."
        echo "Press Ctrl+C to stop"
        echo ""
        python main.py --mode full
        ;;
    2)
        echo ""
        echo "🤖 Запуск без бота"
        echo "Press Ctrl+C to stop"
        echo ""
        python main.py --mode no_bot
        ;;
esac