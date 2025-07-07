# NutriMate Setup Guide 🚀

This guide will walk you through setting up the NutriMate backend project from scratch.

## Prerequisites

Before you begin, ensure you have the following installed on your macOS system:

- **Python 3.8+** (Check with `python3 --version`)
- **PostgreSQL** (Install via Homebrew: `brew install postgresql`)
- **Redis** (Install via Homebrew: `brew install redis`)
- **Git** (Usually pre-installed on macOS)

## 🔧 Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/samrasugu/nutrimate_backend.git
cd nutrimate_backend
```

### 2. Create and Activate Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
# To deactivate later, simply run: deactivate
```

### 3. Upgrade pip and Install Dependencies

```bash
# Upgrade pip to latest version
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your actual credentials
nano .env  # or use your preferred editor
```

Fill in your actual values in the `.env` file:

```env
# Database
POSTGRESDB_URL=postgresql://username:password@localhost:5432/nutrimate
SECRET_KEY=your-super-secret-key-here

# AI Services
OPENAI_API_KEY=sk-your-openai-api-key
GOOGLE_API_KEY=your-google-ai-api-key

# Pinecone
PINECONE_API_KEY=your-pinecone-api-key
INDEX_NAME=nutrimate-index

# Redis
REDIS_URL=redis://localhost:6379

# AWS Lex
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
LOCALE=en_US
SESSION_ID=nutrimate-session
BOT_ID=your-bot-id
BOT_ALIAS_ID=your-bot-alias-id
```

### 5. Set Up Database

```bash
# Start PostgreSQL service
brew services start postgresql

# Create database
createdb nutrimate

# Initialize database tables
python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database tables created successfully!')
"
```

### 6. Set Up Redis

```bash
# Start Redis service
brew services start redis

# Test Redis connection
redis-cli ping
# Should return: PONG
```

### 7. Set Up Pinecone Index

```bash
# Create Pinecone index (run this Python script)
python3 -c "
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
pc.create_index(
    name=os.getenv('INDEX_NAME'),
    dimension=384,  # for all-MiniLM-L6-v2 embeddings
    metric='cosine'
)
print('Pinecone index created successfully!')
"
```

## 🚀 Running the Application

### Development Mode

```bash
# Make sure your virtual environment is activated
source venv/bin/activate

# Start the Flask development server
python3 app.py

# The server will start on http://localhost:5000
```

### Production Mode

```bash
# Using Gunicorn (install if not already)
pip install gunicorn

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 app:app
```

## 📊 Useful Commands

### Virtual Environment Management

```bash
# Activate virtual environment
source venv/bin/activate

# Deactivate virtual environment
deactivate

# Install new package
pip install package-name

# Update requirements.txt after installing new packages
pip freeze > requirements.txt
```

### Database Management

```bash
# Reset database
python3 -c "
from app import app, db
with app.app_context():
    db.drop_all()
    db.create_all()
    print('Database reset complete!')
"

# Access PostgreSQL CLI
psql nutrimate
```

### Service Management

```bash
# Start all services
brew services start postgresql
brew services start redis

# Stop all services
brew services stop postgresql
brew services stop redis

# Check service status
brew services list | grep -E "(postgresql|redis)"
```

## 🔍 API Endpoints

### Using curl

```bash
# Access basic endpoint
curl http://localhost:5000/

# Chat endpoint
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What foods are good for diabetes?"}'

# Recommendations endpoint
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "health_conditions": ["diabetes"]}'
```

### Using Python requests

```python
import requests

# Chat example
response = requests.post('http://localhost:5000/chat', 
                        json={'message': 'Hello'})
print(response.json())
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Kill process on port 5000
   lsof -ti:5000 | xargs kill -9
   ```

2. **Database connection error**
   ```bash
   # Check PostgreSQL is running
   brew services list | grep postgresql
   
   # Restart PostgreSQL
   brew services restart postgresql
   ```

3. **Redis connection error**
   ```bash
   # Check Redis is running
   redis-cli ping
   
   # Restart Redis
   brew services restart redis
   ```

4. **Virtual environment issues**
   ```bash
   # Remove and recreate venv
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Permission errors**
   ```bash
   # Fix Python package permissions
   sudo chown -R $(whoami) venv/
   ```

## 📁 Project Structure Understanding

```
nutrimate_backend/
├── app.py                 # Main Flask application
├── chat.py               # AWS Lex integration
├── recommend.py          # RAG recommendation engine
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create from .env.example)
├── venv/                # Virtual environment (created by you)
├── auth/                # Authentication module
├── diseases/            # Disease management
├── locations/           # Location services
├── models/              # Database models
└── utils/               # Utility functions
```

## 🎯 Next Steps

After successful setup:

1. **Populate your Pinecone index** with nutrition data
2. **Configure AWS Lex bot** with your intents and utterances
3. **Set up your Flutter frontend** to connect to this backend
4. **Add your nutrition knowledge base** to the vector database
5. **Customize the recommendation prompts** in `recommend.py`

## 📞 Need Help?

If you encounter any issues:

1. Check the logs in your terminal
2. Verify all services are running
3. Ensure environment variables are set correctly
4. Check the [main README](README.md) for additional information

Happy coding! 🚀
