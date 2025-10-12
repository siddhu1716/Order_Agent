from typing import Dict, Any, List
import logging
from datetime import datetime

from .shopping_agent import ShoppingAgent

logger = logging.getLogger(__name__)

class QuickCommerceAgent(ShoppingAgent):
    """Enhanced ShoppingAgent specialized in quick commerce optimization
    Platforms: Zepto, Blinkit, Swiggy Instamart, BigBasket
    """

    def __init__(self):
        super().__init__()
        self.agent_id = "QuickCommerceAgent"
        self.quick_commerce_platforms = ["zepto", "blinkit", "swiggy_instamart", "bigbasket"]
        self.order_history: List[Dict[str, Any]] = []
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
        if not self.scraper:
            return {"status": "error", "message": "Quick commerce scraper not available", "agent_id": self.agent_id}

        logger.info(f"QuickCommerceAgent comparing prices for {len(items)} items")
        comparison_results = await self._compare_prices_across_platforms(items)
        best_options = self._find_best_options(comparison_results)
        recommendation = self._prepare_recommendation(best_options, items)
        auto_approve = self._should_auto_approve(recommendation)

        if auto_approve:
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
        comparison_results: Dict[str, Any] = {}
        for platform in self.quick_commerce_platforms:
            platform_results: Dict[str, Any] = {}
            for item in items:
                try:
                    products = await self.scraper.search_products(platform, item)
                    if products:
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
        if not products:
            return {}
        products.sort(key=lambda x: (x.get("rating", 0), -x.get("price", 0)), reverse=True)
        best_product = products[0]
        best_product["platform"] = platform
        return best_product

    def _find_best_options(self, comparison_results: Dict[str, Any]) -> Dict[str, Any]:
        best_options: Dict[str, Any] = {}
        all_items = set()
        for platform_results in comparison_results.values():
            all_items.update(platform_results.keys())
        for item in all_items:
            item_options = []
            for platform, platform_results in comparison_results.items():
                if item in platform_results and platform_results[item].get("price", 0) > 0:
                    item_options.append(platform_results[item])
            if item_options:
                best_option = min(item_options, key=lambda x: x["price"])
                best_options[item] = best_option
        return best_options

    def _prepare_recommendation(self, best_options: Dict[str, Any], requested_items: List[str]) -> Dict[str, Any]:
        total_cost = 0
        platform_breakdown: Dict[str, Any] = {}
        items: List[Dict[str, Any]] = []
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
        best_platform = max(platform_breakdown.keys(), key=lambda x: len(platform_breakdown[x]["items"]))
        total_with_delivery = sum(breakdown["subtotal"] + breakdown["delivery_fee"] for breakdown in platform_breakdown.values())
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
        if len(platform_breakdown) < 2:
            return 0
        costs = [breakdown["subtotal"] + breakdown["delivery_fee"] for breakdown in platform_breakdown.values()]
        if len(costs) > 1:
            costs.sort()
            return costs[1] - costs[0]
        return 0

    def _should_auto_approve(self, recommendation: Dict[str, Any]) -> bool:
        savings = recommendation.get("savings", 0)
        auto_approve_threshold = self.user_preferences.get("auto_approve_threshold", 50)
        return savings >= auto_approve_threshold

    async def _place_order_automation(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        platform = data.get("platform")
        items = data.get("items", [])
        user_id = context.get("user_id", "default_user")
        if not self.scraper:
            return {"status": "error", "message": "Order automation not available", "agent_id": self.agent_id}
        try:
            order_result = await self.scraper.place_order(platform, items, user_id)
            if order_result.get("status") == "success":
                self._track_order(order_result, user_id)
            logger.info(f"QuickCommerceAgent placed order on {platform}")
            return {"status": "success", "data": order_result, "agent_id": self.agent_id}
        except Exception as e:
            logger.error(f"Error placing order: {str(e)}")
            return {"status": "error", "message": f"Order placement failed: {str(e)}", "agent_id": self.agent_id}

    def _track_order(self, order_result: Dict[str, Any], user_id: str):
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
        if len(self.order_history) > 100:
            self.order_history = self.order_history[-100:]

    async def _check_order_status(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        order_id = data.get("order_id")
        user_id = context.get("user_id", "default_user")
        order = next((o for o in self.order_history if o["order_id"] == order_id and o["user_id"] == user_id), None)
        if not order:
            return {"status": "error", "message": "Order not found", "agent_id": self.agent_id}
        order["status"] = "out_for_delivery"
        order["estimated_delivery"] = "5 minutes"
        return {"status": "success", "data": {"order": order, "current_status": order["status"]}, "agent_id": self.agent_id}

    def update_quick_commerce_preferences(self, delivery_priority: str = None,
                                          preferred_platforms: List[str] = None,
                                          auto_approve_threshold: float = None,
                                          quality_threshold: float = None):
        if delivery_priority:
            self.user_preferences["delivery_priority"] = delivery_priority
        if preferred_platforms:
            self.user_preferences["preferred_platforms"] = preferred_platforms
        if auto_approve_threshold:
            self.user_preferences["auto_approve_threshold"] = auto_approve_threshold
        if quality_threshold:
            self.user_preferences["quality_threshold"] = quality_threshold
        logger.info(f"Updated quick commerce preferences: {self.user_preferences}")
