from typing import Dict, Any, List, Optional
import logging
import json
import re
from datetime import datetime

# Import agents
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.food_agent import FoodAgent
from agents.travel_agent import TravelAgent
from agents.shopping_agent import ShoppingAgent
from agents.quick_commerce_agent import QuickCommerceAgent
from agents.payment_agent import PaymentAgent
from agents.base_agent import AgentMessage

logger = logging.getLogger(__name__)

class MasterAgent:
    """Master agent that coordinates all other agents and handles user requests"""
    
    def __init__(self, agents: Optional[Dict[str, Any]] = None):
        if agents:
            self.agents = agents
        else:
            self.agents = {
                "food": FoodAgent(),
                "travel": TravelAgent(),
                "shopping": ShoppingAgent(),
                "quick_commerce": QuickCommerceAgent(),
                "payment": PaymentAgent()
            }
        self.user_context = {}
        self.conversation_history = []
        self.task_queue = []
        
        logger.info("MasterAgent initialized with all domain agents")
    
    async def process(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main entry point for processing user requests"""
        try:
            user_message = request_data.get("message", "")
            user_id = request_data.get("user_id", "default_user")
            
            logger.info(f"Processing request from user {user_id}: {user_message}")
            
            # Analyze intent and determine required agents
            intent_analysis = await self._analyze_intent(user_message)
            
            # Create context for this request
            context = {
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "intent": intent_analysis,
                "user_context": self.user_context.get(user_id, {}),
                "conversation_history": self.conversation_history[-10:]  # Last 10 messages
            }
            
            # Route to appropriate agents
            agent_responses = await self._route_to_agents(intent_analysis, context)
            
            # Synthesize responses
            unified_response = await self._synthesize_responses(agent_responses, context)
            
            # Update user context
            self._update_user_context(user_id, intent_analysis, unified_response)
            
            # Add to conversation history
            self.conversation_history.append({
                "user_message": user_message,
                "intent": intent_analysis,
                "agent_responses": agent_responses,
                "unified_response": unified_response,
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"Successfully processed request for user {user_id}")
            return unified_response
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return {
                "status": "error",
                "message": f"An error occurred while processing your request: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _analyze_intent(self, user_message: str) -> Dict[str, Any]:
        """Analyze user intent and determine which agents to involve"""
        message_lower = user_message.lower()
        
        # Define intent patterns
        food_patterns = [
            r'\b(meals?|foods?|recipes?|cook|dinner|lunch|breakfast|grocery|ingredients?|diet|nutrition)\b',
            r'\b(plan.*meal|what.*eat|hungry|calorie|healthy)\b'
        ]
        
        travel_patterns = [
            r'\b(travels?|trips?|vacations?|flights?|hotels?|bookings?|destinations?|itinerary|itineraries)\b',
            r'\b(go.*to|visit.*|book.*flight|find.*hotel)\b'
        ]
        
        shopping_patterns = [
            r'\b(buy|purchase|shop|products?|prices?|deals?|discounts?|compare|order)\b',
            r'\b(find.*product|best.*price|shopping.*list|compare.*prices)\b'
        ]
        
        quick_commerce_patterns = [
            r'\b(order|get|buy)\s+(tomatoes|milk|bread|eggs|onions|potatoes|rice|dal|vegetables|fruits)\b',
            r'\b(quick|fast)\s+(delivery|order|grocery)\b',
            r'\b(zepto|blinkit|swiggy.*instamart|bigbasket)\b',
            r'\b(10.*min|fifteen.*min|quick.*commerce)\b'
        ]
        
        payment_patterns = [
            r'\b(pay|payment|razorpay|upi|card|wallet|bank|transfer|refund)\b',
            r'\b(create.*order|verify.*payment|payment.*link|transaction)\b'
        ]
        
        # Check patterns
        intents = {
            "food": any(re.search(pattern, message_lower) for pattern in food_patterns),
            "travel": any(re.search(pattern, message_lower) for pattern in travel_patterns),
            "shopping": any(re.search(pattern, message_lower) for pattern in shopping_patterns),
            "quick_commerce": any(re.search(pattern, message_lower) for pattern in quick_commerce_patterns),
            "payment": any(re.search(pattern, message_lower) for pattern in payment_patterns)
        }
        
        logger.info(f"Intents detected: {intents}")
        
        # Determine primary intent (prioritize quick commerce for grocery items)
        primary_intent = None
        if intents["quick_commerce"]:
            primary_intent = "quick_commerce"
        elif intents["payment"]:
            primary_intent = "payment"
        elif intents["food"]:
            primary_intent = "food"
        elif intents["travel"]:
            primary_intent = "travel"
        elif intents["shopping"]:
            primary_intent = "shopping"
        else:
            # Default to general assistance
            primary_intent = "general"
        
        # Extract specific task type
        task_type = self._extract_task_type(user_message, primary_intent)
        
        return {
            "primary_intent": primary_intent,
            "involved_agents": [agent for agent, involved in intents.items() if involved],
            "task_type": task_type,
            "confidence": 0.8,  # Mock confidence score
            "extracted_data": self._extract_data(user_message, primary_intent)
        }
    
    def _extract_task_type(self, user_message: str, primary_intent: str) -> str:
        """Extract specific task type from user message"""
        message_lower = user_message.lower()
        
        if primary_intent == "food":
            if any(word in message_lower for word in ["plan", "meal", "dinner", "lunch", "breakfast"]):
                return "meal_planning"
            elif any(word in message_lower for word in ["recipe", "cook", "ingredient"]):
                return "recipe_generation"
            elif any(word in message_lower for word in ["grocery", "shopping", "list"]):
                return "grocery_list"
            else:
                return "general"
        
        elif primary_intent == "travel":
            if any(word in message_lower for word in ["plan", "trip", "vacation"]):
                return "trip_planning"
            elif any(word in message_lower for word in ["flight", "fly", "airline"]):
                return "flight_search"
            elif any(word in message_lower for word in ["hotel", "accommodation", "stay"]):
                return "hotel_search"
            elif any(word in message_lower for word in ["itinerary", "schedule", "plan"]):
                return "itinerary_generation"
            else:
                return "general"
        
        elif primary_intent == "shopping":
            if any(word in message_lower for word in ["find", "product", "discover"]):
                return "product_discovery"
            elif any(word in message_lower for word in ["compare", "price", "cheaper"]):
                return "price_comparison"
            elif any(word in message_lower for word in ["deal", "discount", "sale"]):
                return "deal_finding"
            elif any(word in message_lower for word in ["list", "buy", "purchase"]):
                return "shopping_list"
            else:
                return "general"
        
        elif primary_intent == "quick_commerce":
            if any(word in message_lower for word in ["order", "get", "buy"]) and any(word in message_lower for word in ["tomatoes", "milk", "bread", "eggs", "onions", "potatoes", "rice", "dal", "vegetables", "fruits"]):
                return "quick_order"
            elif any(word in message_lower for word in ["compare", "price", "best", "deal"]):
                return "compare_prices"
            elif any(word in message_lower for word in ["status", "track", "where"]):
                return "order_status"
            else:
                return "quick_order"
        
        elif primary_intent == "payment":
            if any(word in message_lower for word in ["create", "order", "payment"]):
                return "create_order"
            elif any(word in message_lower for word in ["verify", "payment", "signature"]):
                return "verify_payment"
            elif any(word in message_lower for word in ["link", "payment.*link"]):
                return "create_payment_link"
            elif any(word in message_lower for word in ["refund", "return", "money"]):
                return "refund_payment"
            elif any(word in message_lower for word in ["methods", "payment.*methods"]):
                return "get_payment_methods"
            elif any(word in message_lower for word in ["history", "transaction", "past"]):
                return "get_transaction_history"
            else:
                return "general"
        
        return "general"
    
    def _extract_data(self, user_message: str, primary_intent: str) -> Dict[str, Any]:
        """Extract relevant data from user message"""
        extracted = {}
        
        # Extract budget information
        budget_match = re.search(r'\$(\d+)', user_message)
        if budget_match:
            extracted["budget"] = int(budget_match.group(1))
        
        # Extract amount for payments
        amount_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:rupees?|rs|inr|dollars?|usd)', user_message.lower())
        if amount_match:
            extracted["amount"] = float(amount_match.group(1))
        
        # Extract dates
        date_patterns = [
            r'(\d{1,2}/\d{1,2}/\d{4})',
            r'(\d{4}-\d{2}-\d{2})',
            r'(today|tomorrow|next week)'
        ]
        for pattern in date_patterns:
            date_match = re.search(pattern, user_message)
            if date_match:
                extracted["date"] = date_match.group(1)
                break
        
        # Extract quantities
        quantity_match = re.search(r'(\d+)\s*(people|person|travelers?)', user_message)
        if quantity_match:
            extracted["travelers"] = int(quantity_match.group(1))
        
        # Extract grocery items for quick commerce
        grocery_items = []
        grocery_keywords = ["tomatoes", "milk", "bread", "eggs", "onions", "potatoes", "rice", "dal", "vegetables", "fruits", "chicken", "fish", "cheese", "butter"]
        for keyword in grocery_keywords:
            if keyword in user_message.lower():
                grocery_items.append(keyword)
        if grocery_items:
            extracted["grocery_items"] = grocery_items
        
        # Extract locations/destinations
        location_patterns = [
            r'(?:to|in|at)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'(?:visit|go to)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        ]
        for pattern in location_patterns:
            location_match = re.search(pattern, user_message)
            if location_match:
                extracted["destination"] = location_match.group(1)
                break
        
        # Extract payment IDs
        payment_id_match = re.search(r'(?:payment|order)\s*(?:id|#)?\s*([a-zA-Z0-9_-]+)', user_message)
        if payment_id_match:
            extracted["payment_id"] = payment_id_match.group(1)
        
        return extracted
    
    async def _route_to_agents(self, intent_analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Route request to appropriate agents"""
        agent_responses = {}
        primary_intent = intent_analysis["primary_intent"]
        task_type = intent_analysis["task_type"]
        extracted_data = intent_analysis["extracted_data"]
        
        # Route to primary agent
        if primary_intent in self.agents:
            agent = self.agents[primary_intent]
            
            # Special handling for quick commerce
            if primary_intent == "quick_commerce":
                request_data = {
                    "type": task_type,
                    "items": extracted_data.get("grocery_items", []),
                    "query": context.get("user_message", ""),
                    **extracted_data
                }
            else:
                request_data = {
                    "type": task_type,
                    "query": context.get("user_message", ""),
                    **extracted_data
                }
            
            try:
                response = await agent.process_request(request_data, context)
                agent_responses[primary_intent] = response
                logger.info(f"Successfully routed to {primary_intent} agent")
            except Exception as e:
                logger.error(f"Error routing to {primary_intent} agent: {str(e)}")
                agent_responses[primary_intent] = {
                    "status": "error",
                    "message": f"Error processing {primary_intent} request: {str(e)}"
                }
        
        # Route to secondary agents if needed
        for agent_name in intent_analysis["involved_agents"]:
            if agent_name != primary_intent and agent_name in self.agents:
                agent = self.agents[agent_name]
                request_data = {
                    "type": "general",
                    "query": context.get("user_message", ""),
                    "context": f"Primary request handled by {primary_intent} agent"
                }
                
                try:
                    response = await agent.process_request(request_data, context)
                    agent_responses[agent_name] = response
                except Exception as e:
                    logger.error(f"Error routing to {agent_name} agent: {str(e)}")
        
        return agent_responses
    
    async def _synthesize_responses(self, agent_responses: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize responses from multiple agents into unified response"""
        if not agent_responses:
            return {
                "status": "error",
                "message": "No agents were able to process your request",
                "timestamp": datetime.now().isoformat()
            }
        
        # Get primary response
        primary_agent = context["intent"]["primary_intent"]
        primary_response = agent_responses.get(primary_agent, {})
        
        # Build unified response
        unified_response = {
            "status": "success",
            "message": "Here's what I found for you:",
            "primary_response": primary_response.get("data", {}),
            "agent_used": primary_agent,
            "timestamp": datetime.now().isoformat(),
            "context": {
                "intent": context["intent"]["primary_intent"],
                "task_type": context["intent"]["task_type"]
            }
        }
        
        # Add secondary responses if available
        secondary_responses = {}
        for agent_name, response in agent_responses.items():
            if agent_name != primary_agent and response.get("status") == "success":
                secondary_responses[agent_name] = response.get("data", {})
        
        if secondary_responses:
            unified_response["additional_suggestions"] = secondary_responses
        
        # Add recommendations
        unified_response["recommendations"] = self._generate_recommendations(
            context["intent"], primary_response, secondary_responses
        )
        
        return unified_response
    
    def _generate_recommendations(self, intent: Dict[str, Any], primary_response: Dict[str, Any], 
                                secondary_responses: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on responses"""
        recommendations = []
        
        # Add context-specific recommendations
        if intent["primary_intent"] == "food":
            recommendations.extend([
                "Consider your dietary restrictions when planning meals",
                "Check your pantry before creating grocery lists",
                "Plan meals for the week to save time and money"
            ])
        elif intent["primary_intent"] == "travel":
            recommendations.extend([
                "Book flights and hotels early for better prices",
                "Check travel advisories for your destination",
                "Consider travel insurance for international trips"
            ])
        elif intent["primary_intent"] == "shopping":
            recommendations.extend([
                "Compare prices across multiple vendors",
                "Look for seasonal sales and discounts",
                "Check return policies before making purchases"
            ])
        elif intent["primary_intent"] == "quick_commerce":
            recommendations.extend([
                "Orders are automatically optimized for best price and delivery time",
                "Set auto-approve threshold for small savings",
                "Track your orders in real-time",
                "Consider bulk ordering to save on delivery fees"
            ])
        elif intent["primary_intent"] == "payment":
            recommendations.extend([
                "Always verify payment signatures for security",
                "Keep transaction records for future reference",
                "Use secure payment methods like UPI or cards"
            ])
        
        return recommendations
    
    def _update_user_context(self, user_id: str, intent_analysis: Dict[str, Any], response: Dict[str, Any]):
        """Update user context with new information"""
        if user_id not in self.user_context:
            self.user_context[user_id] = {}
        
        # Update preferences based on interactions
        user_context = self.user_context[user_id]
        
        # Track interaction patterns
        if "interaction_history" not in user_context:
            user_context["interaction_history"] = []
        
        user_context["interaction_history"].append({
            "intent": intent_analysis["primary_intent"],
            "task_type": intent_analysis["task_type"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 50 interactions
        if len(user_context["interaction_history"]) > 50:
            user_context["interaction_history"] = user_context["interaction_history"][-50:]
        
        # Update preferences based on extracted data
        extracted_data = intent_analysis["extracted_data"]
        if "budget" in extracted_data:
            user_context["preferred_budget"] = extracted_data["budget"]
        if "amount" in extracted_data:
            user_context["preferred_amount"] = extracted_data["amount"]
        if "destination" in extracted_data:
            user_context["preferred_destinations"] = user_context.get("preferred_destinations", [])
            if extracted_data["destination"] not in user_context["preferred_destinations"]:
                user_context["preferred_destinations"].append(extracted_data["destination"])
        
        logger.info(f"Updated context for user {user_id}")
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        status = {}
        for agent_name, agent in self.agents.items():
            status[agent_name] = {
                "status": "active",
                "context_summary": agent.get_context_summary(),
                "last_activity": datetime.now().isoformat()
            }
        return status 