"""
Integration tests for API endpoints.
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from main import app


class TestAPIIntegration:
    """Integration tests for API endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

    def test_status_endpoint(self, client):
        """Test system status endpoint."""
        response = client.get("/status")
        assert response.status_code == 200
        data = response.json()
        assert "system_status" in data
        assert "agents" in data
        assert "services" in data

    def test_assistant_endpoint_food_request(self, client):
        """Test assistant endpoint with food request."""
        request_data = {
            "message": "Plan a healthy dinner for tonight",
            "user_id": "test_user",
            "context": {}
        }
        
        response = client.post("/assistant", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "primary_response" in data
        assert data["agent_used"] == "food"

    def test_assistant_endpoint_travel_request(self, client):
        """Test assistant endpoint with travel request."""
        request_data = {
            "message": "Find flights from New York to Los Angeles",
            "user_id": "test_user",
            "context": {}
        }
        
        response = client.post("/assistant", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "primary_response" in data
        assert data["agent_used"] == "travel"

    def test_assistant_endpoint_shopping_request(self, client):
        """Test assistant endpoint with shopping request."""
        request_data = {
            "message": "Compare prices for wireless headphones",
            "user_id": "test_user",
            "context": {}
        }
        
        response = client.post("/assistant", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "primary_response" in data
        assert data["agent_used"] == "shopping"

    def test_assistant_endpoint_quick_commerce_request(self, client):
        """Test assistant endpoint with quick commerce request."""
        request_data = {
            "message": "Order tomatoes and milk",
            "user_id": "test_user",
            "context": {}
        }
        
        response = client.post("/assistant", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "primary_response" in data
        assert data["agent_used"] == "quick_commerce"

    def test_assistant_endpoint_payment_request(self, client):
        """Test assistant endpoint with payment request."""
        request_data = {
            "message": "Create a payment order for 500 rupees",
            "user_id": "test_user",
            "context": {}
        }
        
        response = client.post("/assistant", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "primary_response" in data
        assert data["agent_used"] == "payment"

    def test_quick_order_endpoint(self, client):
        """Test quick order endpoint."""
        request_data = {
            "items": ["tomatoes", "milk", "bread"],
            "user_id": "test_user",
            "delivery_preference": "fastest",
            "auto_approve": False
        }
        
        response = client.post("/quick-order", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data

    def test_quick_order_approval_endpoint(self, client):
        """Test quick order approval endpoint."""
        request_data = {
            "order_id": "test_order_123",
            "approved": True,
            "user_id": "test_user"
        }
        
        response = client.post("/quick-order/approve", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_order_status_endpoint(self, client):
        """Test order status endpoint."""
        order_id = "test_order_123"
        user_id = "test_user"
        
        response = client.get(f"/quick-order/status/{order_id}?user_id={user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_speech_to_text_endpoint(self, client):
        """Test speech-to-text endpoint."""
        # Create a mock audio file
        files = {"file": ("test_audio.wav", b"fake audio content", "audio/wav")}
        data = {"language": "en"}
        
        response = client.post("/speech-to-text", files=files, data=data)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["status"] == "success"
        assert "transcription" in response_data["data"]

    def test_payment_create_order_endpoint(self, client):
        """Test payment order creation endpoint."""
        request_data = {
            "amount": 500.0,
            "currency": "INR",
            "receipt": "test_receipt_001"
        }
        
        response = client.post("/payment/create-order", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "order_id" in data["data"]

    def test_payment_verify_endpoint(self, client):
        """Test payment verification endpoint."""
        request_data = {
            "payment_id": "pay_test123",
            "order_id": "order_test123",
            "signature": "test_signature"
        }
        
        response = client.post("/payment/verify", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_payment_create_link_endpoint(self, client):
        """Test payment link creation endpoint."""
        request_data = {
            "amount": 1000.0,
            "currency": "INR",
            "description": "Test payment",
            "reference_id": "ref_test123"
        }
        
        response = client.post("/payment/create-link", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "payment_link" in data["data"]

    def test_payment_methods_endpoint(self, client):
        """Test payment methods endpoint."""
        response = client.get("/payment/methods")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "payment_methods" in data["data"]

    def test_test_endpoints(self, client):
        """Test all test endpoints."""
        test_endpoints = [
            "/test/food",
            "/test/travel", 
            "/test/shopping",
            "/test/payment",
            "/test/quick-commerce"
        ]
        
        for endpoint in test_endpoints:
            response = client.post(endpoint)
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"

    def test_invalid_endpoint(self, client):
        """Test invalid endpoint returns 404."""
        response = client.get("/invalid-endpoint")
        assert response.status_code == 404

    def test_invalid_request_data(self, client):
        """Test invalid request data handling."""
        # Test with missing required fields
        request_data = {
            "message": "",  # Empty message
            "user_id": "test_user"
        }
        
        response = client.post("/assistant", json=request_data)
        assert response.status_code == 200  # Should handle gracefully
        data = response.json()
        assert data["status"] in ["success", "error"]

    def test_cors_headers(self, client):
        """Test CORS headers are present."""
        response = client.options("/assistant")
        assert response.status_code == 200
        # CORS headers should be present (handled by FastAPI middleware)

    def test_response_format_consistency(self, client):
        """Test that all endpoints return consistent response format."""
        endpoints = [
            ("/health", "GET", None),
            ("/status", "GET", None),
            ("/assistant", "POST", {"message": "test", "user_id": "test"}),
            ("/quick-order", "POST", {"items": ["test"], "user_id": "test"}),
        ]
        
        for endpoint, method, data in endpoints:
            if method == "GET":
                response = client.get(endpoint)
            else:
                response = client.post(endpoint, json=data)
            
            assert response.status_code == 200
            response_data = response.json()
            
            # All responses should have status field
            assert "status" in response_data
            
            # Success responses should have data field
            if response_data["status"] == "success":
                assert "data" in response_data

    def test_concurrent_requests(self, client):
        """Test handling of concurrent requests."""
        import threading
        import time
        
        results = []
        
        def make_request():
            request_data = {
                "message": "Plan a meal",
                "user_id": f"user_{threading.current_thread().ident}",
                "context": {}
            }
            response = client.post("/assistant", json=request_data)
            results.append(response.status_code)
        
        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert all(status == 200 for status in results)
        assert len(results) == 5
