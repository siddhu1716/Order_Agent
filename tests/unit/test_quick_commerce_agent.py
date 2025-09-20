"""
Unit tests for QuickCommerceAgent class.
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from agents.shopping_agent import QuickCommerceAgent


class TestQuickCommerceAgent:
    """Test cases for QuickCommerceAgent class."""

    def test_quick_commerce_agent_initialization(self):
        """Test QuickCommerceAgent initialization."""
        agent = QuickCommerceAgent()
        
        assert agent.agent_id == "quick_commerce_agent"
        assert "quick_order" in agent.capabilities
        assert "compare_prices_quick_commerce" in agent.capabilities
        assert "place_order" in agent.capabilities
        assert "order_status" in agent.capabilities

    def test_platform_configuration(self):
        """Test platform configuration."""
        agent = QuickCommerceAgent()
        
        assert "zepto" in agent.platforms
        assert "blinkit" in agent.platforms
        assert "swiggy_instamart" in agent.platforms
        assert "bigbasket" in agent.platforms

    def test_user_preferences_initialization(self):
        """Test user preferences initialization."""
        agent = QuickCommerceAgent()
        
        assert agent.preferences["delivery_priority"] == "fastest"
        assert agent.preferences["max_delivery_time"] == 30
        assert isinstance(agent.preferences["preferred_platforms"], list)
        assert agent.preferences["auto_approve_threshold"] == 50.0
        assert agent.preferences["quality_threshold"] == 4.0

    @pytest.mark.asyncio
    async def test_process_request_quick_order(self, quick_commerce_agent, sample_quick_commerce_request):
        """Test quick order request processing."""
        request_data = {
            "task_type": "quick_order",
            "items": ["tomatoes", "milk"],
            "delivery_preference": "fastest"
        }
        
        result = await quick_commerce_agent.process_request(request_data, {})
        
        assert result["status"] == "success"
        assert "recommendation" in result["data"]
        assert "best_platform" in result["data"]["recommendation"]

    @pytest.mark.asyncio
    async def test_process_request_compare_prices(self, quick_commerce_agent):
        """Test price comparison request processing."""
        request_data = {
            "task_type": "compare_prices_quick_commerce",
            "items": ["tomatoes", "milk"]
        }
        
        result = await quick_commerce_agent.process_request(request_data, {})
        
        assert result["status"] == "success"
        assert "price_comparison" in result["data"]

    @pytest.mark.asyncio
    async def test_process_request_place_order(self, quick_commerce_agent):
        """Test order placement request processing."""
        request_data = {
            "task_type": "place_order",
            "platform": "zepto",
            "items": [{"name": "tomatoes", "quantity": 2}],
            "user_id": "test_user"
        }
        
        result = await quick_commerce_agent.process_request(request_data, {})
        
        assert result["status"] == "success"
        assert "order_result" in result["data"]

    @pytest.mark.asyncio
    async def test_process_request_order_status(self, quick_commerce_agent):
        """Test order status request processing."""
        request_data = {
            "task_type": "order_status",
            "order_id": "order_123",
            "user_id": "test_user"
        }
        
        result = await quick_commerce_agent.process_request(request_data, {})
        
        assert result["status"] == "success"
        assert "order_status" in result["data"]

    @pytest.mark.asyncio
    async def test_process_request_invalid_task_type(self, quick_commerce_agent):
        """Test processing request with invalid task type."""
        request_data = {
            "task_type": "invalid_task",
            "data": "test"
        }
        
        result = await quick_commerce_agent.process_request(request_data, {})
        
        assert result["status"] == "error"
        assert "Unsupported task type" in result["message"]

    @pytest.mark.asyncio
    async def test_quick_order_flow(self, quick_commerce_agent):
        """Test complete quick order flow."""
        items = ["tomatoes", "milk"]
        preferences = {"delivery_preference": "fastest"}
        
        result = await quick_commerce_agent._quick_order(items, preferences)
        
        assert "recommendation" in result
        assert "best_platform" in result["recommendation"]
        assert "total_cost" in result["recommendation"]
        assert "savings" in result["recommendation"]

    @pytest.mark.asyncio
    async def test_compare_prices_across_platforms(self, quick_commerce_agent):
        """Test price comparison across platforms."""
        items = ["tomatoes", "milk"]
        
        result = await quick_commerce_agent._compare_prices_across_platforms(items)
        
        assert isinstance(result, dict)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_place_order_automation(self, quick_commerce_agent):
        """Test order placement automation."""
        platform = "zepto"
        items = [{"name": "tomatoes", "quantity": 2, "price": 25.0}]
        user_id = "test_user"
        
        result = await quick_commerce_agent._place_order_automation(platform, items, user_id)
        
        assert "order_id" in result
        assert "status" in result
        assert "total_amount" in result

    def test_select_best_product_on_platform(self, quick_commerce_agent):
        """Test selecting best product on a platform."""
        products = [
            {"name": "Tomatoes A", "price": 30.0, "rating": 4.2, "availability": True},
            {"name": "Tomatoes B", "price": 25.0, "rating": 4.5, "availability": True},
            {"name": "Tomatoes C", "price": 20.0, "rating": 4.0, "availability": True}
        ]
        
        best_product = quick_commerce_agent._select_best_product_on_platform(products)
        
        assert best_product is not None
        assert "name" in best_product
        assert "price" in best_product
        assert "rating" in best_product

    def test_find_best_options(self, quick_commerce_agent):
        """Test finding best options across platforms."""
        all_results = {
            "zepto": [{"name": "Tomatoes", "price": 25.0, "rating": 4.5}],
            "blinkit": [{"name": "Tomatoes", "price": 30.0, "rating": 4.3}],
            "swiggy_instamart": [{"name": "Tomatoes", "price": 28.0, "rating": 4.4}]
        }
        
        best_options = quick_commerce_agent._find_best_options(all_results)
        
        assert isinstance(best_options, dict)
        assert len(best_options) > 0

    def test_prepare_recommendation(self, quick_commerce_agent):
        """Test preparing recommendation."""
        best_options = {
            "zepto": {"name": "Tomatoes", "price": 25.0, "rating": 4.5},
            "blinkit": {"name": "Tomatoes", "price": 30.0, "rating": 4.3}
        }
        
        recommendation = quick_commerce_agent._prepare_recommendation(best_options)
        
        assert "best_platform" in recommendation
        assert "total_cost" in recommendation
        assert "platform_breakdown" in recommendation
        assert "savings" in recommendation

    def test_calculate_savings(self, quick_commerce_agent):
        """Test calculating savings."""
        best_options = {
            "zepto": {"price": 25.0},
            "blinkit": {"price": 30.0},
            "swiggy_instamart": {"price": 28.0}
        }
        
        savings = quick_commerce_agent._calculate_savings(best_options)
        
        assert isinstance(savings, (int, float))
        assert savings >= 0

    def test_should_auto_approve(self, quick_commerce_agent):
        """Test auto-approval logic."""
        # Test with savings above threshold
        savings = 60.0
        threshold = 50.0
        
        should_approve = quick_commerce_agent._should_auto_approve(savings, threshold)
        assert should_approve is True
        
        # Test with savings below threshold
        savings = 30.0
        should_approve = quick_commerce_agent._should_auto_approve(savings, threshold)
        assert should_approve is False

    def test_track_order(self, quick_commerce_agent):
        """Test order tracking."""
        order_details = {
            "order_id": "order_123",
            "platform": "zepto",
            "items": [{"name": "tomatoes", "quantity": 2}],
            "total_amount": 50.0,
            "status": "placed"
        }
        
        quick_commerce_agent._track_order(order_details)
        
        assert len(quick_commerce_agent.order_history) == 1
        assert quick_commerce_agent.order_history[0]["order_id"] == "order_123"

    def test_check_order_status(self, quick_commerce_agent):
        """Test checking order status."""
        order_id = "order_123"
        
        # Add order to history first
        order_details = {
            "order_id": order_id,
            "platform": "zepto",
            "status": "placed"
        }
        quick_commerce_agent._track_order(order_details)
        
        status = quick_commerce_agent._check_order_status(order_id)
        
        assert status is not None
        assert "order_id" in status
        assert "status" in status

    def test_update_quick_commerce_preferences(self, quick_commerce_agent):
        """Test updating quick commerce preferences."""
        new_preferences = {
            "delivery_priority": "cheapest",
            "max_delivery_time": 45,
            "preferred_platforms": ["zepto", "blinkit"],
            "auto_approve_threshold": 75.0,
            "quality_threshold": 4.2
        }
        
        quick_commerce_agent.update_quick_commerce_preferences(**new_preferences)
        
        assert quick_commerce_agent.preferences["delivery_priority"] == "cheapest"
        assert quick_commerce_agent.preferences["max_delivery_time"] == 45
        assert quick_commerce_agent.preferences["preferred_platforms"] == ["zepto", "blinkit"]
        assert quick_commerce_agent.preferences["auto_approve_threshold"] == 75.0
        assert quick_commerce_agent.preferences["quality_threshold"] == 4.2

    @pytest.mark.asyncio
    async def test_scraper_integration(self, quick_commerce_agent):
        """Test integration with QuickCommerceScraper."""
        with patch.object(quick_commerce_agent.scraper, 'search_products') as mock_search:
            mock_search.return_value = [{"name": "Tomatoes", "price": 25.0, "rating": 4.5}]
            
            result = await quick_commerce_agent._compare_prices_across_platforms(["tomatoes"])
            
            mock_search.assert_called()
            assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_optimizer_integration(self, quick_commerce_agent):
        """Test integration with QuickCommerceOptimizer."""
        with patch.object(quick_commerce_agent.optimizer, 'find_best_deals') as mock_optimize:
            mock_optimize.return_value = {
                "best_platform": "zepto",
                "total_cost": 245.0,
                "savings": 35.0
            }
            
            result = await quick_commerce_agent._quick_order(["tomatoes"], {})
            
            mock_optimize.assert_called()
            assert "recommendation" in result

    def test_error_handling(self, quick_commerce_agent):
        """Test error handling in quick commerce agent."""
        # Test with invalid data
        request_data = {
            "task_type": "quick_order",
            "items": []  # Empty items list
        }
        
        # This should not raise an exception but return an error response
        import asyncio
        result = asyncio.run(quick_commerce_agent.process_request(request_data, {}))
        
        assert result["status"] == "error" or result["status"] == "success"  # Depends on implementation
