#!/bin/bash

# Quick start script for NutriMate Backend
# Run this after completing the initial setup

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_warning "Virtual environment not found. Run ./setup.sh first."
    exit 1
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Please copy .env.example to .env and fill in your credentials."
    exit 1
fi

# Start services
print_status "Starting PostgreSQL..."
brew services start postgresql 2>/dev/null || echo "PostgreSQL may already be running"

print_status "Starting Redis..."
brew services start redis 2>/dev/null || echo "Redis may already be running"

# Wait a moment for services to start
sleep 2

# Test database connection
print_status "Testing database connection..."
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import create_engine
engine = create_engine(os.getenv('POSTGRESDB_URL'))
conn = engine.connect()
conn.close()
print('Database connection successful!')
" 2>/dev/null || print_warning "Database connection failed. Check your .env file."

# Test Redis connection
print_status "Testing Redis connection..."
redis-cli ping > /dev/null && print_status "Redis connection successful!" || print_warning "Redis connection failed."

print_status "Starting Flask development server..."
echo ""
echo "🚀 NutriMate Backend is starting..."
echo "📍 Server will be available at: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Start the Flask app
python3 app.py
