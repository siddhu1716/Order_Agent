# mcp/quick_commerce_scraper.py
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from typing import Dict, Any, List, Optional
import json
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class QuickCommerceScraper:
    """Web scraper for quick commerce platforms"""
    
    def __init__(self):
        self.platforms = {
            "zepto": {
                "base_url": "https://www.zepto.com",
                "search_url": "https://www.zepto.com/search",
                "selectors": {
                    "product_name": ".product-name",
                    "price": ".price",
                    "rating": ".rating",
                    "availability": ".availability"
                }
            },
            "blinkit": {
                "base_url": "https://blinkit.com",
                "search_url": "https://blinkit.com/search",
                "selectors": {
                    "product_name": ".product-title",
                    "price": ".price-value",
                    "rating": ".rating-stars",
                    "availability": ".stock-status"
                }
            },
            "swiggy_instamart": {
                "base_url": "https://www.swiggy.com/instamart",
                "search_url": "https://www.swiggy.com/instamart/search",
                "selectors": {
                    "product_name": ".product-name",
                    "price": ".price",
                    "rating": ".rating",
                    "availability": ".availability"
                }
            },
            "bigbasket": {
                "base_url": "https://www.bigbasket.com",
                "search_url": "https://www.bigbasket.com/ps/?q=",
                "selectors": {
                    "product_name": ".prod-name, .uiv2-product-name",
                    "price": ".price, .uiv2-price",
                    "rating": ".rating, .uiv2-rating",
                    "availability": ".availability, .uiv2-sold-out"
                }
            }
        }
        
    async def search_products(self, platform: str, query: str) -> List[Dict[str, Any]]:
        """Search products on a specific platform"""
        if platform not in self.platforms:
            raise ValueError(f"Unsupported platform: {platform}")
        
        platform_config = self.platforms[platform]
        
        # Try Selenium for dynamic content, fallback to HTTP parsing
        try:
            products = await self._scrape_with_selenium(platform, query)
            if products:
                return products
        except Exception as e:
            logger.warning(f"Selenium path failed for {platform}: {e}")

        try:
            products = await self._scrape_with_http(platform, query)
            return products
        except Exception as e:
            logger.error(f"HTTP fallback failed for {platform}: {e}")
            return []
    
    async def _scrape_with_selenium(self, platform: str, query: str) -> List[Dict[str, Any]]:
        """Scrape using Selenium for dynamic content"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1280,800")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
        
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            platform_config = self.platforms[platform]
            # Some sites (bigbasket) expect q appended directly
            if platform == "bigbasket":
                search_url = f"{platform_config['search_url']}{query}"
            else:
                search_url = f"{platform_config['search_url']}?q={query}"
            
            driver.get(search_url)
            
            # Wait for products to load
            WebDriverWait(driver, 12).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product, .item, .product-card, .uiv2-card"))
            )
            
            # Extract product data
            products = []
            product_elements = driver.find_elements(By.CSS_SELECTOR, ".product, .item, .product-card, .uiv2-card")
            
            for element in product_elements:
                try:
                    product = {
                        "name": self._extract_text(element, platform_config['selectors']['product_name']),
                        "price": self._extract_price(element, platform_config['selectors']['price']),
                        "rating": self._extract_rating(element, platform_config['selectors']['rating']),
                        "availability": self._extract_text(element, platform_config['selectors']['availability']),
                        "platform": platform,
                        "image_url": self._extract_image_url(element),
                        "product_url": self._extract_product_url(element)
                    }
                    products.append(product)
                except Exception as e:
                    logger.warning(f"Error extracting product: {str(e)}")
                    continue
            
            return products
            
        finally:
            driver.quit()

    async def _scrape_with_http(self, platform: str, query: str) -> List[Dict[str, Any]]:
        """Scrape using HTTP + BeautifulSoup as a fallback (best-effort)."""
        platform_config = self.platforms[platform]
        if platform == "bigbasket":
            url = f"{platform_config['search_url']}{query}"
        else:
            url = f"{platform_config['search_url']}?q={query}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=15) as resp:
                if resp.status != 200:
                    logger.warning(f"HTTP scrape got status {resp.status} for {platform}")
                    return []
                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")

                products: List[Dict[str, Any]] = []
                # Best-effort generic selectors
                cards = soup.select(".product, .item, .product-card, .uiv2-card, .col-sm-12")
                for card in cards[:20]:  # limit to avoid huge outputs
                    try:
                        name_el = card.select_one(platform_config['selectors']['product_name']) or card.select_one("[class*='name']")
                        price_el = card.select_one(platform_config['selectors']['price']) or card.select_one("[class*='price']")
                        rating_el = card.select_one(platform_config['selectors']['rating']) or card.select_one("[class*='rating']")
                        avail_el = card.select_one(platform_config['selectors']['availability']) or card.select_one("[class*='stock'], [class*='avail']")

                        name = (name_el.get_text(strip=True) if name_el else "")
                        price_text = (price_el.get_text(strip=True) if price_el else "")
                        rating_text = (rating_el.get_text(strip=True) if rating_el else "")
                        availability = (avail_el.get_text(strip=True) if avail_el else "")

                        # Parse price
                        try:
                            price = float(''.join(filter(str.isdigit, price_text))) / 100
                        except Exception:
                            price = 0.0
                        # Parse rating
                        try:
                            rating = float(rating_text.split()[0]) if rating_text else 0.0
                        except Exception:
                            rating = 0.0

                        products.append({
                            "name": name,
                            "price": price,
                            "rating": rating,
                            "availability": availability,
                            "platform": platform,
                            "image_url": "",
                            "product_url": url
                        })
                    except Exception as e:
                        logger.debug(f"HTTP parse error on {platform}: {e}")
                        continue

                return products
    
    def _extract_text(self, element, selector: str) -> str:
        """Extract text from element using selector"""
        try:
            sub_element = element.find_element(By.CSS_SELECTOR, selector)
            return sub_element.text.strip()
        except:
            return ""
    
    def _extract_price(self, element, selector: str) -> float:
        """Extract price from element"""
        try:
            price_text = self._extract_text(element, selector)
            # Remove currency symbols and convert to float
            price = float(''.join(filter(str.isdigit, price_text))) / 100
            return price
        except:
            return 0.0
    
    def _extract_rating(self, element, selector: str) -> float:
        """Extract rating from element"""
        try:
            rating_text = self._extract_text(element, selector)
            return float(rating_text.split()[0])
        except:
            return 0.0
    
    def _extract_image_url(self, element) -> str:
        """Extract product image URL"""
        try:
            img_element = element.find_element(By.CSS_SELECTOR, "img")
            return img_element.get_attribute("src")
        except:
            return ""
    
    def _extract_product_url(self, element) -> str:
        """Extract product URL"""
        try:
            link_element = element.find_element(By.CSS_SELECTOR, "a")
            return link_element.get_attribute("href")
        except:
            return ""

class QuickCommerceOptimizer:
    """Optimize orders across multiple platforms"""
    
    def __init__(self):
        self.scraper = QuickCommerceScraper()
    
    async def find_best_deals(self, items: List[str], preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Find best deals across all platforms"""
        all_results = {}
        
        for platform in ["zepto", "blinkit", "swiggy_instamart"]:
            platform_results = {}
            
            for item in items:
                try:
                    products = await self.scraper.search_products(platform, item)
                    if products:
                        # Find best product for this item
                        best_product = self._select_best_product(products, preferences)
                        platform_results[item] = best_product
                except Exception as e:
                    logger.error(f"Error searching {item} on {platform}: {str(e)}")
                    continue
            
            all_results[platform] = platform_results
        
        # Optimize across platforms
        optimized_order = self._optimize_order(all_results, preferences)
        
        return optimized_order
    
    def _select_best_product(self, products: List[Dict], preferences: Dict) -> Dict:
        """Select best product based on preferences"""
        if not products:
            return {}
        
        # Sort by preference (price, rating, availability)
        if preferences.get("priority") == "price":
            products.sort(key=lambda x: x["price"])
        elif preferences.get("priority") == "rating":
            products.sort(key=lambda x: x["rating"], reverse=True)
        else:
            # Default: balance of price and rating
            products.sort(key=lambda x: (x["price"] / 100) - (x["rating"] * 10))
        
        return products[0]
    
    def _optimize_order(self, all_results: Dict, preferences: Dict) -> Dict:
        """Optimize order across platforms"""
        optimization = {
            "recommended_platform": None,
            "total_cost": 0,
            "delivery_time": 0,
            "items": [],
            "savings": 0
        }
        
        # Calculate total cost for each platform
        platform_costs = {}
        
        for platform, results in all_results.items():
            total_cost = sum(product.get("price", 0) for product in results.values())
            delivery_fee = 0 if platform in ["zepto", "blinkit"] else 20
            platform_costs[platform] = total_cost + delivery_fee
        
        # Select best platform
        best_platform = min(platform_costs.items(), key=lambda x: x[1])
        optimization["recommended_platform"] = best_platform[0]
        optimization["total_cost"] = best_platform[1]
        optimization["delivery_time"] = 10 if best_platform[0] in ["zepto", "blinkit"] else 30
        optimization["items"] = all_results[best_platform[0]]
        
        # Calculate savings
        if len(platform_costs) > 1:
            sorted_costs = sorted(platform_costs.values())
            optimization["savings"] = sorted_costs[1] - sorted_costs[0]
        
        return optimization
    
    async def place_order(self, platform: str, items: List[Dict], user_id: str) -> Dict[str, Any]:
        """Place order via headless browser automation"""
        try:
            # Initialize browser
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            try:
                platform_config = self.platforms[platform]
                
                # Step 1: Navigate to platform
                driver.get(platform_config["base_url"])
                time.sleep(2)
                
                # Step 2: Handle login (mock - in real implementation, use stored credentials)
                await self._handle_login(driver, platform, user_id)
                
                # Step 3: Add items to cart
                cart_items = []
                for item in items:
                    item_added = await self._add_item_to_cart(driver, platform, item)
                    if item_added:
                        cart_items.append(item)
                
                if not cart_items:
                    return {
                        "status": "error",
                        "message": "No items could be added to cart"
                    }
                
                # Step 4: Proceed to checkout
                checkout_result = await self._proceed_to_checkout(driver, platform, cart_items)
                
                if checkout_result["status"] == "success":
                    # Step 5: Place order
                    order_result = await self._place_order_final(driver, platform, cart_items)
                    
                    return {
                        "status": "success",
                        "order_id": order_result.get("order_id"),
                        "platform": platform,
                        "items": cart_items,
                        "total_amount": sum(item.get("price", 0) for item in cart_items),
                        "estimated_delivery": order_result.get("estimated_delivery"),
                        "tracking_url": order_result.get("tracking_url")
                    }
                else:
                    return checkout_result
                    
            finally:
                driver.quit()
                
        except Exception as e:
            logger.error(f"Error placing order on {platform}: {str(e)}")
            return {
                "status": "error",
                "message": f"Order placement failed: {str(e)}"
            }
    
    async def _handle_login(self, driver, platform: str, user_id: str):
        """Handle login for the platform"""
        # Mock login implementation
        # In real implementation, use stored credentials or OAuth
        logger.info(f"Handling login for {platform} - user {user_id}")
        
        # For demo purposes, we'll assume user is already logged in
        # or handle login flow based on platform
        if platform == "zepto":
            # Handle Zepto login
            pass
        elif platform == "blinkit":
            # Handle Blinkit login
            pass
        elif platform == "swiggy_instamart":
            # Handle Swiggy Instamart login
            pass
    
    async def _add_item_to_cart(self, driver, platform: str, item: Dict) -> bool:
        """Add item to cart"""
        try:
            item_name = item.get("name", "")
            
            # Search for the item
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search'], input[placeholder*='search'], .search-input"))
            )
            search_box.clear()
            search_box.send_keys(item_name)
            search_box.send_keys(Keys.RETURN)
            
            time.sleep(2)
            
            # Find and click the first product
            product_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".product, .item, .product-card"))
            )
            product_element.click()
            
            time.sleep(1)
            
            # Add to cart
            add_to_cart_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='add'], .add-to-cart, .add-btn"))
            )
            add_to_cart_button.click()
            
            time.sleep(1)
            logger.info(f"Added {item_name} to cart on {platform}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding {item.get('name', '')} to cart on {platform}: {str(e)}")
            return False
    
    async def _proceed_to_checkout(self, driver, platform: str, items: List[Dict]) -> Dict[str, Any]:
        """Proceed to checkout"""
        try:
            # Click cart/checkout button
            cart_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".cart, .checkout, .basket, [class*='cart']"))
            )
            cart_button.click()
            
            time.sleep(2)
            
            # Verify items in cart
            cart_items = driver.find_elements(By.CSS_SELECTOR, ".cart-item, .item, .product")
            
            if len(cart_items) >= len(items):
                logger.info(f"Proceeding to checkout on {platform} with {len(cart_items)} items")
                return {"status": "success", "items_count": len(cart_items)}
            else:
                return {
                    "status": "error",
                    "message": f"Expected {len(items)} items, found {len(cart_items)}"
                }
                
        except Exception as e:
            logger.error(f"Error proceeding to checkout on {platform}: {str(e)}")
            return {
                "status": "error",
                "message": f"Checkout failed: {str(e)}"
            }
    
    async def _place_order_final(self, driver, platform: str, items: List[Dict]) -> Dict[str, Any]:
        """Final order placement"""
        try:
            # Click proceed to payment/place order button
            place_order_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='order'], .place-order, .proceed, .checkout"))
            )
            place_order_button.click()
            
            time.sleep(3)
            
            # Generate mock order details
            order_id = f"{platform}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            estimated_delivery = datetime.now() + timedelta(minutes=10)
            
            logger.info(f"Order placed successfully on {platform}: {order_id}")
            
            return {
                "order_id": order_id,
                "estimated_delivery": estimated_delivery.isoformat(),
                "tracking_url": f"https://{platform}.com/track/{order_id}",
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error placing final order on {platform}: {str(e)}")
            return {
                "status": "error",
                "message": f"Final order placement failed: {str(e)}"
            }