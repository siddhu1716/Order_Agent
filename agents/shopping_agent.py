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
        
        # Mock product discovery
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
                "vendor": "Walmart"
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
                "vendor": "Target"
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
        vendors = data.get("vendors", ["Amazon", "Walmart", "Target", "Best Buy"])
        
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
                    "vendor": "Walmart",
                    "price": 84.99,
                    "shipping": 5.99,
                    "total": 90.98,
                    "delivery_time": "3-5 days",
                    "rating": 4.2
                },
                {
                    "vendor": "Target",
                    "price": 92.99,
                    "shipping": 0.0,
                    "total": 92.99,
                    "delivery_time": "1-2 days",
                    "rating": 4.0
                },
                {
                    "vendor": "Best Buy",
                    "price": 79.99,
                    "shipping": 0.0,
                    "total": 79.99,
                    "delivery_time": "2-4 days",
                    "rating": 4.3
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
                "Walmart": {
                    "items": [item for item in items if "household" in item.lower()],
                    "total_cost": 0,
                    "delivery_time": "3-5 days"
                },
                "Target": {
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
                "vendor": "Walmart",
                "expires": "2024-01-28",
                "category": "home"
            },
            {
                "product": "Running Shoes",
                "original_price": 119.99,
                "sale_price": 89.99,
                "discount": "25% off",
                "vendor": "Target",
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


class QuickCommerceAgent(ShoppingAgent):
    """Enhanced ShoppingAgent specialized in quick commerce optimization"""
    
    def __init__(self):
        super().__init__()
        self.agent_id = "QuickCommerceAgent"
        self.quick_commerce_platforms = ["zepto", "blinkit", "swiggy_instamart", "bigbasket"]
        self.order_history = []
        self.user_preferences = {
            "delivery_priority": "fastest",  # fastest, cheapest, best_rated
            "max_delivery_time": 15,  # minutes
            "preferred_platforms": ["zepto", "blinkit"],
            "auto_approve_threshold": 50,  # Auto-approve if savings > ₹50
            "quality_threshold": 4.0  # minimum rating
        }
        
        # Import scraper
        try:
            from mcp.quick_commerce_scrapper import QuickCommerceScraper, QuickCommerceOptimizer
            self.scraper = QuickCommerceScraper()
            self.optimizer = QuickCommerceOptimizer()
            logger.info("QuickCommerceAgent initialized with scraper")
        except ImportError:
            self.scraper = None
            self.optimizer = None
            logger.warning("Quick commerce scraper not available")
    
    async def process_request(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Process quick commerce requests with enhanced functionality"""
        request_type = data.get("type", "general")
        
        if request_type == "quick_order":
            return await self._quick_order(data, context)
        elif request_type == "compare_prices":
            return await self._compare_prices_quick_commerce(data, context)
        elif request_type == "place_order":
            return await self._place_order_automation(data, context)
        elif request_type == "order_status":
            return await self._check_order_status(data, context)
        else:
            # Fallback to parent class methods
            return await super().process_request(data, context)
    
    async def _quick_order(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Step 1: Compare prices and show best option to user"""
        items = data.get("items", [])
        user_id = context.get("user_id", "default_user")
        
        if not self.scraper:
            return {
                "status": "error",
                "message": "Quick commerce scraper not available",
                "agent_id": self.agent_id
            }
        
        logger.info(f"QuickCommerceAgent comparing prices for {len(items)} items")
        
        # Step 1: Compare prices across platforms
        comparison_results = await self._compare_prices_across_platforms(items)
        
        # Step 2: Find best options
        best_options = self._find_best_options(comparison_results)
        
        # Step 3: Prepare recommendation
        recommendation = self._prepare_recommendation(best_options, items)
        
        # Step 4: Check if auto-approve
        auto_approve = self._should_auto_approve(recommendation)
        
        if auto_approve:
            # Auto-place order
            order_result = await self._place_order_automation({
                "platform": recommendation["best_platform"],
                "items": recommendation["items"]
            }, context)
            
            return {
                "status": "success",
                "data": {
                    "action": "auto_ordered",
                    "recommendation": recommendation,
                    "order_result": order_result,
                    "time_saved": "20-30 minutes"
                },
                "agent_id": self.agent_id
            }
        else:
            # Show recommendation and wait for approval
            return {
                "status": "success",
                "data": {
                    "action": "awaiting_approval",
                    "recommendation": recommendation,
                    "message": "Please approve the order to proceed",
                    "time_saved": "20-30 minutes"
                },
                "agent_id": self.agent_id
            }
    
    async def _compare_prices_across_platforms(self, items: List[str]) -> Dict[str, Any]:
        """Compare prices across all quick commerce platforms"""
        comparison_results = {}
        
        for platform in self.quick_commerce_platforms:
            platform_results = {}
            
            for item in items:
                try:
                    # Use scraper to get product data
                    products = await self.scraper.search_products(platform, item)
                    
                    if products:
                        # Find best product for this item on this platform
                        best_product = self._select_best_product_on_platform(products, platform)
                        platform_results[item] = best_product
                    else:
                        platform_results[item] = {
                            "name": item,
                            "price": 0,
                            "rating": 0,
                            "availability": "Not Available",
                            "platform": platform
                        }
                        
                except Exception as e:
                    logger.error(f"Error searching {item} on {platform}: {str(e)}")
                    platform_results[item] = {
                        "name": item,
                        "price": 0,
                        "rating": 0,
                        "availability": "Error",
                        "platform": platform,
                        "error": str(e)
                    }
            
            comparison_results[platform] = platform_results
        
        return comparison_results
    
    def _select_best_product_on_platform(self, products: List[Dict], platform: str) -> Dict[str, Any]:
        """Select best product on a specific platform"""
        if not products:
            return {}
        
        # Sort by rating first, then by price
        products.sort(key=lambda x: (x.get("rating", 0), -x.get("price", 0)), reverse=True)
        
        best_product = products[0]
        best_product["platform"] = platform
        
        return best_product
    
    def _find_best_options(self, comparison_results: Dict[str, Any]) -> Dict[str, Any]:
        """Find best options across all platforms"""
        best_options = {}
        
        # Get all unique items
        all_items = set()
        for platform_results in comparison_results.values():
            all_items.update(platform_results.keys())
        
        for item in all_items:
            item_options = []
            
            for platform, platform_results in comparison_results.items():
                if item in platform_results and platform_results[item].get("price", 0) > 0:
                    item_options.append(platform_results[item])
            
            if item_options:
                # Find best option for this item
                best_option = min(item_options, key=lambda x: x["price"])
                best_options[item] = best_option
        
        return best_options
    
    def _prepare_recommendation(self, best_options: Dict[str, Any], requested_items: List[str]) -> Dict[str, Any]:
        """Prepare recommendation for user"""
        total_cost = 0
        platform_breakdown = {}
        items = []
        
        for item, option in best_options.items():
            if item in requested_items:
                total_cost += option["price"]
                platform = option["platform"]
                
                if platform not in platform_breakdown:
                    platform_breakdown[platform] = {
                        "items": [],
                        "subtotal": 0,
                        "delivery_fee": 0 if platform in ["zepto", "blinkit"] else 20,
                        "delivery_time": 10 if platform in ["zepto", "blinkit"] else 30
                    }
                
                platform_breakdown[platform]["items"].append(option)
                platform_breakdown[platform]["subtotal"] += option["price"]
                items.append(option)
        
        # Find best platform (most items or lowest cost)
        best_platform = max(platform_breakdown.keys(), key=lambda x: len(platform_breakdown[x]["items"]))
        
        # Calculate total with delivery fees
        total_with_delivery = sum(
            breakdown["subtotal"] + breakdown["delivery_fee"] 
            for breakdown in platform_breakdown.values()
        )
        
        # Calculate savings
        savings = self._calculate_savings(platform_breakdown)
        
        return {
            "best_platform": best_platform,
            "total_cost": total_with_delivery,
            "items": items,
            "platform_breakdown": platform_breakdown,
            "savings": savings,
            "delivery_time": platform_breakdown[best_platform]["delivery_time"],
            "summary": f"Best option: {best_platform.title()} - ₹{total_with_delivery:.2f} total, {platform_breakdown[best_platform]['delivery_time']} min delivery"
        }
    
    def _calculate_savings(self, platform_breakdown: Dict[str, Any]) -> float:
        """Calculate potential savings"""
        if len(platform_breakdown) < 2:
            return 0
        
        costs = [
            breakdown["subtotal"] + breakdown["delivery_fee"] 
            for breakdown in platform_breakdown.values()
        ]
        
        if len(costs) > 1:
            costs.sort()
            return costs[1] - costs[0]  # Savings compared to second-best option
        
        return 0
    
    def _should_auto_approve(self, recommendation: Dict[str, Any]) -> bool:
        """Check if order should be auto-approved"""
        savings = recommendation.get("savings", 0)
        auto_approve_threshold = self.user_preferences.get("auto_approve_threshold", 50)
        
        return savings >= auto_approve_threshold
    
    async def _place_order_automation(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Step 3: Place order via headless browser automation"""
        platform = data.get("platform")
        items = data.get("items", [])
        user_id = context.get("user_id", "default_user")
        
        if not self.scraper:
            return {
                "status": "error",
                "message": "Order automation not available",
                "agent_id": self.agent_id
            }
        
        try:
            # Use scraper's automation capabilities
            order_result = await self.scraper.place_order(platform, items, user_id)
            
            # Track the order
            if order_result.get("status") == "success":
                self._track_order(order_result, user_id)
            
            logger.info(f"QuickCommerceAgent placed order on {platform}")
            return {
                "status": "success",
                "data": order_result,
                "agent_id": self.agent_id
            }
            
        except Exception as e:
            logger.error(f"Error placing order: {str(e)}")
            return {
                "status": "error",
                "message": f"Order placement failed: {str(e)}",
                "agent_id": self.agent_id
            }
    
    def _track_order(self, order_result: Dict[str, Any], user_id: str):
        """Track order in history"""
        order_record = {
            "order_id": order_result.get("order_id"),
            "platform": order_result.get("platform"),
            "user_id": user_id,
            "items": order_result.get("items", []),
            "total_amount": order_result.get("total_amount", 0),
            "order_time": datetime.now().isoformat(),
            "status": "placed"
        }
        
        self.order_history.append(order_record)
        
        # Keep only last 100 orders
        if len(self.order_history) > 100:
            self.order_history = self.order_history[-100:]
    
    async def _check_order_status(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Check order status"""
        order_id = data.get("order_id")
        user_id = context.get("user_id", "default_user")
        
        # Find order in history
        order = next(
            (o for o in self.order_history if o["order_id"] == order_id and o["user_id"] == user_id),
            None
        )
        
        if not order:
            return {
                "status": "error",
                "message": "Order not found",
                "agent_id": self.agent_id
            }
        
        # Mock status update
        order["status"] = "out_for_delivery"
        order["estimated_delivery"] = "5 minutes"
        
        return {
            "status": "success",
            "data": {
                "order": order,
                "current_status": order["status"]
            },
            "agent_id": self.agent_id
        }
    
    def update_quick_commerce_preferences(self, delivery_priority: str = None,
                                        preferred_platforms: List[str] = None,
                                        auto_approve_threshold: float = None,
                                        quality_threshold: float = None):
        """Update quick commerce preferences"""
        if delivery_priority:
            self.user_preferences["delivery_priority"] = delivery_priority
        if preferred_platforms:
            self.user_preferences["preferred_platforms"] = preferred_platforms
        if auto_approve_threshold:
            self.user_preferences["auto_approve_threshold"] = auto_approve_threshold
        if quality_threshold:
            self.user_preferences["quality_threshold"] = quality_threshold
        
        logger.info(f"Updated quick commerce preferences: {self.user_preferences}") 