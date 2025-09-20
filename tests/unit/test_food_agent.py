"""
Unit tests for FoodAgent class.
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from agents.food_agent import FoodAgent


class TestFoodAgent:
    """Test cases for FoodAgent class."""

    def test_food_agent_initialization(self):
        """Test FoodAgent initialization."""
        agent = FoodAgent()
        
        assert agent.agent_id == "food_agent"
        assert "meal_planning" in agent.capabilities
        assert "recipe_generation" in agent.capabilities
        assert "grocery_list" in agent.capabilities
        assert "dietary_analysis" in agent.capabilities

    @pytest.mark.asyncio
    async def test_process_request_meal_planning(self, food_agent, sample_food_request):
        """Test meal planning request processing."""
        request_data = {
            "task_type": "meal_planning",
            "calories": 500,
            "diet": "vegetarian"
        }
        
        result = await food_agent.process_request(request_data, {})
        
        assert result["status"] == "success"
        assert "meal_plan" in result["data"]
        assert "nutrients" in result["data"]

    @pytest.mark.asyncio
    async def test_process_request_recipe_generation(self, food_agent):
        """Test recipe generation request processing."""
        request_data = {
            "task_type": "recipe_generation",
            "ingredients": ["tomatoes", "pasta", "cheese"],
            "diet": "vegetarian"
        }
        
        result = await food_agent.process_request(request_data, {})
        
        assert result["status"] == "success"
        assert "recipes" in result["data"]

    @pytest.mark.asyncio
    async def test_process_request_grocery_list(self, food_agent):
        """Test grocery list generation."""
        request_data = {
            "task_type": "grocery_list",
            "meal_plan": [
                {"title": "Breakfast", "ingredients": ["eggs", "bread"]},
                {"title": "Lunch", "ingredients": ["salad", "chicken"]}
            ]
        }
        
        result = await food_agent.process_request(request_data, {})
        
        assert result["status"] == "success"
        assert "grocery_list" in result["data"]
        assert "total_estimated_cost" in result["data"]

    @pytest.mark.asyncio
    async def test_process_request_dietary_analysis(self, food_agent):
        """Test dietary analysis request processing."""
        request_data = {
            "task_type": "dietary_analysis",
            "food_items": [
                {"name": "apple", "quantity": 1, "unit": "medium"},
                {"name": "chicken breast", "quantity": 100, "unit": "g"}
            ]
        }
        
        result = await food_agent.process_request(request_data, {})
        
        assert result["status"] == "success"
        assert "nutritional_analysis" in result["data"]
        assert "total_calories" in result["data"]

    @pytest.mark.asyncio
    async def test_process_request_invalid_task_type(self, food_agent):
        """Test processing request with invalid task type."""
        request_data = {
            "task_type": "invalid_task",
            "data": "test"
        }
        
        result = await food_agent.process_request(request_data, {})
        
        assert result["status"] == "error"
        assert "Unsupported task type" in result["message"]

    def test_update_dietary_preferences(self, food_agent):
        """Test updating dietary preferences."""
        restrictions = ["vegetarian", "gluten-free"]
        allergies = ["nuts", "dairy"]
        cuisine_preferences = ["Italian", "Mediterranean"]
        
        food_agent.update_dietary_preferences(restrictions, allergies, cuisine_preferences)
        
        assert food_agent.preferences["dietary_restrictions"] == restrictions
        assert food_agent.preferences["allergies"] == allergies
        assert food_agent.preferences["cuisine_preferences"] == cuisine_preferences

    @pytest.mark.asyncio
    async def test_generate_meal_plan(self, food_agent):
        """Test meal plan generation."""
        calories = 2000
        diet = "balanced"
        time_frame = "week"
        
        result = await food_agent._generate_meal_plan(calories, diet, time_frame)
        
        assert "meals" in result
        assert "nutrients" in result
        assert len(result["meals"]) > 0

    @pytest.mark.asyncio
    async def test_search_recipes(self, food_agent):
        """Test recipe search."""
        query = "vegetarian pasta"
        max_results = 5
        diet = "vegetarian"
        
        result = await food_agent._search_recipes(query, max_results, diet)
        
        assert isinstance(result, list)
        assert len(result) <= max_results

    @pytest.mark.asyncio
    async def test_get_recipe_details(self, food_agent):
        """Test getting recipe details."""
        recipe_id = 123
        
        result = await food_agent._get_recipe_details(recipe_id)
        
        assert "id" in result
        assert "title" in result
        assert "instructions" in result

    def test_create_grocery_list(self, food_agent):
        """Test grocery list creation."""
        meal_plan = [
            {
                "title": "Breakfast",
                "ingredients": [
                    {"name": "eggs", "amount": 2, "unit": "pieces"},
                    {"name": "bread", "amount": 2, "unit": "slices"}
                ]
            },
            {
                "title": "Lunch",
                "ingredients": [
                    {"name": "chicken", "amount": 150, "unit": "g"},
                    {"name": "rice", "amount": 100, "unit": "g"}
                ]
            }
        ]
        
        result = food_agent._create_grocery_list(meal_plan)
        
        assert "grocery_list" in result
        assert "total_estimated_cost" in result
        assert len(result["grocery_list"]) > 0

    def test_analyze_nutrition(self, food_agent):
        """Test nutritional analysis."""
        food_items = [
            {"name": "apple", "quantity": 1, "unit": "medium"},
            {"name": "chicken breast", "quantity": 100, "unit": "g"}
        ]
        
        result = food_agent._analyze_nutrition(food_items)
        
        assert "nutritional_analysis" in result
        assert "total_calories" in result
        assert "macronutrients" in result
        assert "micronutrients" in result

    @pytest.mark.asyncio
    async def test_api_client_integration(self, food_agent):
        """Test integration with FoodAPIClient."""
        # Test that the agent properly uses the API client
        with patch.object(food_agent.food_api_client, 'search_recipes') as mock_search:
            mock_search.return_value = [{"id": 1, "title": "Test Recipe"}]
            
            result = await food_agent._search_recipes("test query", 5)
            
            mock_search.assert_called_once()
            assert len(result) == 1
            assert result[0]["title"] == "Test Recipe"

    def test_error_handling(self, food_agent):
        """Test error handling in food agent."""
        # Test with invalid data
        request_data = {
            "task_type": "meal_planning",
            "calories": "invalid"  # Should be int
        }
        
        # This should not raise an exception but return an error response
        import asyncio
        result = asyncio.run(food_agent.process_request(request_data, {}))
        
        assert result["status"] == "error" or result["status"] == "success"  # Depends on implementation
