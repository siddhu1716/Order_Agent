"""
Mock clients for testing external API integrations.
"""
from unittest.mock import Mock, AsyncMock
import json
from typing import Dict, Any, List, Optional


class MockFoodAPIClient:
    """Mock FoodAPIClient for testing."""
    
    def __init__(self):
        self.search_recipes = AsyncMock(side_effect=self._mock_search_recipes)
        self.get_recipe_by_id = AsyncMock(side_effect=self._mock_get_recipe_by_id)
        self.get_meal_plan = AsyncMock(side_effect=self._mock_get_meal_plan)
    
    async def _mock_search_recipes(self, query: str, max_results: int = 10, 
                                 diet: Optional[str] = None, 
                                 cuisine: Optional[str] = None) -> List[Dict[str, Any]]:
        """Mock recipe search."""
        return [
            {
                "id": 123,
                "title": f"Mock Recipe for {query}",
                "readyInMinutes": 30,
                "servings": 4,
                "sourceUrl": "https://example.com/recipe",
                "image": "https://example.com/image.jpg",
                "summary": f"A delicious mock recipe for {query}",
                "instructions": "1. Mock step 1\n2. Mock step 2\n3. Serve",
                "ingredients": [
                    {"name": "ingredient1", "amount": 100, "unit": "g"},
                    {"name": "ingredient2", "amount": 2, "unit": "pieces"}
                ]
            }
        ]
    
    async def _mock_get_recipe_by_id(self, recipe_id: int) -> Optional[Dict[str, Any]]:
        """Mock get recipe by ID."""
        return {
            "id": recipe_id,
            "title": f"Mock Recipe {recipe_id}",
            "instructions": "Mock detailed instructions",
            "ingredients": [
                {"name": "mock_ingredient", "amount": 1, "unit": "cup"}
            ],
            "nutrition": {
                "calories": 300,
                "protein": 15,
                "fat": 10,
                "carbohydrates": 40
            }
        }
    
    async def _mock_get_meal_plan(self, calories: int, diet: str = "balanced", 
                                time_frame: str = "day") -> Dict[str, Any]:
        """Mock meal plan generation."""
        return {
            "meals": [
                {
                    "id": 1,
                    "title": "Mock Breakfast",
                    "readyInMinutes": 15,
                    "calories": calories // 4,
                    "ingredients": ["mock_ingredient1", "mock_ingredient2"]
                },
                {
                    "id": 2,
                    "title": "Mock Lunch",
                    "readyInMinutes": 30,
                    "calories": calories // 2,
                    "ingredients": ["mock_ingredient3", "mock_ingredient4"]
                },
                {
                    "id": 3,
                    "title": "Mock Dinner",
                    "readyInMinutes": 45,
                    "calories": calories // 4,
                    "ingredients": ["mock_ingredient5", "mock_ingredient6"]
                }
            ],
            "nutrients": {
                "calories": calories,
                "protein": calories * 0.15,
                "fat": calories * 0.25,
                "carbohydrates": calories * 0.6
            }
        }


class MockGroqWhisperClient:
    """Mock GroqWhisperClient for testing."""
    
    def __init__(self):
        self.transcribe_audio = AsyncMock(side_effect=self._mock_transcribe_audio)
        self.transcribe_audio_bytes = AsyncMock(side_effect=self._mock_transcribe_audio_bytes)
        self.get_supported_languages = Mock(side_effect=self._mock_get_supported_languages)
    
    async def _mock_transcribe_audio(self, audio_file_path: str, 
                                   language: str = "en") -> Dict[str, Any]:
        """Mock audio transcription."""
        return {
            "text": "Mock transcription from audio file",
            "language": language,
            "duration": 5.2,
            "confidence": 0.95
        }
    
    async def _mock_transcribe_audio_bytes(self, audio_bytes: bytes, 
                                         filename: str = "audio.wav", 
                                         language: str = "en") -> Dict[str, Any]:
        """Mock audio bytes transcription."""
        return {
            "text": "Mock transcription from audio bytes",
            "language": language,
            "duration": 3.1,
            "confidence": 0.92
        }
    
    def _mock_get_supported_languages(self) -> Dict[str, Any]:
        """Mock supported languages."""
        return {
            "languages": [
                {"code": "en", "name": "English"},
                {"code": "es", "name": "Spanish"},
                {"code": "fr", "name": "French"},
                {"code": "de", "name": "German"},
                {"code": "hi", "name": "Hindi"}
            ]
        }


class MockRazorpayAPIClient:
    """Mock RazorpayAPIClient for testing."""
    
    def __init__(self):
        self.create_order = AsyncMock(side_effect=self._mock_create_order)
        self.verify_payment_signature = AsyncMock(side_effect=self._mock_verify_payment_signature)
        self.create_payment_link = AsyncMock(side_effect=self._mock_create_payment_link)
        self.refund_payment = AsyncMock(side_effect=self._mock_refund_payment)
        self.fetch_payment = AsyncMock(side_effect=self._mock_fetch_payment)
        self.get_payment_methods = AsyncMock(side_effect=self._mock_get_payment_methods)
    
    async def _mock_create_order(self, amount: float, currency: str = "INR", 
                               receipt: Optional[str] = None, 
                               notes: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Mock order creation."""
        return {
            "id": f"order_mock_{hash(str(amount))}",
            "amount": int(amount * 100),  # Convert to paise
            "currency": currency,
            "status": "created",
            "receipt": receipt or f"receipt_mock_{hash(str(amount))}",
            "notes": notes or {},
            "created_at": 1642234567
        }
    
    async def _mock_verify_payment_signature(self, params_dict: Dict[str, str]) -> Dict[str, Any]:
        """Mock payment signature verification."""
        return {
            "success": True,
            "message": "Payment signature verified successfully",
            "payment_id": params_dict.get("payment_id"),
            "order_id": params_dict.get("order_id")
        }
    
    async def _mock_create_payment_link(self, amount: float, currency: str = "INR", 
                                      description: str = "", 
                                      reference_id: Optional[str] = None) -> Dict[str, Any]:
        """Mock payment link creation."""
        return {
            "id": f"plink_mock_{hash(str(amount))}",
            "amount": int(amount * 100),
            "currency": currency,
            "description": description,
            "reference_id": reference_id or f"ref_mock_{hash(str(amount))}",
            "short_url": f"https://rzp.io/mock_{hash(str(amount))}",
            "status": "created",
            "created_at": 1642234567
        }
    
    async def _mock_refund_payment(self, payment_id: str, amount: float, 
                                 currency: str = "INR", 
                                 notes: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Mock payment refund."""
        return {
            "id": f"rfnd_mock_{hash(payment_id)}",
            "amount": int(amount * 100),
            "currency": currency,
            "payment_id": payment_id,
            "status": "processed",
            "notes": notes or {},
            "created_at": 1642234567
        }
    
    async def _mock_fetch_payment(self, payment_id: str) -> Dict[str, Any]:
        """Mock fetch payment."""
        return {
            "id": payment_id,
            "amount": 50000,
            "currency": "INR",
            "status": "captured",
            "order_id": f"order_mock_{hash(payment_id)}",
            "method": "card",
            "created_at": 1642234567
        }
    
    async def _mock_get_payment_methods(self) -> Dict[str, Any]:
        """Mock get payment methods."""
        return {
            "payment_methods": [
                {"method": "card", "name": "Credit/Debit Card"},
                {"method": "upi", "name": "UPI"},
                {"method": "netbanking", "name": "Net Banking"},
                {"method": "wallet", "name": "Wallet"}
            ]
        }


class MockQuickCommerceScraper:
    """Mock QuickCommerceScraper for testing."""
    
    def __init__(self):
        self.search_products = AsyncMock(side_effect=self._mock_search_products)
        self.place_order = AsyncMock(side_effect=self._mock_place_order)
    
    async def _mock_search_products(self, platform: str, query: str) -> List[Dict[str, Any]]:
        """Mock product search."""
        return [
            {
                "name": f"Mock {query.title()} from {platform.title()}",
                "price": 25.0 + hash(query) % 50,  # Vary price based on query
                "rating": 4.0 + (hash(query) % 10) / 10,  # Vary rating
                "availability": True,
                "image_url": f"https://example.com/{platform}/{query}.jpg",
                "product_url": f"https://{platform}.com/product/{hash(query)}",
                "platform": platform,
                "delivery_time": f"{10 + hash(query) % 20} min"
            }
        ]
    
    async def _mock_place_order(self, platform: str, items: List[Dict], 
                              user_id: str) -> Dict[str, Any]:
        """Mock order placement."""
        total_amount = sum(item.get("price", 25.0) * item.get("quantity", 1) for item in items)
        
        return {
            "order_id": f"order_{platform}_{hash(str(items))}",
            "platform": platform,
            "status": "placed",
            "total_amount": total_amount,
            "estimated_delivery": "2024-01-15T10:30:00Z",
            "tracking_url": f"https://{platform}.com/track/{hash(str(items))}",
            "user_id": user_id,
            "items": items
        }


class MockQuickCommerceOptimizer:
    """Mock QuickCommerceOptimizer for testing."""
    
    def __init__(self):
        self.find_best_deals = AsyncMock(side_effect=self._mock_find_best_deals)
    
    async def _mock_find_best_deals(self, items: List[str], 
                                  preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Mock finding best deals."""
        platforms = ["zepto", "blinkit", "swiggy_instamart", "bigbasket"]
        platform_breakdown = {}
        
        for platform in platforms:
            platform_breakdown[platform] = {
                "subtotal": 200.0 + hash(platform) % 100,
                "delivery_fee": 0 if platform == "zepto" else 15 + hash(platform) % 20,
                "delivery_time": 10 + hash(platform) % 20,
                "total": 200.0 + hash(platform) % 100 + (0 if platform == "zepto" else 15 + hash(platform) % 20)
            }
        
        # Find best platform (lowest total)
        best_platform = min(platform_breakdown.keys(), 
                          key=lambda p: platform_breakdown[p]["total"])
        
        # Calculate savings compared to second best
        sorted_platforms = sorted(platform_breakdown.keys(), 
                                key=lambda p: platform_breakdown[p]["total"])
        savings = platform_breakdown[sorted_platforms[1]]["total"] - platform_breakdown[best_platform]["total"]
        
        return {
            "best_platform": best_platform,
            "total_cost": platform_breakdown[best_platform]["total"],
            "savings": max(0, savings),
            "delivery_time": platform_breakdown[best_platform]["delivery_time"],
            "platform_breakdown": platform_breakdown,
            "summary": f"Best deal found on {best_platform.title()} for ₹{platform_breakdown[best_platform]['total']:.0f}"
        }


# Factory function to create mock clients
def create_mock_clients():
    """Create all mock clients for testing."""
    return {
        "food_api_client": MockFoodAPIClient(),
        "whisper_client": MockGroqWhisperClient(),
        "razorpay_client": MockRazorpayAPIClient(),
        "quick_commerce_scraper": MockQuickCommerceScraper(),
        "quick_commerce_optimizer": MockQuickCommerceOptimizer()
    }
