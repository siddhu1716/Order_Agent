"""
Unit tests for FoodAgent class.
"""
import pytest
from agents.food_agent import FoodAgent

@pytest.fixture
def food_agent():
    """Provides a FoodAgent instance for testing."""
    return FoodAgent()

class TestFoodAgent:
    """Test cases for FoodAgent class."""

    def test_food_agent_initialization(self, food_agent):
        """Test FoodAgent initialization."""
        assert food_agent.agent_id == "FoodAgent"
        assert food_agent.dietary_restrictions == []
        assert food_agent.allergies == []

    @pytest.mark.asyncio
    async def test_process_request_meal_planning(self, food_agent):
        """Test meal planning request processing."""
        request_data = {
            "type": "meal_planning",
            "calories": 500,
            "meal_type": "dinner"
        }
        
        result = await food_agent.process_request(request_data, {})
        
        assert result["status"] == "success"
        assert "meal_type" in result["data"]
        assert result["data"]["calories"] == 500

    @pytest.mark.asyncio
    async def test_process_request_recipe_generation(self, food_agent):
        """Test recipe generation request processing."""
        request_data = {
            "type": "recipe_generation",
            "ingredients": ["tomatoes", "pasta", "cheese"],
            "cuisine": "Italian"
        }
        
        result = await food_agent.process_request(request_data, {})
        
        assert result["status"] == "success"
        assert "name" in result["data"]
        assert "Italian" in result["data"]["name"]

    @pytest.mark.asyncio
    async def test_process_request_grocery_list(self, food_agent):
        """Test grocery list generation."""
        request_data = {
            "type": "grocery_list",
            "recipes": [
                {"ingredients": ["eggs", "bread"]},
                {"ingredients": ["salad", "chicken"]}
            ]
        }
        
        result = await food_agent.process_request(request_data, {})
        
        assert result["status"] == "success"
        assert "grocery_list" in result["data"]
        assert len(result["data"]["grocery_list"]) == 4 # eggs, bread, salad, chicken

    @pytest.mark.asyncio
    async def test_process_request_dietary_analysis(self, food_agent):
        """Test dietary analysis request processing."""
        request_data = {
            "type": "dietary_analysis",
            "food_items": ["apple", "chicken breast"]
        }
        
        result = await food_agent.process_request(request_data, {})
        
        assert result["status"] == "success"
        assert "total_calories" in result["data"]
        assert result["data"]["total_calories"] == 400

    @pytest.mark.asyncio
    async def test_process_request_general_assistance(self, food_agent):
        """Test processing a general request."""
        request_data = {
            "type": "invalid_task",
            "query": "tell me about food"
        }
        
        result = await food_agent.process_request(request_data, {})
        
        assert result["status"] == "success"
        assert "suggestion" in result["data"]
        assert "available_actions" in result["data"]

    def test_update_dietary_preferences(self, food_agent):
        """Test updating dietary preferences."""
        restrictions = ["vegetarian", "gluten-free"]
        allergies = ["nuts", "dairy"]
        cuisine_preferences = ["Italian", "Mediterranean"]
        
        food_agent.update_dietary_preferences(restrictions, allergies, cuisine_preferences)
        
        assert food_agent.dietary_restrictions == restrictions
        assert food_agent.allergies == allergies
        assert food_agent.cuisine_preferences == cuisine_preferences
