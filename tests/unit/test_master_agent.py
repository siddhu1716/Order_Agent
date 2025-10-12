"""
Unit tests for MasterAgent class.
"""
import pytest
from unittest.mock import AsyncMock
from master.master_agent import MasterAgent

class TestMasterAgent:
    """Test cases for MasterAgent class."""

    @pytest.mark.asyncio
    async def test_process_food_intent(self):
        """Test processing a food-related request."""
        mock_food_agent = AsyncMock()
        mock_food_agent.process_request.return_value = {"status": "success", "data": {"plan": "..."}}
        agents = {"food": mock_food_agent}
        master_agent = MasterAgent(agents=agents)
        
        request = {"message": "Plan a healthy dinner", "user_id": "test_user"}
        result = await master_agent.process(request)
        
        assert result["status"] == "success"
        assert result["agent_used"] == "food"
        mock_food_agent.process_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_travel_intent(self):
        """Test processing a travel-related request."""
        mock_travel_agent = AsyncMock()
        mock_travel_agent.process_request.return_value = {"status": "success", "data": {"flights": []}}
        agents = {"travel": mock_travel_agent}
        master_agent = MasterAgent(agents=agents)

        request = {"message": "Find flights to Paris", "user_id": "test_user"}
        result = await master_agent.process(request)

        assert result["status"] == "success"
        assert result["agent_used"] == "travel"
        mock_travel_agent.process_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_shopping_intent(self):
        """Test processing a shopping-related request."""
        mock_shopping_agent = AsyncMock()
        mock_shopping_agent.process_request.return_value = {"status": "success", "data": {"deals": []}}
        agents = {"shopping": mock_shopping_agent}
        master_agent = MasterAgent(agents=agents)

        request = {"message": "Find deals on laptops", "user_id": "test_user"}
        result = await master_agent.process(request)

        assert result["status"] == "success"
        assert result["agent_used"] == "shopping"
        mock_shopping_agent.process_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_analyze_intent_logic(self):
        """Test the internal intent analysis logic."""
        master_agent = MasterAgent(agents={})
        # Food
        intent = await master_agent._analyze_intent("Plan a meal")
        assert intent["primary_intent"] == "food"
        # Travel
        intent = await master_agent._analyze_intent("Book a hotel")
        assert intent["primary_intent"] == "travel"

    @pytest.mark.asyncio
    async def test_error_handling_in_process(self):
        """Test that the main process method handles exceptions gracefully."""
        mock_travel_agent = AsyncMock()
        mock_travel_agent.process_request.side_effect = Exception("Agent connection failed")
        agents = {"travel": mock_travel_agent}
        master_agent = MasterAgent(agents=agents)

        request = {"message": "Find flights", "user_id": "test_user"}
        result = await master_agent.process(request)

        assert result["status"] == "error"
        assert "Error processing travel request" in result["message"]
