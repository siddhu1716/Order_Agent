from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentMessage
import logging
import json

logger = logging.getLogger(__name__)

class FoodAgent(BaseAgent):
    """Agent specialized in food-related tasks: meal planning, recipes, grocery lists"""
    
    def __init__(self):
        super().__init__("FoodAgent")
        self.dietary_restrictions = []
        self.cuisine_preferences = []
        self.calorie_targets = {}
        self.allergies = []
    
    async def process_request(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Process food-related requests"""
        request_type = data.get("type", "general")
        
        if request_type == "meal_planning":
            return await self._plan_meal(data, context)
        elif request_type == "recipe_generation":
            return await self._generate_recipe(data, context)
        elif request_type == "grocery_list":
            return await self._create_grocery_list(data, context)
        elif request_type == "dietary_analysis":
            return await self._analyze_dietary_info(data, context)
        else:
            return await self._general_food_assistance(data, context)
    
    async def _plan_meal(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Plan a meal based on preferences and constraints"""
        calories = data.get("calories", 500)
        meal_type = data.get("meal_type", "dinner")
        ingredients = data.get("available_ingredients", [])
        
        # Mock meal planning logic
        meal_plan = {
            "meal_type": meal_type,
            "calories": calories,
            "suggested_recipes": [
                {
                    "name": "Grilled Chicken Salad",
                    "calories": 450,
                    "ingredients": ["chicken breast", "mixed greens", "tomatoes", "olive oil"],
                    "prep_time": "20 minutes",
                    "difficulty": "easy"
                },
                {
                    "name": "Quinoa Bowl",
                    "calories": 480,
                    "ingredients": ["quinoa", "black beans", "avocado", "lime"],
                    "prep_time": "25 minutes",
                    "difficulty": "easy"
                }
            ],
            "nutritional_info": {
                "protein": "25g",
                "carbs": "35g",
                "fat": "15g"
            }
        }
        
        logger.info(f"FoodAgent planned {meal_type} with {calories} calories")
        return {
            "status": "success",
            "data": meal_plan,
            "agent_id": self.agent_id
        }
    
    async def _generate_recipe(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a recipe based on ingredients and preferences"""
        ingredients = data.get("ingredients", [])
        cuisine = data.get("cuisine", "general")
        
        # Mock recipe generation
        recipe = {
            "name": f"Creative {cuisine.title()} Dish",
            "ingredients": ingredients + ["salt", "pepper", "olive oil"],
            "instructions": [
                "Chop all vegetables",
                "Heat oil in pan",
                "Add ingredients in order of cooking time",
                "Season to taste"
            ],
            "cooking_time": "30 minutes",
            "servings": 2,
            "difficulty": "medium"
        }
        
        logger.info(f"FoodAgent generated recipe using {len(ingredients)} ingredients")
        return {
            "status": "success",
            "data": recipe,
            "agent_id": self.agent_id
        }
    
    async def _create_grocery_list(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a grocery list based on meal plans"""
        recipes = data.get("recipes", [])
        budget = data.get("budget", 50)
        
        # Mock grocery list generation
        grocery_items = []
        for recipe in recipes:
            if isinstance(recipe, dict) and "ingredients" in recipe:
                grocery_items.extend(recipe["ingredients"])
        
        # Remove duplicates and add quantities
        unique_items = list(set(grocery_items))
        grocery_list = [
            {"item": item, "quantity": "1 unit", "estimated_cost": 5.0}
            for item in unique_items
        ]
        
        total_estimated_cost = len(grocery_list) * 5.0
        
        logger.info(f"FoodAgent created grocery list with {len(grocery_list)} items")
        return {
            "status": "success",
            "data": {
                "grocery_list": grocery_list,
                "total_estimated_cost": total_estimated_cost,
                "budget_remaining": budget - total_estimated_cost
            },
            "agent_id": self.agent_id
        }
    
    async def _analyze_dietary_info(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze dietary information and provide recommendations"""
        food_items = data.get("food_items", [])
        
        # Mock dietary analysis
        analysis = {
            "total_calories": len(food_items) * 200,
            "protein_content": "moderate",
            "fiber_content": "high" if len(food_items) > 3 else "low",
            "recommendations": [
                "Consider adding more vegetables",
                "Include a protein source",
                "Watch portion sizes"
            ]
        }
        
        logger.info(f"FoodAgent analyzed {len(food_items)} food items")
        return {
            "status": "success",
            "data": analysis,
            "agent_id": self.agent_id
        }
    
    async def _general_food_assistance(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Provide general food assistance"""
        query = data.get("query", "")
        
        # Mock general assistance
        response = {
            "suggestion": f"Based on your query '{query}', I recommend checking our recipe database or meal planning features.",
            "available_actions": [
                "meal_planning",
                "recipe_generation", 
                "grocery_list",
                "dietary_analysis"
            ]
        }
        
        logger.info(f"FoodAgent provided general assistance for: {query}")
        return {
            "status": "success",
            "data": response,
            "agent_id": self.agent_id
        }
    
    def update_dietary_preferences(self, restrictions: List[str], allergies: List[str], 
                                 cuisine_preferences: List[str]):
        """Update dietary preferences and restrictions"""
        self.dietary_restrictions = restrictions
        self.allergies = allergies
        self.cuisine_preferences = cuisine_preferences
        logger.info(f"Updated dietary preferences: {restrictions}, allergies: {allergies}") 