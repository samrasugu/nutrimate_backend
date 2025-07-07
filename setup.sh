#!/bin/bash

# NutriMate Backend Setup Script for macOS
# This script automates the setup process

set -e  # Exit on any error

echo "🚀 Setting up NutriMate Backend..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

print_status "Python 3 found: $(python3 --version)"

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    print_warning "PostgreSQL not found. Installing via Homebrew..."
    if command -v brew &> /dev/null; then
        brew install postgresql
        brew services start postgresql
    else
        print_error "Homebrew not found. Please install PostgreSQL manually."
        exit 1
    fi
fi

# Check if Redis is installed
if ! command -v redis-cli &> /dev/null; then
    print_warning "Redis not found. Installing via Homebrew..."
    if command -v brew &> /dev/null; then
        brew install redis
        brew services start redis
    else
        print_error "Homebrew not found. Please install Redis manually."
        exit 1
    fi
fi

# Create virtual environment
print_status "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing dependencies..."
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    print_status "Creating .env file from template..."
    cp .env.example .env
    print_warning "Please edit .env file with your actual credentials before running the app!"
else
    print_status ".env file already exists."
fi

# Copy test environment file
if [ ! -f .env.test ]; then
    print_status "Creating .env.test file from template..."
    cp .env.test.example .env.test
    print_status "Test environment file created."
fi

# Create databases
print_status "Creating databases..."
createdb nutrimate 2>/dev/null || print_warning "Database 'nutrimate' may already exist"
createdb nutrimate_test 2>/dev/null || print_warning "Database 'nutrimate_test' may already exist"

# Initialize database
print_status "Initializing database tables..."
python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database tables created successfully!')
" 2>/dev/null || print_warning "Database initialization may have failed. Check your .env file."

print_status "Setup complete! 🎉"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your actual credentials"
echo "2. Run 'source venv/bin/activate' to activate virtual environment"
echo "3. Run 'python3 app.py' to start the development server"
echo ""
echo "For detailed setup instructions, see SETUP.md"
