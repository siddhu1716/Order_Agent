from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentMessage
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class ShoppingAgent(BaseAgent):
    """Agent specialized in shopping-related tasks: product discovery, price comparison, order optimization"""
    
    def __init__(self):
        super().__init__("ShoppingAgent")
        self.preferred_vendors = []
        self.budget_constraints = {}
        self.shopping_history = []
        self.product_preferences = {}
    
    async def process_request(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Process shopping-related requests"""
        request_type = data.get("type", "general")
        
        if request_type == "product_discovery":
            return await self._discover_products(data, context)
        elif request_type == "price_comparison":
            return await self._compare_prices(data, context)
        elif request_type == "order_optimization":
            return await self._optimize_order(data, context)
        elif request_type == "deal_finding":
            return await self._find_deals(data, context)
        elif request_type == "shopping_list":
            return await self._create_shopping_list(data, context)
        else:
            return await self._general_shopping_assistance(data, context)
    
    async def _discover_products(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Discover products based on search criteria"""
        query = data.get("query", "")
        category = data.get("category", "general")
        price_range = data.get("price_range", {"min": 0, "max": 1000})
        brand_preferences = data.get("brand_preferences", [])
        
        # Mock product discovery (Amazon, Flipkart, Myntra)
        products = [
            {
                "id": "prod_001",
                "name": f"Premium {query}",
                "brand": "BrandA",
                "price": 89.99,
                "rating": 4.5,
                "reviews": 1250,
                "features": ["Feature 1", "Feature 2", "Feature 3"],
                "availability": "In Stock",
                "vendor": "Amazon"
            },
            {
                "id": "prod_002",
                "name": f"Standard {query}",
                "brand": "BrandB",
                "price": 59.99,
                "rating": 4.2,
                "reviews": 890,
                "features": ["Feature 1", "Feature 2"],
                "availability": "In Stock",
                "vendor": "Flipkart"
            },
            {
                "id": "prod_003",
                "name": f"Budget {query}",
                "brand": "BrandC",
                "price": 29.99,
                "rating": 3.8,
                "reviews": 456,
                "features": ["Feature 1"],
                "availability": "Limited Stock",
                "vendor": "Myntra"
            }
        ]
        
        # Filter by price range
        filtered_products = [
            p for p in products 
            if price_range["min"] <= p["price"] <= price_range["max"]
        ]
        
        logger.info(f"ShoppingAgent discovered {len(filtered_products)} products for '{query}'")
        return {
            "status": "success",
            "data": {
                "products": filtered_products,
                "search_criteria": {
                    "query": query,
                    "category": category,
                    "price_range": price_range,
                    "brand_preferences": brand_preferences
                }
            },
            "agent_id": self.agent_id
        }
    
    async def _compare_prices(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Compare prices across different vendors"""
        product_name = data.get("product_name", "")
        vendors = data.get("vendors", ["Amazon", "Flipkart", "Myntra"])
        
        # Mock price comparison
        price_comparison = {
            "product": product_name,
            "vendors": [
                {
                    "vendor": "Amazon",
                    "price": 89.99,
                    "shipping": 0.0,
                    "total": 89.99,
                    "delivery_time": "2-3 days",
                    "rating": 4.5
                },
                {
                    "vendor": "Flipkart",
                    "price": 84.99,
                    "shipping": 5.99,
                    "total": 90.98,
                    "delivery_time": "3-5 days",
                    "rating": 4.2
                },
                {
                    "vendor": "Myntra",
                    "price": 92.99,
                    "shipping": 0.0,
                    "total": 92.99,
                    "delivery_time": "1-2 days",
                    "rating": 4.0
                }
            ]
        }
        
        # Find best deal
        best_deal = min(price_comparison["vendors"], key=lambda x: x["total"])
        price_comparison["best_deal"] = best_deal
        
        logger.info(f"ShoppingAgent compared prices for '{product_name}' across {len(vendors)} vendors")
        return {
            "status": "success",
            "data": price_comparison,
            "agent_id": self.agent_id
        }
    
    async def _optimize_order(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize order for best value and delivery"""
        items = data.get("items", [])
        budget = data.get("budget", 500)
        delivery_preference = data.get("delivery_preference", "standard")
        
        # Mock order optimization
        optimized_order = {
            "items": items,
            "total_budget": budget,
            "optimization_strategy": "Best value for money",
            "recommended_vendors": {
                "Amazon": {
                    "items": [item for item in items if "electronics" in item.lower()],
                    "total_cost": 0,
                    "delivery_time": "2-3 days"
                },
                "Flipkart": {
                    "items": [item for item in items if "household" in item.lower()],
                    "total_cost": 0,
                    "delivery_time": "3-5 days"
                },
                "Myntra": {
                    "items": [item for item in items if "clothing" in item.lower()],
                    "total_cost": 0,
                    "delivery_time": "1-2 days"
                }
            },
            "savings_opportunities": [
                "Bundle items from same vendor for free shipping",
                "Use store loyalty programs",
                "Check for manufacturer coupons"
            ]
        }
        
        # Calculate costs (mock)
        total_cost = 0
        for vendor, details in optimized_order["recommended_vendors"].items():
            if details["items"]:
                cost = len(details["items"]) * 25  # Mock cost calculation
                details["total_cost"] = cost
                total_cost += cost
        
        optimized_order["total_cost"] = total_cost
        optimized_order["budget_remaining"] = budget - total_cost
        
        logger.info(f"ShoppingAgent optimized order with {len(items)} items")
        return {
            "status": "success",
            "data": optimized_order,
            "agent_id": self.agent_id
        }
    
    async def _find_deals(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Find current deals and discounts"""
        category = data.get("category", "all")
        max_price = data.get("max_price", 100)
        
        # Mock deal finding
        deals = [
            {
                "product": "Wireless Headphones",
                "original_price": 129.99,
                "sale_price": 79.99,
                "discount": "38% off",
                "vendor": "Amazon",
                "expires": "2024-01-31",
                "category": "electronics"
            },
            {
                "product": "Coffee Maker",
                "original_price": 89.99,
                "sale_price": 59.99,
                "discount": "33% off",
                "vendor": "Flipkart",
                "expires": "2024-01-28",
                "category": "home"
            },
            {
                "product": "Running Shoes",
                "original_price": 119.99,
                "sale_price": 89.99,
                "discount": "25% off",
                "vendor": "Myntra",
                "expires": "2024-01-25",
                "category": "sports"
            }
        ]
        
        # Filter by category and price
        filtered_deals = [
            deal for deal in deals
            if (category == "all" or deal["category"] == category) and
            deal["sale_price"] <= max_price
        ]
        
        logger.info(f"ShoppingAgent found {len(filtered_deals)} deals in {category} category")
        return {
            "status": "success",
            "data": {
                "deals": filtered_deals,
                "search_criteria": {
                    "category": category,
                    "max_price": max_price
                }
            },
            "agent_id": self.agent_id
        }
    
    async def _create_shopping_list(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Create an organized shopping list"""
        items = data.get("items", [])
        budget = data.get("budget", 200)
        priority = data.get("priority", "medium")
        
        # Mock shopping list creation
        shopping_list = {
            "items": [
                {
                    "name": item,
                    "estimated_price": 15.0,
                    "priority": priority,
                    "category": "general",
                    "notes": ""
                }
                for item in items
            ],
            "total_estimated_cost": len(items) * 15.0,
            "budget": budget,
            "budget_remaining": budget - (len(items) * 15.0),
            "organizations": {
                "by_store": {
                    "Grocery Store": [item for item in items if "food" in item.lower()],
                    "Electronics Store": [item for item in items if "tech" in item.lower()],
                    "General Store": [item for item in items if "food" not in item.lower() and "tech" not in item.lower()]
                }
            }
        }
        
        logger.info(f"ShoppingAgent created shopping list with {len(items)} items")
        return {
            "status": "success",
            "data": shopping_list,
            "agent_id": self.agent_id
        }
    
    async def _general_shopping_assistance(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Provide general shopping assistance"""
        query = data.get("query", "")
        
        # Mock general assistance
        response = {
            "suggestion": f"Based on your shopping query '{query}', I can help with product discovery, price comparison, deal finding, and order optimization.",
            "available_actions": [
                "product_discovery",
                "price_comparison",
                "order_optimization",
                "deal_finding",
                "shopping_list"
            ]
        }
        
        logger.info(f"ShoppingAgent provided general assistance for: {query}")
        return {
            "status": "success",
            "data": response,
            "agent_id": self.agent_id
        }
    
    def update_shopping_preferences(self, preferred_vendors: List[str], budget_constraints: Dict[str, Any],
                                  product_preferences: Dict[str, Any]):
        """Update shopping preferences"""
        self.preferred_vendors = preferred_vendors
        self.budget_constraints = budget_constraints
        self.product_preferences = product_preferences
        logger.info(f"Updated shopping preferences: vendors={preferred_vendors}, budget={budget_constraints}")


 