"""
Helper utilities for the QuickPick system.
"""
import re
import hashlib
import uuid
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timedelta
import asyncio
import functools


def generate_order_id(platform: str = "quickpick") -> str:
    """
    Generate a unique order ID.
    
    Args:
        platform: Platform name
    
    Returns:
        Unique order ID
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"{platform.upper()}_{timestamp}_{unique_id}"


def generate_user_id() -> str:
    """
    Generate a unique user ID.
    
    Returns:
        Unique user ID
    """
    return f"user_{uuid.uuid4().hex[:12]}"


def sanitize_text(text: str) -> str:
    """
    Sanitize text by removing special characters and normalizing.
    
    Args:
        text: Input text
    
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove special characters except basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    return text


def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """
    Extract keywords from text.
    
    Args:
        text: Input text
        min_length: Minimum keyword length
    
    Returns:
        List of keywords
    """
    if not text:
        return []
    
    # Convert to lowercase and split
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter by length and common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
        'before', 'after', 'above', 'below', 'between', 'among', 'is', 'are',
        'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do',
        'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
        'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
        'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
    }
    
    keywords = [
        word for word in words 
        if len(word) >= min_length and word not in stop_words
    ]
    
    return list(set(keywords))  # Remove duplicates


def calculate_savings(original_price: float, discounted_price: float) -> Dict[str, Any]:
    """
    Calculate savings information.
    
    Args:
        original_price: Original price
        discounted_price: Discounted price
    
    Returns:
        Dictionary with savings information
    """
    if original_price <= 0:
        return {"amount": 0, "percentage": 0, "savings": 0}
    
    savings_amount = original_price - discounted_price
    savings_percentage = (savings_amount / original_price) * 100
    
    return {
        "amount": round(savings_amount, 2),
        "percentage": round(savings_percentage, 2),
        "savings": savings_amount > 0
    }


def format_currency(amount: float, currency: str = "INR") -> str:
    """
    Format currency amount.
    
    Args:
        amount: Amount to format
        currency: Currency code
    
    Returns:
        Formatted currency string
    """
    currency_symbols = {
        "INR": "₹",
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥"
    }
    
    symbol = currency_symbols.get(currency, currency)
    
    if currency == "INR":
        return f"{symbol}{amount:,.0f}"
    else:
        return f"{symbol}{amount:,.2f}"


def parse_delivery_time(time_str: str) -> int:
    """
    Parse delivery time string to minutes.
    
    Args:
        time_str: Delivery time string (e.g., "10-15 min", "30 mins")
    
    Returns:
        Delivery time in minutes
    """
    if not time_str:
        return 0
    
    # Extract numbers from string
    numbers = re.findall(r'\d+', time_str)
    
    if not numbers:
        return 0
    
    # If range (e.g., "10-15"), take average
    if len(numbers) >= 2:
        return (int(numbers[0]) + int(numbers[1])) // 2
    
    return int(numbers[0])


def validate_email(email: str) -> bool:
    """
    Validate email address.
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """
    Validate phone number.
    
    Args:
        phone: Phone number to validate
    
    Returns:
        True if valid, False otherwise
    """
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Check if it's a valid length (7-15 digits)
    return 7 <= len(digits) <= 15


def hash_string(text: str, algorithm: str = "sha256") -> str:
    """
    Hash a string using the specified algorithm.
    
    Args:
        text: Text to hash
        algorithm: Hash algorithm
    
    Returns:
        Hashed string
    """
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(text.encode('utf-8'))
    return hash_obj.hexdigest()


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split a list into chunks of specified size.
    
    Args:
        lst: List to chunk
        chunk_size: Size of each chunk
    
    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple dictionaries.
    
    Args:
        *dicts: Dictionaries to merge
    
    Returns:
        Merged dictionary
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result


def deep_merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two dictionaries.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
    
    Returns:
        Deep merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result


def retry_async(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator for retrying async functions.
    
    Args:
        max_attempts: Maximum number of attempts
        delay: Initial delay between attempts
        backoff: Backoff multiplier
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
            
            return None
        
        return wrapper
    return decorator


def retry_sync(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator for retrying sync functions.
    
    Args:
        max_attempts: Maximum number of attempts
        delay: Initial delay between attempts
        backoff: Backoff multiplier
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    
                    import time
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            return None
        
        return wrapper
    return decorator


def time_execution(func):
    """
    Decorator to measure function execution time.
    
    Args:
        func: Function to measure
    
    Returns:
        Decorated function
    """
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = datetime.utcnow()
        result = await func(*args, **kwargs)
        end_time = datetime.utcnow()
        execution_time = (end_time - start_time).total_seconds()
        
        # Add execution time to result if it's a dict
        if isinstance(result, dict):
            result["execution_time"] = execution_time
        
        return result
    
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = datetime.utcnow()
        result = func(*args, **kwargs)
        end_time = datetime.utcnow()
        execution_time = (end_time - start_time).total_seconds()
        
        # Add execution time to result if it's a dict
        if isinstance(result, dict):
            result["execution_time"] = execution_time
        
        return result
    
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


def normalize_platform_name(platform: str) -> str:
    """
    Normalize platform name.
    
    Args:
        platform: Platform name
    
    Returns:
        Normalized platform name
    """
    platform_mapping = {
        "zepto": "zepto",
        "blinkit": "blinkit",
        "swiggy": "swiggy_instamart",
        "swiggy_instamart": "swiggy_instamart",
        "instamart": "swiggy_instamart",
        "bigbasket": "bigbasket",
        "big_basket": "bigbasket"
    }
    
    return platform_mapping.get(platform.lower(), platform.lower())


def get_platform_display_name(platform: str) -> str:
    """
    Get display name for platform.
    
    Args:
        platform: Platform identifier
    
    Returns:
        Display name
    """
    display_names = {
        "zepto": "Zepto",
        "blinkit": "Blinkit",
        "swiggy_instamart": "Swiggy Instamart",
        "bigbasket": "BigBasket"
    }
    
    return display_names.get(platform.lower(), platform.title())


def calculate_delivery_score(delivery_time: int, rating: float, price: float) -> float:
    """
    Calculate delivery score based on multiple factors.
    
    Args:
        delivery_time: Delivery time in minutes
        rating: Platform rating
        price: Total price
    
    Returns:
        Delivery score (0-100)
    """
    # Time score (lower is better, max 30 points)
    time_score = max(0, 30 - (delivery_time / 2))
    
    # Rating score (max 40 points)
    rating_score = (rating / 5.0) * 40
    
    # Price score (lower is better, max 30 points)
    # Assuming average price of 200 INR
    price_score = max(0, 30 - (price / 10))
    
    return min(100, time_score + rating_score + price_score)
