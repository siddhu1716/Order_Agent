"""
Unit tests for BaseAgent class.
"""
import pytest
from unittest.mock import Mock, patch
from agents.base_agent import BaseAgent


class TestBaseAgent:
    """Test cases for BaseAgent class."""

    def test_base_agent_initialization(self):
        """Test BaseAgent initialization."""
        agent = BaseAgent(agent_id="test_agent")
        
        assert agent.agent_id == "test_agent"
        assert agent.capabilities == []
        assert agent.preferences == {}
        assert agent.history == []

    def test_base_agent_with_capabilities(self):
        """Test BaseAgent initialization with capabilities."""
        capabilities = ["test_capability1", "test_capability2"]
        agent = BaseAgent(agent_id="test_agent", capabilities=capabilities)
        
        assert agent.capabilities == capabilities

    def test_base_agent_with_preferences(self):
        """Test BaseAgent initialization with preferences."""
        preferences = {"test_pref": "test_value"}
        agent = BaseAgent(agent_id="test_agent", preferences=preferences)
        
        assert agent.preferences == preferences

    def test_update_preferences(self):
        """Test updating agent preferences."""
        agent = BaseAgent(agent_id="test_agent")
        new_preferences = {"new_pref": "new_value"}
        
        agent.update_preferences(new_preferences)
        
        assert agent.preferences == new_preferences

    def test_add_to_history(self):
        """Test adding entries to agent history."""
        agent = BaseAgent(agent_id="test_agent")
        history_entry = {"timestamp": "2024-01-01", "action": "test_action"}
        
        agent.add_to_history(history_entry)
        
        assert len(agent.history) == 1
        assert agent.history[0] == history_entry

    def test_get_history(self):
        """Test retrieving agent history."""
        agent = BaseAgent(agent_id="test_agent")
        history_entry = {"timestamp": "2024-01-01", "action": "test_action"}
        agent.add_to_history(history_entry)
        
        history = agent.get_history()
        
        assert history == [history_entry]

    def test_clear_history(self):
        """Test clearing agent history."""
        agent = BaseAgent(agent_id="test_agent")
        history_entry = {"timestamp": "2024-01-01", "action": "test_action"}
        agent.add_to_history(history_entry)
        
        agent.clear_history()
        
        assert len(agent.history) == 0

    def test_has_capability(self):
        """Test checking if agent has a specific capability."""
        capabilities = ["capability1", "capability2"]
        agent = BaseAgent(agent_id="test_agent", capabilities=capabilities)
        
        assert agent.has_capability("capability1") is True
        assert agent.has_capability("capability3") is False

    def test_get_agent_info(self):
        """Test getting agent information."""
        capabilities = ["capability1", "capability2"]
        preferences = {"pref1": "value1"}
        agent = BaseAgent(agent_id="test_agent", capabilities=capabilities, preferences=preferences)
        
        info = agent.get_agent_info()
        
        assert info["agent_id"] == "test_agent"
        assert info["capabilities"] == capabilities
        assert info["preferences"] == preferences
        assert "history_count" in info

    @pytest.mark.asyncio
    async def test_process_request_not_implemented(self):
        """Test that process_request raises NotImplementedError."""
        agent = BaseAgent(agent_id="test_agent")
        
        with pytest.raises(NotImplementedError):
            await agent.process_request({}, {})

    def test_str_representation(self):
        """Test string representation of agent."""
        agent = BaseAgent(agent_id="test_agent")
        
        str_repr = str(agent)
        
        assert "test_agent" in str_repr
        assert "BaseAgent" in str_repr

    def test_repr_representation(self):
        """Test repr representation of agent."""
        agent = BaseAgent(agent_id="test_agent")
        
        repr_str = repr(agent)
        
        assert "test_agent" in repr_str
        assert "BaseAgent" in repr_str
