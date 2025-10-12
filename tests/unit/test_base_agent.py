"""
Unit tests for BaseAgent class.
"""
import pytest
from unittest.mock import Mock, patch
from agents.base_agent import BaseAgent, AgentMessage
from typing import Dict, Any

# A concrete implementation of BaseAgent for testing purposes
class ConcreteTestAgent(BaseAgent):
    async def process_request(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "success", "data": {"processed": True}}

class TestBaseAgent:
    """Test cases for BaseAgent class."""

    def test_base_agent_initialization(self):
        """Test BaseAgent initialization."""
        agent = ConcreteTestAgent(agent_id="test_agent")
        
        assert agent.agent_id == "test_agent"
        assert agent.user_preferences == {}
        assert agent.conversation_history == []

    def test_update_user_preferences(self):
        """Test updating agent preferences."""
        agent = ConcreteTestAgent(agent_id="test_agent")
        new_preferences = {"new_pref": "new_value"}
        
        agent.update_user_preferences(new_preferences)
        
        assert agent.user_preferences == new_preferences

    def test_add_to_history(self):
        """Test adding entries to agent history."""
        agent = ConcreteTestAgent(agent_id="test_agent")
        message = AgentMessage(agent_id="user", message_type="request", context={}, data={})
        
        agent.add_to_history(message)
        
        assert len(agent.conversation_history) == 1
        assert agent.conversation_history[0] == message

    def test_get_context_summary(self):
        """Test retrieving agent context summary."""
        agent = ConcreteTestAgent(agent_id="test_agent")
        message = AgentMessage(agent_id="user", message_type="request", context={}, data={})
        agent.add_to_history(message)
        
        summary = agent.get_context_summary()
        
        assert summary["agent_id"] == "test_agent"
        assert summary["preferences"] == {}
        assert summary["recent_messages"] == 1
        assert summary["last_activity"] is not None

    @pytest.mark.asyncio
    async def test_process_request_implemented(self):
        """Test that the concrete implementation of process_request works."""
        agent = ConcreteTestAgent(agent_id="test_agent")
        result = await agent.process_request({}, {})
        assert result["status"] == "success"

    def test_abstract_class_instantiation(self):
        """Test that BaseAgent cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseAgent(agent_id="test_agent")
