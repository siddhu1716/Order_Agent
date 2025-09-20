from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentMessage(BaseModel):
    """Standard message format for inter-agent communication"""
    agent_id: str
    message_type: str  # "request" | "response" | "alert"
    context: Dict[str, Any]
    data: Dict[str, Any]
    priority: str = "medium"  # "low" | "medium" | "high"
    requires_response: bool = True
    timestamp: datetime = datetime.now()

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.user_preferences = {}
        self.conversation_history = []
        logger.info(f"Initialized {self.agent_id}")
    
    @abstractmethod
    async def process_request(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a request and return a response"""
        pass
    
    def update_user_preferences(self, preferences: Dict[str, Any]):
        """Update user preferences for this agent"""
        self.user_preferences.update(preferences)
        logger.info(f"Updated preferences for {self.agent_id}: {preferences}")
    
    def add_to_history(self, message: AgentMessage):
        """Add message to conversation history"""
        self.conversation_history.append(message)
        # Keep only last 100 messages to prevent memory bloat
        if len(self.conversation_history) > 100:
            self.conversation_history = self.conversation_history[-100:]
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get a summary of the agent's context and preferences"""
        return {
            "agent_id": self.agent_id,
            "preferences": self.user_preferences,
            "recent_messages": len(self.conversation_history),
            "last_activity": self.conversation_history[-1].timestamp if self.conversation_history else None
        }
    
    async def send_message(self, target_agent: str, message_type: str, data: Dict[str, Any], 
                          context: Dict[str, Any], priority: str = "medium") -> AgentMessage:
        """Send a message to another agent"""
        message = AgentMessage(
            agent_id=self.agent_id,
            message_type=message_type,
            context=context,
            data=data,
            priority=priority
        )
        self.add_to_history(message)
        logger.info(f"{self.agent_id} sending {message_type} message to {target_agent}")
        return message 