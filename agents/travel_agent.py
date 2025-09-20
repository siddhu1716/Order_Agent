from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentMessage
import logging
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class TravelAgent(BaseAgent):
    """Agent specialized in travel-related tasks: trip planning, booking, itineraries"""
    
    def __init__(self):
        super().__init__("TravelAgent")
        self.preferred_airlines = []
        self.preferred_hotels = []
        self.budget_preferences = {}
        self.travel_style = "balanced"  # budget, luxury, adventure, etc.
    
    async def process_request(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Process travel-related requests"""
        request_type = data.get("type", "general")
        
        if request_type == "trip_planning":
            return await self._plan_trip(data, context)
        elif request_type == "flight_search":
            return await self._search_flights(data, context)
        elif request_type == "hotel_search":
            return await self._search_hotels(data, context)
        elif request_type == "itinerary_generation":
            return await self._generate_itinerary(data, context)
        elif request_type == "booking_assistance":
            return await self._assist_booking(data, context)
        else:
            return await self._general_travel_assistance(data, context)
    
    async def _plan_trip(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Plan a complete trip based on preferences and constraints"""
        destination = data.get("destination", "Unknown")
        start_date = data.get("start_date", "2024-01-01")
        end_date = data.get("end_date", "2024-01-07")
        budget = data.get("budget", 2000)
        travelers = data.get("travelers", 1)
        
        # Mock trip planning logic
        trip_plan = {
            "destination": destination,
            "duration": "7 days",
            "total_budget": budget,
            "budget_breakdown": {
                "flights": budget * 0.4,
                "accommodation": budget * 0.35,
                "activities": budget * 0.15,
                "food": budget * 0.1
            },
            "recommended_activities": [
                "City walking tour",
                "Local cuisine tasting",
                "Museum visits",
                "Shopping districts"
            ],
            "travel_tips": [
                "Best time to visit: Spring or Fall",
                "Local currency: Check exchange rates",
                "Transportation: Public transit recommended"
            ]
        }
        
        logger.info(f"TravelAgent planned trip to {destination} with {budget} budget")
        return {
            "status": "success",
            "data": trip_plan,
            "agent_id": self.agent_id
        }
    
    async def _search_flights(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Search for available flights"""
        origin = data.get("origin", "NYC")
        destination = data.get("destination", "LAX")
        departure_date = data.get("departure_date", "2024-01-15")
        return_date = data.get("return_date", "2024-01-22")
        passengers = data.get("passengers", 1)
        
        # Mock flight search results
        flights = [
            {
                "airline": "Delta Airlines",
                "flight_number": "DL123",
                "departure": "08:00 AM",
                "arrival": "11:30 AM",
                "duration": "3h 30m",
                "price": 350,
                "stops": 0
            },
            {
                "airline": "American Airlines",
                "flight_number": "AA456",
                "departure": "10:15 AM",
                "arrival": "01:45 PM",
                "duration": "3h 30m",
                "price": 320,
                "stops": 1
            },
            {
                "airline": "United Airlines",
                "flight_number": "UA789",
                "departure": "02:30 PM",
                "arrival": "06:00 PM",
                "duration": "3h 30m",
                "price": 380,
                "stops": 0
            }
        ]
        
        logger.info(f"TravelAgent found {len(flights)} flights from {origin} to {destination}")
        return {
            "status": "success",
            "data": {
                "flights": flights,
                "search_criteria": {
                    "origin": origin,
                    "destination": destination,
                    "departure_date": departure_date,
                    "return_date": return_date,
                    "passengers": passengers
                }
            },
            "agent_id": self.agent_id
        }
    
    async def _search_hotels(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Search for available hotels"""
        location = data.get("location", "Downtown")
        check_in = data.get("check_in", "2024-01-15")
        check_out = data.get("check_out", "2024-01-22")
        guests = data.get("guests", 2)
        budget_per_night = data.get("budget_per_night", 150)
        
        # Mock hotel search results
        hotels = [
            {
                "name": "Grand Hotel",
                "rating": 4.5,
                "price_per_night": 180,
                "amenities": ["WiFi", "Pool", "Gym", "Restaurant"],
                "location": "City Center",
                "distance_from_airport": "15 miles"
            },
            {
                "name": "Comfort Inn",
                "rating": 3.8,
                "price_per_night": 120,
                "amenities": ["WiFi", "Breakfast", "Parking"],
                "location": "Business District",
                "distance_from_airport": "12 miles"
            },
            {
                "name": "Luxury Resort",
                "rating": 4.8,
                "price_per_night": 350,
                "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Beach Access"],
                "location": "Waterfront",
                "distance_from_airport": "25 miles"
            }
        ]
        
        logger.info(f"TravelAgent found {len(hotels)} hotels in {location}")
        return {
            "status": "success",
            "data": {
                "hotels": hotels,
                "search_criteria": {
                    "location": location,
                    "check_in": check_in,
                    "check_out": check_out,
                    "guests": guests,
                    "budget_per_night": budget_per_night
                }
            },
            "agent_id": self.agent_id
        }
    
    async def _generate_itinerary(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a detailed travel itinerary"""
        destination = data.get("destination", "Paris")
        days = data.get("days", 5)
        interests = data.get("interests", ["culture", "food", "sightseeing"])
        
        # Mock itinerary generation
        itinerary = {
            "destination": destination,
            "duration": f"{days} days",
            "daily_plans": []
        }
        
        for day in range(1, days + 1):
            daily_plan = {
                "day": day,
                "morning": f"Breakfast at local café, visit {destination} landmarks",
                "afternoon": f"Lunch at recommended restaurant, explore {destination} neighborhoods",
                "evening": f"Dinner at authentic {destination} restaurant, evening entertainment",
                "accommodation": "Return to hotel for rest"
            }
            itinerary["daily_plans"].append(daily_plan)
        
        itinerary["recommendations"] = [
            "Book popular attractions in advance",
            "Try local cuisine specialties",
            "Use public transportation",
            "Keep emergency contacts handy"
        ]
        
        logger.info(f"TravelAgent generated {days}-day itinerary for {destination}")
        return {
            "status": "success",
            "data": itinerary,
            "agent_id": self.agent_id
        }
    
    async def _assist_booking(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Assist with booking process"""
        booking_type = data.get("booking_type", "flight")
        selection = data.get("selection", {})
        
        # Mock booking assistance
        booking_info = {
            "booking_type": booking_type,
            "confirmation_number": f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "status": "confirmed",
            "total_cost": selection.get("price", 0),
            "booking_details": selection,
            "next_steps": [
                "Check email for confirmation",
                "Download mobile boarding pass",
                "Arrive 2 hours before departure"
            ]
        }
        
        logger.info(f"TravelAgent assisted with {booking_type} booking")
        return {
            "status": "success",
            "data": booking_info,
            "agent_id": self.agent_id
        }
    
    async def _general_travel_assistance(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Provide general travel assistance"""
        query = data.get("query", "")
        
        # Mock general assistance
        response = {
            "suggestion": f"Based on your travel query '{query}', I can help with trip planning, flight searches, hotel bookings, and itinerary creation.",
            "available_actions": [
                "trip_planning",
                "flight_search",
                "hotel_search",
                "itinerary_generation",
                "booking_assistance"
            ]
        }
        
        logger.info(f"TravelAgent provided general assistance for: {query}")
        return {
            "status": "success",
            "data": response,
            "agent_id": self.agent_id
        }
    
    def update_travel_preferences(self, preferred_airlines: List[str], preferred_hotels: List[str],
                                budget_preferences: Dict[str, Any], travel_style: str):
        """Update travel preferences"""
        self.preferred_airlines = preferred_airlines
        self.preferred_hotels = preferred_hotels
        self.budget_preferences = budget_preferences
        self.travel_style = travel_style
        logger.info(f"Updated travel preferences: style={travel_style}, airlines={preferred_airlines}") 