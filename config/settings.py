"""
Application settings and configuration management.
"""
import os
from typing import Dict, Any, List, Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = Field(default="QuickPick Multi-Agent System", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # API Keys
    spoonacular_api_key: Optional[str] = Field(default=None, env="SPOONACULAR_API_KEY")
    groq_api_key: Optional[str] = Field(default=None, env="GROQ_API_KEY")
    razorpay_api_key: Optional[str] = Field(default=None, env="RAZORPAY_API_KEY")
    razorpay_api_secret: Optional[str] = Field(default=None, env="RAZORPAY_API_SECRET")
    razorpay_callback_url: Optional[str] = Field(default=None, env="RAZORPAY_CALLBACK_URL")
    
    # Database
    database_url: Optional[str] = Field(default=None, env="DATABASE_URL")
    redis_url: Optional[str] = Field(default="redis://localhost:6379", env="REDIS_URL")
    
    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    reload: bool = Field(default=False, env="RELOAD")
    
    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        env="CORS_ORIGINS"
    )
    
    # Quick Commerce
    quick_commerce_platforms: List[str] = Field(
        default=["zepto", "blinkit", "swiggy_instamart", "bigbasket"],
        env="QUICK_COMMERCE_PLATFORMS"
    )
    
    # Selenium
    selenium_headless: bool = Field(default=True, env="SELENIUM_HEADLESS")
    selenium_timeout: int = Field(default=30, env="SELENIUM_TIMEOUT")
    selenium_implicit_wait: int = Field(default=10, env="SELENIUM_IMPLICIT_WAIT")
    
    # Rate Limiting
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=3600, env="RATE_LIMIT_WINDOW")  # seconds
    
    # Cache
    cache_ttl: int = Field(default=300, env="CACHE_TTL")  # seconds
    cache_max_size: int = Field(default=1000, env="CACHE_MAX_SIZE")
    
    # Security
    secret_key: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Monitoring
    enable_metrics: bool = Field(default=False, env="ENABLE_METRICS")
    metrics_port: int = Field(default=9090, env="METRICS_PORT")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class AgentSettings:
    """Agent-specific settings."""
    
    # Food Agent
    food_agent = {
        "max_recipes_per_search": 10,
        "default_meal_calories": 2000,
        "supported_diets": ["balanced", "vegetarian", "vegan", "keto", "paleo"],
        "supported_cuisines": ["italian", "mexican", "indian", "chinese", "mediterranean"]
    }
    
    # Travel Agent
    travel_agent = {
        "max_flight_results": 20,
        "max_hotel_results": 15,
        "default_trip_duration": 7,
        "supported_currencies": ["USD", "EUR", "INR", "GBP", "JPY"]
    }
    
    # Shopping Agent
    shopping_agent = {
        "max_product_results": 25,
        "default_budget": 1000,
        "supported_categories": ["electronics", "clothing", "home", "books", "sports"]
    }
    
    # Quick Commerce Agent
    quick_commerce_agent = {
        "default_delivery_preference": "fastest",
        "max_delivery_time": 30,
        "auto_approve_threshold": 50.0,
        "quality_threshold": 4.0,
        "max_order_items": 20
    }
    
    # Payment Agent
    payment_agent = {
        "default_currency": "INR",
        "supported_currencies": ["INR", "USD", "EUR"],
        "payment_methods": ["card", "upi", "netbanking", "wallet"],
        "refund_timeout": 7  # days
    }


class PlatformConfig:
    """Platform-specific configurations."""
    
    zepto = {
        "name": "Zepto",
        "logo": "⚡",
        "base_url": "https://www.zepto.com",
        "search_url": "https://www.zepto.com/search",
        "selectors": {
            "product_name": ".product-name",
            "product_price": ".price",
            "product_rating": ".rating",
            "product_availability": ".availability",
            "product_image": ".product-image img",
            "product_url": ".product-link"
        },
        "delivery_time": "8-12 min",
        "delivery_fee": 0
    }
    
    blinkit = {
        "name": "Blinkit",
        "logo": "🛒",
        "base_url": "https://blinkit.com",
        "search_url": "https://blinkit.com/search",
        "selectors": {
            "product_name": ".product-title",
            "product_price": ".price-value",
            "product_rating": ".rating-stars",
            "product_availability": ".stock-status",
            "product_image": ".product-image img",
            "product_url": ".product-link"
        },
        "delivery_time": "10-15 min",
        "delivery_fee": 15
    }
    
    swiggy_instamart = {
        "name": "Swiggy Instamart",
        "logo": "🍊",
        "base_url": "https://instamart.swiggy.com",
        "search_url": "https://instamart.swiggy.com/search",
        "selectors": {
            "product_name": ".product-name",
            "product_price": ".price",
            "product_rating": ".rating",
            "product_availability": ".availability",
            "product_image": ".product-image img",
            "product_url": ".product-link"
        },
        "delivery_time": "15-20 min",
        "delivery_fee": 25
    }
    
    bigbasket = {
        "name": "BigBasket",
        "logo": "🥬",
        "base_url": "https://www.bigbasket.com",
        "search_url": "https://www.bigbasket.com/ps/?q=",
        "selectors": {
            "product_name": ".prod-name",
            "product_price": ".price",
            "product_rating": ".rating",
            "product_availability": ".availability",
            "product_image": ".prod-img img",
            "product_url": ".prod-link"
        },
        "delivery_time": "25-30 min",
        "delivery_fee": 30
    }


# Global settings instance
settings = Settings()

# Export commonly used configurations
def get_platform_config(platform: str) -> Dict[str, Any]:
    """Get configuration for a specific platform."""
    return getattr(PlatformConfig, platform, {})


def get_agent_settings(agent: str) -> Dict[str, Any]:
    """Get settings for a specific agent."""
    return getattr(AgentSettings, agent, {})


def get_all_platforms() -> List[str]:
    """Get list of all supported platforms."""
    return settings.quick_commerce_platforms


def is_development() -> bool:
    """Check if running in development mode."""
    return settings.debug


def is_production() -> bool:
    """Check if running in production mode."""
    return not settings.debug
