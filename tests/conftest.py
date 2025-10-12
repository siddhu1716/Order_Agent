"""
Pytest configuration and shared fixtures for the QuickPick test suite.
"""
import pytest
import asyncio
from typing import Dict, Any, List
from unittest.mock import Mock, AsyncMock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent
from agents.food_agent import FoodAgent
from agents.travel_agent import TravelAgent
from agents.shopping_agent import ShoppingAgent, QuickCommerceAgent
from agents.payment_agent import PaymentAgent
from master.master_agent import MasterAgent
from mcp.food_api_client import FoodAPIClient
from mcp.speech_to_text_client import GroqWhisperClient
from mcp.razorpay_api_client import RazorpayAPIClient
from mcp.quick_commerce_scrapper import QuickCommerceScraper, QuickCommerceOptimizer


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_food_api_client():
    """Mock FoodAPIClient for testing."""
    mock_client = Mock(spec=FoodAPIClient)
    mock_client.search_recipes = AsyncMock(return_value=[
        {
            "id": 123,
            "title": "Test Recipe",
            "readyInMinutes": 30,
            "servings": 4,
            "sourceUrl": "https://example.com/recipe",
            "image": "https://example.com/image.jpg",
            "summary": "A delicious test recipe"
        }
    ])
    mock_client.get_recipe_by_id = AsyncMock(return_value={
        "id": 123,
        "title": "Test Recipe",
        "instructions": "Test instructions",
        "ingredients": ["ingredient1", "ingredient2"]
    })
    mock_client.get_meal_plan = AsyncMock(return_value={
        "meals": [
            {"id": 1, "title": "Breakfast", "readyInMinutes": 15},
            {"id": 2, "title": "Lunch", "readyInMinutes": 30},
            {"id": 3, "title": "Dinner", "readyInMinutes": 45}
        ],
        "nutrients": {
            "calories": 2000,
            "protein": 150,
            "fat": 80,
            "carbohydrates": 250
        }
    })
    return mock_client


@pytest.fixture
def mock_whisper_client():
    """Mock GroqWhisperClient for testing."""
    mock_client = Mock(spec=GroqWhisperClient)
    mock_client.transcribe_audio = AsyncMock(return_value={
        "text": "Order tomatoes and milk",
        "language": "en",
        "duration": 5.2
    })
    mock_client.transcribe_audio_bytes = AsyncMock(return_value={
        "text": "Test transcription",
        "language": "en",
        "duration": 3.1
    })
    mock_client.get_supported_languages = Mock(return_value={
        "languages": ["en", "es", "fr", "de", "hi"]
    })
    return mock_client


@pytest.fixture
def mock_razorpay_client():
    """Mock RazorpayAPIClient for testing."""
    mock_client = Mock(spec=RazorpayAPIClient)
    mock_client.create_order = AsyncMock(return_value={
        "id": "order_test123",
        "amount": 50000,
        "currency": "INR",
        "status": "created",
        "receipt": "test_receipt_001"
    })
    mock_client.verify_payment_signature = AsyncMock(return_value={
        "success": True,
        "message": "Payment verified successfully"
    })
    mock_client.create_payment_link = AsyncMock(return_value={
        "id": "plink_test123",
        "short_url": "https://rzp.io/test123",
        "status": "created"
    })
    mock_client.refund_payment = AsyncMock(return_value={
        "id": "rfnd_test123",
        "amount": 50000,
        "status": "processed"
    })
    return mock_client


@pytest.fixture
def mock_quick_commerce_scraper():
    """Mock QuickCommerceScraper for testing."""
    mock_scraper = Mock(spec=QuickCommerceScraper)
    mock_scraper.search_products = AsyncMock(return_value=[
        {
            "name": "Tomatoes",
            "price": 25.0,
            "rating": 4.5,
            "availability": True,
            "image_url": "https://example.com/tomatoes.jpg",
            "product_url": "https://example.com/product/123"
        }
    ])
    mock_scraper.place_order = AsyncMock(return_value={
        "order_id": "order_zepto_123",
        "status": "placed",
        "total_amount": 245.0,
        "estimated_delivery": "2024-01-15T10:30:00Z",
        "tracking_url": "https://zepto.com/track/123"
    })
    return mock_scraper


@pytest.fixture
def mock_quick_commerce_optimizer():
    """Mock QuickCommerceOptimizer for testing."""
    mock_optimizer = Mock(spec=QuickCommerceOptimizer)
    mock_optimizer.find_best_deals = AsyncMock(return_value={
        "best_platform": "zepto",
        "total_cost": 245.0,
        "savings": 35.0,
        "delivery_time": 10,
        "platform_breakdown": {
            "zepto": {"subtotal": 245.0, "delivery_fee": 0, "delivery_time": 10},
            "blinkit": {"subtotal": 280.0, "delivery_fee": 15, "delivery_time": 15}
        }
    })
    return mock_optimizer


@pytest.fixture
def food_agent(mock_food_api_client):
    """Create FoodAgent instance for testing."""
    agent = FoodAgent()
    agent.food_api_client = mock_food_api_client
    return agent


@pytest.fixture
def travel_agent():
    """Create TravelAgent instance for testing."""
    return TravelAgent()


@pytest.fixture
def shopping_agent():
    """Create ShoppingAgent instance for testing."""
    return ShoppingAgent()


@pytest.fixture
def quick_commerce_agent(mock_quick_commerce_scraper, mock_quick_commerce_optimizer):
    """Create QuickCommerceAgent instance for testing."""
    agent = QuickCommerceAgent()
    agent.scraper = mock_quick_commerce_scraper
    agent.optimizer = mock_quick_commerce_optimizer
    return agent


@pytest.fixture
def payment_agent(mock_razorpay_client):
    """Create PaymentAgent instance for testing."""
    agent = PaymentAgent()
    agent.razorpay_client = mock_razorpay_client
    return agent


@pytest.fixture
def sample_food_request():
    """Sample food request data for testing."""
    return {
        "message": "Plan a healthy dinner for tonight",
        "user_id": "test_user_123",
        "context": {
            "dietary_restrictions": ["vegetarian"],
            "calorie_goal": 500
        }
    }


@pytest.fixture
def sample_travel_request():
    """Sample travel request data for testing."""
    return {
        "message": "Find flights from New York to Los Angeles for next week",
        "user_id": "test_user_123",
        "context": {
            "departure_date": "2024-01-20",
            "return_date": "2024-01-27",
            "passengers": 2
        }
    }


@pytest.fixture
def sample_shopping_request():
    """Sample shopping request data for testing."""
    return {
        "message": "Compare prices for wireless headphones under $100",
        "user_id": "test_user_123",
        "context": {
            "budget": 100,
            "category": "electronics"
        }
    }


@pytest.fixture
def sample_quick_commerce_request():
    """Sample quick commerce request data for testing."""
    return {
        "message": "Order tomatoes and milk",
        "user_id": "test_user_123",
        "context": {
            "items": ["tomatoes", "milk"],
            "delivery_preference": "fastest"
        }
    }


@pytest.fixture
def sample_payment_request():
    """Sample payment request data for testing."""
    return {
        "message": "Create a payment order for 500 rupees",
        "user_id": "test_user_123",
        "context": {
            "amount": 500.0,
            "currency": "INR"
        }
    }


@pytest.fixture
def sample_audio_file():
    """Sample audio file path for testing."""
    return "tests/fixtures/sample_audio.wav"


@pytest.fixture
def mock_platform_data():
    """Mock platform data for quick commerce testing."""
    return {
        "zepto": {
            "name": "Zepto",
            "logo": "⚡",
            "base_url": "https://www.zepto.com",
            "search_url": "https://www.zepto.com/search",
            "selectors": {
                "product_name": ".product-name",
                "product_price": ".price",
                "product_rating": ".rating",
                "product_availability": ".availability"
            }
        },
        "blinkit": {
            "name": "Blinkit",
            "logo": "🛒",
            "base_url": "https://blinkit.com",
            "search_url": "https://blinkit.com/search",
            "selectors": {
                "product_name": ".product-title",
                "product_price": ".price-value",
                "product_rating": ".rating-stars",
                "product_availability": ".stock-status"
            }
        }
    }


@pytest.fixture
def mock_product_data():
    """Mock product data for testing."""
    return [
        {
            "name": "Fresh Tomatoes",
            "price": 25.0,
            "rating": 4.5,
            "availability": True,
            "platform": "zepto",
            "image_url": "https://example.com/tomatoes.jpg",
            "product_url": "https://zepto.com/product/123"
        },
        {
            "name": "Organic Milk 1L",
            "price": 60.0,
            "rating": 4.3,
            "availability": True,
            "platform": "blinkit",
            "image_url": "https://example.com/milk.jpg",
            "product_url": "https://blinkit.com/product/456"
        }
    ]


@pytest.fixture
def mock_order_data():
    """Mock order data for testing."""
    return {
        "order_id": "order_zepto_123",
        "platform": "zepto",
        "items": [
            {"name": "Tomatoes", "quantity": 2, "price": 25.0},
            {"name": "Milk", "quantity": 1, "price": 60.0}
        ],
        "total_amount": 110.0,
        "status": "placed",
        "estimated_delivery": "2024-01-15T10:30:00Z",
        "tracking_url": "https://zepto.com/track/123",
        "user_id": "test_user_123"
    }


# Test data fixtures
@pytest.fixture
def test_recipes():
    """Test recipe data."""
    return [
        {
            "id": 1,
            "title": "Vegetarian Pasta",
            "readyInMinutes": 30,
            "servings": 4,
            "sourceUrl": "https://example.com/recipe1",
            "image": "https://example.com/image1.jpg",
            "summary": "A delicious vegetarian pasta dish"
        },
        {
            "id": 2,
            "title": "Chicken Curry",
            "readyInMinutes": 45,
            "servings": 6,
            "sourceUrl": "https://example.com/recipe2",
            "image": "https://example.com/image2.jpg",
            "summary": "Spicy chicken curry with rice"
        }
    ]


@pytest.fixture
def test_flights():
    """Test flight data."""
    return [
        {
            "id": "flight_1",
            "airline": "Delta",
            "departure": "2024-01-20T08:00:00Z",
            "arrival": "2024-01-20T11:30:00Z",
            "price": 350.0,
            "duration": "3h 30m"
        },
        {
            "id": "flight_2",
            "airline": "American",
            "departure": "2024-01-20T14:00:00Z",
            "arrival": "2024-01-20T17:30:00Z",
            "price": 380.0,
            "duration": "3h 30m"
        }
    ]


@pytest.fixture
def test_hotels():
    """Test hotel data."""
    return [
        {
            "id": "hotel_1",
            "name": "Marriott Downtown",
            "price": 200.0,
            "rating": 4.5,
            "amenities": ["WiFi", "Pool", "Gym"],
            "location": "Downtown"
        },
        {
            "id": "hotel_2",
            "name": "Hilton Garden Inn",
            "price": 150.0,
            "rating": 4.2,
            "amenities": ["WiFi", "Restaurant"],
            "location": "Airport"
        }
    ]


# Async test helpers
@pytest.fixture
def async_test():
    """Helper for async tests."""
    def _async_test(coro):
        return asyncio.get_event_loop().run_until_complete(coro)
    return _async_test


# Environment setup for tests
@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    """Set up test environment variables."""
    monkeypatch.setenv("SPOONACULAR_API_KEY", "test_key")
    monkeypatch.setenv("GROQ_API_KEY", "test_key")
    monkeypatch.setenv("RAZORPAY_API_KEY", "test_key")
    monkeypatch.setenv("RAZORPAY_API_SECRET", "test_secret")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
