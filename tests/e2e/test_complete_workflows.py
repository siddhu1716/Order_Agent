"""
End-to-end tests for complete user workflows.
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from main import app


class TestCompleteWorkflows:
    """End-to-end tests for complete user workflows."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    def test_complete_meal_planning_workflow(self, client):
        """Test complete meal planning workflow."""
        # Step 1: Plan a meal
        meal_request = {
            "message": "Plan a healthy dinner for tonight with 500 calories",
            "user_id": "test_user",
            "context": {"dietary_restrictions": ["vegetarian"]}
        }
        
        response = client.post("/assistant", json=meal_request)
        assert response.status_code == 200
        meal_data = response.json()
        assert meal_data["status"] == "success"
        assert meal_data["agent_used"] == "food"
        
        # Step 2: Generate grocery list from meal plan
        grocery_request = {
            "message": "Create a grocery list from the meal plan",
            "user_id": "test_user",
            "context": meal_data["data"]
        }
        
        response = client.post("/assistant", json=grocery_request)
        assert response.status_code == 200
        grocery_data = response.json()
        assert grocery_data["status"] == "success"
        
        # Step 3: Order groceries via quick commerce
        order_request = {
            "message": "Order the groceries from the list",
            "user_id": "test_user",
            "context": grocery_data["data"]
        }
        
        response = client.post("/assistant", json=order_request)
        assert response.status_code == 200
        order_data = response.json()
        assert order_data["status"] == "success"
        assert order_data["agent_used"] == "quick_commerce"

    def test_complete_travel_planning_workflow(self, client):
        """Test complete travel planning workflow."""
        # Step 1: Search for flights
        flight_request = {
            "message": "Find flights from New York to Paris for next week",
            "user_id": "test_user",
            "context": {"departure_date": "2024-01-20", "return_date": "2024-01-27"}
        }
        
        response = client.post("/assistant", json=flight_request)
        assert response.status_code == 200
        flight_data = response.json()
        assert flight_data["status"] == "success"
        assert flight_data["agent_used"] == "travel"
        
        # Step 2: Find hotels
        hotel_request = {
            "message": "Find hotels in Paris for 3 nights",
            "user_id": "test_user",
            "context": {"check_in": "2024-01-20", "check_out": "2024-01-23"}
        }
        
        response = client.post("/assistant", json=hotel_request)
        assert response.status_code == 200
        hotel_data = response.json()
        assert hotel_data["status"] == "success"
        
        # Step 3: Create itinerary
        itinerary_request = {
            "message": "Create a 3-day itinerary for Paris",
            "user_id": "test_user",
            "context": {"duration": 3, "interests": ["museums", "food"]}
        }
        
        response = client.post("/assistant", json=itinerary_request)
        assert response.status_code == 200
        itinerary_data = response.json()
        assert itinerary_data["status"] == "success"

    def test_complete_shopping_workflow(self, client):
        """Test complete shopping workflow."""
        # Step 1: Search for products
        search_request = {
            "message": "Find wireless headphones under $100",
            "user_id": "test_user",
            "context": {"budget": 100, "category": "electronics"}
        }
        
        response = client.post("/assistant", json=search_request)
        assert response.status_code == 200
        search_data = response.json()
        assert search_data["status"] == "success"
        assert search_data["agent_used"] == "shopping"
        
        # Step 2: Compare prices
        compare_request = {
            "message": "Compare prices for the best options",
            "user_id": "test_user",
            "context": search_data["data"]
        }
        
        response = client.post("/assistant", json=compare_request)
        assert response.status_code == 200
        compare_data = response.json()
        assert compare_data["status"] == "success"
        
        # Step 3: Create payment order
        payment_request = {
            "message": "Create a payment order for the selected product",
            "user_id": "test_user",
            "context": compare_data["data"]
        }
        
        response = client.post("/assistant", json=payment_request)
        assert response.status_code == 200
        payment_data = response.json()
        assert payment_data["status"] == "success"
        assert payment_data["agent_used"] == "payment"

    def test_complete_quick_commerce_workflow(self, client):
        """Test complete quick commerce workflow."""
        # Step 1: Place quick order
        order_request = {
            "items": ["tomatoes", "milk", "bread"],
            "user_id": "test_user",
            "delivery_preference": "fastest",
            "auto_approve": False
        }
        
        response = client.post("/quick-order", json=order_request)
        assert response.status_code == 200
        order_data = response.json()
        assert order_data["status"] == "success"
        
        # Step 2: Approve order
        if order_data["data"]["action"] == "awaiting_approval":
            approval_request = {
                "order_id": order_data["data"]["order_result"]["order_id"],
                "approved": True,
                "user_id": "test_user"
            }
            
            response = client.post("/quick-order/approve", json=approval_request)
            assert response.status_code == 200
            approval_data = response.json()
            assert approval_data["status"] == "success"
        
        # Step 3: Check order status
        order_id = order_data["data"]["order_result"]["order_id"]
        response = client.get(f"/quick-order/status/{order_id}?user_id=test_user")
        assert response.status_code == 200
        status_data = response.json()
        assert status_data["status"] == "success"

    def test_voice_command_workflow(self, client):
        """Test voice command workflow."""
        # Step 1: Transcribe audio
        files = {"file": ("test_audio.wav", b"fake audio content", "audio/wav")}
        data = {"language": "en"}
        
        response = client.post("/speech-to-text", files=files, data=data)
        assert response.status_code == 200
        transcription_data = response.json()
        assert transcription_data["status"] == "success"
        assert "transcription" in transcription_data["data"]
        
        # Step 2: Process transcribed command
        command_request = {
            "message": transcription_data["data"]["transcription"],
            "user_id": "test_user",
            "context": {}
        }
        
        response = client.post("/assistant", json=command_request)
        assert response.status_code == 200
        command_data = response.json()
        assert command_data["status"] == "success"

    def test_multi_agent_collaboration_workflow(self, client):
        """Test workflow involving multiple agents."""
        # Step 1: Plan a meal (Food Agent)
        meal_request = {
            "message": "Plan a healthy lunch for 2 people",
            "user_id": "test_user",
            "context": {}
        }
        
        response = client.post("/assistant", json=meal_request)
        assert response.status_code == 200
        meal_data = response.json()
        assert meal_data["agent_used"] == "food"
        
        # Step 2: Find ingredients via shopping (Shopping Agent)
        shopping_request = {
            "message": "Find the best prices for the ingredients needed",
            "user_id": "test_user",
            "context": meal_data["data"]
        }
        
        response = client.post("/assistant", json=shopping_request)
        assert response.status_code == 200
        shopping_data = response.json()
        assert shopping_data["agent_used"] == "shopping"
        
        # Step 3: Order via quick commerce (Quick Commerce Agent)
        quick_order_request = {
            "message": "Order the ingredients for quick delivery",
            "user_id": "test_user",
            "context": shopping_data["data"]
        }
        
        response = client.post("/assistant", json=quick_order_request)
        assert response.status_code == 200
        order_data = response.json()
        assert order_data["agent_used"] == "quick_commerce"
        
        # Step 4: Process payment (Payment Agent)
        payment_request = {
            "message": "Create payment for the order",
            "user_id": "test_user",
            "context": order_data["data"]
        }
        
        response = client.post("/assistant", json=payment_request)
        assert response.status_code == 200
        payment_data = response.json()
        assert payment_data["agent_used"] == "payment"

    def test_error_recovery_workflow(self, client):
        """Test error recovery in workflows."""
        # Step 1: Make a request that might fail
        invalid_request = {
            "message": "Order invalid items that don't exist",
            "user_id": "test_user",
            "context": {}
        }
        
        response = client.post("/assistant", json=invalid_request)
        assert response.status_code == 200
        error_data = response.json()
        
        # Step 2: Make a valid request after error
        valid_request = {
            "message": "Order tomatoes and milk",
            "user_id": "test_user",
            "context": {}
        }
        
        response = client.post("/assistant", json=valid_request)
        assert response.status_code == 200
        valid_data = response.json()
        assert valid_data["status"] == "success"

    def test_user_preference_persistence_workflow(self, client):
        """Test that user preferences persist across requests."""
        user_id = "preference_test_user"
        
        # Step 1: Set dietary preferences
        preference_request = {
            "message": "I'm vegetarian and allergic to nuts",
            "user_id": user_id,
            "context": {}
        }
        
        response = client.post("/assistant", json=preference_request)
        assert response.status_code == 200
        
        # Step 2: Request meal plan (should respect preferences)
        meal_request = {
            "message": "Plan a dinner for me",
            "user_id": user_id,
            "context": {}
        }
        
        response = client.post("/assistant", json=meal_request)
        assert response.status_code == 200
        meal_data = response.json()
        assert meal_data["status"] == "success"
        
        # Step 3: Request another meal (preferences should still apply)
        another_meal_request = {
            "message": "Suggest a lunch option",
            "user_id": user_id,
            "context": {}
        }
        
        response = client.post("/assistant", json=another_meal_request)
        assert response.status_code == 200
        another_meal_data = response.json()
        assert another_meal_data["status"] == "success"

    def test_concurrent_user_workflows(self, client):
        """Test multiple users using the system concurrently."""
        import threading
        import time
        
        results = []
        
        def user_workflow(user_id):
            # Each user performs a different workflow
            workflows = [
                {"message": "Plan a meal", "expected_agent": "food"},
                {"message": "Find flights to Paris", "expected_agent": "travel"},
                {"message": "Compare laptop prices", "expected_agent": "shopping"},
                {"message": "Order groceries", "expected_agent": "quick_commerce"},
                {"message": "Create payment order", "expected_agent": "payment"}
            ]
            
            workflow = workflows[int(user_id) % len(workflows)]
            request = {
                "message": workflow["message"],
                "user_id": f"user_{user_id}",
                "context": {}
            }
            
            response = client.post("/assistant", json=request)
            results.append({
                "user_id": f"user_{user_id}",
                "status_code": response.status_code,
                "agent_used": response.json().get("agent_used"),
                "expected_agent": workflow["expected_agent"]
            })
        
        # Create multiple threads for different users
        threads = []
        for i in range(10):
            thread = threading.Thread(target=user_workflow, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all requests succeeded
        assert len(results) == 10
        assert all(result["status_code"] == 200 for result in results)
        
        # Verify agents were used correctly
        for result in results:
            assert result["agent_used"] == result["expected_agent"]
