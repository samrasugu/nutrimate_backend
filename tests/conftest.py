"""
Test configuration and fixtures for NutriMate tests.
"""
import pytest
import tempfile
import os
import sys
from pathlib import Path

# Add the parent directory to the Python path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set test environment variables before importing modules
os.environ['TESTING'] = 'true'
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
os.environ['SECRET_KEY'] = 'test-secret-key'

# Set dummy API keys for testing to prevent connection attempts
os.environ['PINECONE_API_KEY'] = 'test-pinecone-key'
os.environ['INDEX_NAME'] = 'test-index'
os.environ['OPENAI_API_KEY'] = 'test-openai-key'
os.environ['GOOGLE_API_KEY'] = 'test-google-key'
os.environ['REDIS_URL'] = 'redis://localhost:6379/15'  # Use different DB for tests
os.environ['AWS_REGION'] = 'us-east-1'
os.environ['AWS_ACCESS_KEY_ID'] = 'test-access-key'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'test-secret-key'
os.environ['LOCALE'] = 'en_US'
os.environ['SESSION_ID'] = 'test-session'
os.environ['BOT_ID'] = 'test-bot-id'
os.environ['BOT_ALIAS_ID'] = 'test-bot-alias-id'

# Load environment variables for testing
from dotenv import load_dotenv
load_dotenv('.env.test', override=False)  # Don't override what we set above

try:
    from app import app
    from database_config import db
    from models.user import User
    from models.user_profile import UserProfile
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running pytest from the project root directory")
    raise


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    # Create a temporary database file
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Disable authentication for testing
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()
    
    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return {
        'firstname': 'John',
        'lastname': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'password123'
    }


@pytest.fixture
def sample_user_profile():
    """Create a sample user profile for testing."""
    return {
        'age': 30,
        'gender': 'Male',
        'illnesses': ['diabetes'],
        'weight': 70.5,
        'height': 175.0,
        'location': 'New York',
        'food_preferences': ['vegetarian', 'low-carb']
    }


@pytest.fixture
def auth_headers():
    """Create authentication headers for testing."""
    return {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token'
    }


@pytest.fixture
def mock_chat_message():
    """Create a mock chat message for testing."""
    return {
        'message': 'What foods are good for diabetes?'
    }


@pytest.fixture
def mock_recommend_data():
    """Create mock recommendation data for testing."""
    return {
        'user_id': 1,
        'health_conditions': ['diabetes'],
        'dietary_preferences': ['vegetarian'],
        'message': 'I need meal recommendations for diabetes'
    }


@pytest.fixture
def created_user(client, sample_user):
    """Create a user in the database for testing."""
    with client.application.app_context():
        user = User(
            firstname=sample_user['firstname'],
            lastname=sample_user['lastname'],
            email=sample_user['email'],
            password=sample_user['password']  # In real app, this should be hashed
        )
        db.session.add(user)
        db.session.commit()
        return user
