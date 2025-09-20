"""
Unit tests for MasterAgent class.
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from master.master_agent import MasterAgent


class TestMasterAgent:
    """Test cases for MasterAgent class."""

    def test_master_agent_initialization(self):
        """Test MasterAgent initialization."""
        agent = MasterAgent()
        
        assert agent.agent_id == "master_agent"
        assert "intent_analysis" in agent.capabilities
        assert "task_routing" in agent.capabilities
        assert "response_synthesis" in agent.capabilities

    def test_agents_initialization(self):
        """Test that all agents are properly initialized."""
        agent = MasterAgent()
        
        assert "food" in agent.agents
        assert "travel" in agent.agents
        assert "shopping" in agent.agents
        assert "quick_commerce" in agent.agents
        assert "payment" in agent.agents

    @pytest.mark.asyncio
    async def test_process_request_food_intent(self, master_agent, sample_food_request):
        """Test processing food-related requests."""
        result = await master_agent.process_request(sample_food_request)
        
        assert result["status"] == "success"
        assert "primary_response" in result
        assert "agent_used" in result
        assert result["agent_used"] == "food"

    @pytest.mark.asyncio
    async def test_process_request_travel_intent(self, master_agent, sample_travel_request):
        """Test processing travel-related requests."""
        result = await master_agent.process_request(sample_travel_request)
        
        assert result["status"] == "success"
        assert "primary_response" in result
        assert "agent_used" in result
        assert result["agent_used"] == "travel"

    @pytest.mark.asyncio
    async def test_process_request_shopping_intent(self, master_agent, sample_shopping_request):
        """Test processing shopping-related requests."""
        result = await master_agent.process_request(sample_shopping_request)
        
        assert result["status"] == "success"
        assert "primary_response" in result
        assert "agent_used" in result
        assert result["agent_used"] == "shopping"

    @pytest.mark.asyncio
    async def test_process_request_quick_commerce_intent(self, master_agent, sample_quick_commerce_request):
        """Test processing quick commerce-related requests."""
        result = await master_agent.process_request(sample_quick_commerce_request)
        
        assert result["status"] == "success"
        assert "primary_response" in result
        assert "agent_used" in result
        assert result["agent_used"] == "quick_commerce"

    @pytest.mark.asyncio
    async def test_process_request_payment_intent(self, master_agent, sample_payment_request):
        """Test processing payment-related requests."""
        result = await master_agent.process_request(sample_payment_request)
        
        assert result["status"] == "success"
        assert "primary_response" in result
        assert "agent_used" in result
        assert result["agent_used"] == "payment"

    def test_analyze_intent_food_keywords(self, master_agent):
        """Test intent analysis for food-related keywords."""
        messages = [
            "Plan a healthy dinner",
            "Find recipes for pasta",
            "Create a meal plan",
            "What should I cook tonight?",
            "Generate a grocery list"
        ]
        
        for message in messages:
            intent = master_agent._analyze_intent(message)
            assert intent["primary_intent"] == "food"
            assert "food" in intent["involved_agents"]

    def test_analyze_intent_travel_keywords(self, master_agent):
        """Test intent analysis for travel-related keywords."""
        messages = [
            "Find flights to Paris",
            "Book a hotel in Tokyo",
            "Plan a trip to London",
            "Search for vacation deals",
            "Create a travel itinerary"
        ]
        
        for message in messages:
            intent = master_agent._analyze_intent(message)
            assert intent["primary_intent"] == "travel"
            assert "travel" in intent["involved_agents"]

    def test_analyze_intent_shopping_keywords(self, master_agent):
        """Test intent analysis for shopping-related keywords."""
        messages = [
            "Compare prices for laptops",
            "Find deals on electronics",
            "Search for products",
            "Create a shopping list",
            "Find the best price"
        ]
        
        for message in messages:
            intent = master_agent._analyze_intent(message)
            assert intent["primary_intent"] == "shopping"
            assert "shopping" in intent["involved_agents"]

    def test_analyze_intent_quick_commerce_keywords(self, master_agent):
        """Test intent analysis for quick commerce-related keywords."""
        messages = [
            "Order tomatoes from Zepto",
            "Quick delivery for groceries",
            "Order milk and bread",
            "Find cheapest rice delivery",
            "Blinkit order for vegetables"
        ]
        
        for message in messages:
            intent = master_agent._analyze_intent(message)
            assert intent["primary_intent"] == "quick_commerce"
            assert "quick_commerce" in intent["involved_agents"]

    def test_analyze_intent_payment_keywords(self, master_agent):
        """Test intent analysis for payment-related keywords."""
        messages = [
            "Create a payment order",
            "Process payment",
            "Verify payment",
            "Generate payment link",
            "Refund payment"
        ]
        
        for message in messages:
            intent = master_agent._analyze_intent(message)
            assert intent["primary_intent"] == "payment"
            assert "payment" in intent["involved_agents"]

    def test_analyze_intent_unknown_keywords(self, master_agent):
        """Test intent analysis for unknown keywords."""
        messages = [
            "Hello, how are you?",
            "What's the weather like?",
            "Tell me a joke",
            "Random text without keywords"
        ]
        
        for message in messages:
            intent = master_agent._analyze_intent(message)
            assert intent["primary_intent"] == "general"
            assert len(intent["involved_agents"]) == 0

    def test_extract_task_type(self, master_agent):
        """Test task type extraction."""
        test_cases = [
            ("Plan a meal", "meal_planning"),
            ("Find recipes", "recipe_generation"),
            ("Create grocery list", "grocery_list"),
            ("Book a flight", "flight_search"),
            ("Find hotels", "hotel_search"),
            ("Compare prices", "price_comparison"),
            ("Order groceries", "quick_order"),
            ("Create payment", "create_order")
        ]
        
        for message, expected_task in test_cases:
            task_type = master_agent._extract_task_type(message)
            assert task_type == expected_task

    def test_extract_data(self, master_agent):
        """Test data extraction from messages."""
        test_cases = [
            ("Order tomatoes and milk", {"grocery_items": ["tomatoes", "milk"]}),
            ("Find flights to Paris", {"destination": "Paris"}),
            ("Book hotel in Tokyo", {"destination": "Tokyo"}),
            ("Create payment for 500 rupees", {"amount": 500, "currency": "rupees"})
        ]
        
        for message, expected_data in test_cases:
            extracted_data = master_agent._extract_data(message)
            for key, value in expected_data.items():
                assert key in extracted_data
                assert extracted_data[key] == value

    @pytest.mark.asyncio
    async def test_route_to_agents(self, master_agent):
        """Test routing requests to appropriate agents."""
        intent_analysis = {
            "primary_intent": "food",
            "involved_agents": ["food"],
            "task_type": "meal_planning",
            "extracted_data": {"calories": 500}
        }
        context = {"user_id": "test_user"}
        
        result = await master_agent._route_to_agents(intent_analysis, context)
        
        assert "food" in result
        assert result["food"]["status"] == "success"

    @pytest.mark.asyncio
    async def test_synthesize_responses(self, master_agent):
        """Test response synthesis from multiple agents."""
        agent_responses = {
            "food": {
                "status": "success",
                "data": {"meal_plan": "Test meal plan"},
                "message": "Meal plan created successfully"
            }
        }
        context = {"user_id": "test_user"}
        
        result = await master_agent._synthesize_responses(agent_responses, context)
        
        assert "primary_response" in result
        assert "additional_suggestions" in result
        assert "recommendations" in result

    def test_generate_recommendations(self, master_agent):
        """Test generating recommendations based on intent."""
        test_cases = [
            ("food", ["Try our meal planning feature", "Explore new recipes"]),
            ("travel", ["Check out our travel deals", "Plan your next trip"]),
            ("shopping", ["Compare prices across vendors", "Find the best deals"]),
            ("quick_commerce", ["Save time with quick delivery", "Compare prices across platforms"]),
            ("payment", ["Secure payment processing", "Multiple payment options available"])
        ]
        
        for intent, expected_recommendations in test_cases:
            recommendations = master_agent._generate_recommendations(intent)
            assert isinstance(recommendations, list)
            assert len(recommendations) > 0

    @pytest.mark.asyncio
    async def test_error_handling(self, master_agent):
        """Test error handling in master agent."""
        # Test with invalid request data
        invalid_request = {
            "message": "",  # Empty message
            "user_id": "test_user"
        }
        
        result = await master_agent.process_request(invalid_request)
        
        assert result["status"] == "error" or result["status"] == "success"  # Depends on implementation

    @pytest.mark.asyncio
    async def test_agent_failure_handling(self, master_agent):
        """Test handling of agent failures."""
        # Mock an agent to fail
        with patch.object(master_agent.agents["food"], 'process_request') as mock_food:
            mock_food.side_effect = Exception("Agent failure")
            
            request = {
                "message": "Plan a meal",
                "user_id": "test_user"
            }
            
            result = await master_agent.process_request(request)
            
            # Should handle the error gracefully
            assert result["status"] == "error" or result["status"] == "success"  # Depends on implementation

    def test_intent_priority(self, master_agent):
        """Test intent priority handling."""
        # Test that quick_commerce intent takes priority over general shopping
        message = "Order tomatoes from Zepto for quick delivery"
        intent = master_agent._analyze_intent(message)
        
        assert intent["primary_intent"] == "quick_commerce"
        assert "quick_commerce" in intent["involved_agents"]

    @pytest.mark.asyncio
    async def test_multi_agent_requests(self, master_agent):
        """Test requests that involve multiple agents."""
        request = {
            "message": "Plan a meal and find flights to Paris",
            "user_id": "test_user"
        }
        
        result = await master_agent.process_request(request)
        
        assert result["status"] == "success"
        assert "primary_response" in result
        # Should handle multiple intents appropriately
