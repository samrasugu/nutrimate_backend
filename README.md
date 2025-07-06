# NutriMate 🥗

An intelligent nutrition chat system that leverages Retrieval Augmented Generation (RAG) to deliver personalized dietary guidance. NutriMate combines a comprehensive nutrition knowledge base with advanced natural language processing to provide tailored recommendations based on users' health profiles, dietary preferences, and wellness goals.

## 🚀 Features

- **Intelligent Chat System**: AI-powered conversational interface for nutrition guidance
- **Personalized Recommendations**: Tailored dietary advice based on user profiles and health conditions
- **RAG Architecture**: Combines retrieval from knowledge base with generative AI for accurate responses
- **User Management**: Complete authentication and user profile management
- **Health Condition Tracking**: Support for various diseases and dietary restrictions
- **Location-Based Services**: Geo-specific nutrition recommendations
- **Conversational Memory**: Maintains chat history for contextual conversations

## 🛠️ Tech Stack

### Backend
- **Python** - Core programming language
- **Flask** - Web framework
- **LangChain** - LLM orchestration and RAG implementation
- **Pinecone** - Vector database for embeddings storage
- **OpenAI/Google AI** - Language models for natural language processing
- **Redis** - Chat message history and caching
- **PostgreSQL** - Primary database for user data
- **AWS Lex** - Additional conversational AI capabilities

### Frontend
- **Flutter** - Cross-platform mobile application

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- Redis instance
- Pinecone account
- OpenAI API key
- Google AI API key
- AWS account (for Lex integration)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/samrasugu/nutrimate_backend.git
   cd nutrimate_backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   # Database
   POSTGRESDB_URL=postgresql://username:password@localhost:5432/nutrimate
   SECRET_KEY=your-secret-key-here
   
   # AI Services
   OPENAI_API_KEY=your-openai-api-key
   GOOGLE_API_KEY=your-google-ai-api-key
   
   # Pinecone
   PINECONE_API_KEY=your-pinecone-api-key
   INDEX_NAME=your-pinecone-index-name
   
   # Redis
   REDIS_URL=redis://localhost:6379
   
   # AWS Lex
   AWS_REGION=your-aws-region
   AWS_ACCESS_KEY_ID=your-aws-access-key
   AWS_SECRET_ACCESS_KEY=your-aws-secret-key
   LOCALE=en_US
   SESSION_ID=your-session-id
   BOT_ID=your-bot-id
   BOT_ALIAS_ID=your-bot-alias-id
   ```

5. **Initialize the database**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

## 🚀 Usage

1. **Start the development server**
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`

2. **API Endpoints**

   ### Chat
   ```bash
   POST /chat
   Content-Type: application/json
   
   {
     "message": "What foods are good for diabetes?"
   }
   ```

   ### Recommendations
   ```bash
   POST /recommend
   Content-Type: application/json
   
   {
     "user_id": 123,
     "health_conditions": ["diabetes"],
     "dietary_preferences": ["vegetarian"]
   }
   ```

   ### Authentication
   ```bash
   POST /login
   Content-Type: application/json
   
   {
     "email": "user@example.com",
     "password": "password123"
   }
   ```

## 📁 Project Structure

```
nutrimate_backend/
├── app.py                 # Flask application entry point
├── chat.py               # AWS Lex chat integration
├── recommend.py          # RAG-based recommendation system
├── database_config.py    # Database configuration
├── requirements.txt      # Python dependencies
├── auth/
│   └── auth.py          # Authentication logic
├── diseases/
│   └── diseases.py      # Disease management
├── locations/
│   └── locations.py     # Location services
├── models/
│   ├── user.py          # User model
│   ├── user_profile.py  # User profile model
│   ├── disease.py       # Disease model
│   └── location.py      # Location model
└── utils/
    └── utils.py         # Utility functions
```

## 🔄 RAG Architecture

NutriMate implements a sophisticated RAG (Retrieval Augmented Generation) system:

1. **Knowledge Base**: Nutrition data is embedded and stored in Pinecone vector database
2. **Retrieval**: Relevant nutrition information is retrieved based on user queries
3. **Generation**: LLM generates personalized responses using retrieved context
4. **Memory**: Redis maintains conversation history for contextual responses

## 🏗️ Key Components

### Chat System (`chat.py`)
- Integrates with AWS Lex for natural language understanding
- Handles user input and bot responses

### Recommendation Engine (`recommend.py`)
- Implements RAG using LangChain
- Combines Pinecone vector search with Google AI/OpenAI
- Maintains conversation history with Redis

### User Management (`auth/`, `models/`)
- User authentication and authorization
- Profile management with health conditions
- Location-based personalization

## 🔐 Security Features

- Password hashing with bcrypt
- Session management with Flask
- Environment variable configuration
- SQL injection protection with SQLAlchemy

## 🧪 Testing

Run tests with:
```bash
python -m pytest tests/
```

## 📊 Performance Considerations

- **Caching**: Redis for conversation history and frequent queries
- **Vector Search**: Optimized Pinecone queries for fast retrieval
- **Database**: PostgreSQL with proper indexing
- **Async Processing**: Background task handling for heavy operations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, email support@nutrimate.com or open an issue on GitHub.

## 🙏 Acknowledgments

- OpenAI for GPT models
- Google AI for Gemini integration
- Pinecone for vector database services
- LangChain for RAG framework
- AWS for Lex conversational AI

---

**NutriMate** - Empowering healthier lives through intelligent nutrition guidance 🌱
