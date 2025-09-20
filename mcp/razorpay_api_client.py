import httpx
import logging
import os
import hmac
import hashlib
from typing import Dict, Any, Optional
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class RazorpayAPIClient:
    """Client for Razorpay payment gateway API"""
    
    def __init__(self):
        self.api_key = os.getenv("RAZORPAY_API_KEY", "mock_key")
        self.api_secret = os.getenv("RAZORPAY_API_SECRET", "mock_secret")
        self.base_url = "https://api.razorpay.com/v1"
        self.client = httpx.AsyncClient(
            auth=(self.api_key, self.api_secret),
            timeout=30.0
        )
        
        logger.info("Razorpay API client initialized")
    
    async def create_order(self, amount: float, currency: str = "INR", 
                          receipt: Optional[str] = None, notes: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Create a new payment order"""
        try:
            # Convert amount to paise (smallest currency unit for INR)
            amount_in_paise = int(amount * 100) if currency == "INR" else int(amount)
            
            order_data = {
                "amount": amount_in_paise,
                "currency": currency,
                "receipt": receipt or f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "notes": notes or {}
            }
            
            response = await self.client.post(
                f"{self.base_url}/orders",
                json=order_data
            )
            
            if response.status_code == 200:
                order_response = response.json()
                logger.info(f"Successfully created order: {order_response.get('id')}")
                return {
                    "status": "success",
                    "order_id": order_response.get("id"),
                    "amount": order_response.get("amount"),
                    "currency": order_response.get("currency"),
                    "receipt": order_response.get("receipt"),
                    "status_order": order_response.get("status"),
                    "created_at": order_response.get("created_at")
                }
            else:
                logger.error(f"Failed to create order: {response.status_code} - {response.text}")
                return {
                    "status": "error",
                    "message": f"Failed to create order: {response.status_code}",
                    "details": response.text
                }
                
        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            return {
                "status": "error",
                "message": f"Order creation error: {str(e)}"
            }
    
    def verify_payment_signature(self, params_dict: Dict[str, str]) -> Dict[str, Any]:
        """Verify payment signature"""
        try:
            order_id = params_dict.get("razorpay_order_id")
            payment_id = params_dict.get("razorpay_payment_id")
            signature = params_dict.get("razorpay_signature")
            
            if not all([order_id, payment_id, signature]):
                return {
                    "status": "error",
                    "message": "Missing required parameters for signature verification"
                }
            
            # Create the message to verify
            message = f"{order_id}|{payment_id}"
            
            # Generate expected signature
            expected_signature = hmac.new(
                self.api_secret.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            # Verify signature
            is_valid = hmac.compare_digest(expected_signature, signature)
            
            if is_valid:
                logger.info(f"Payment signature verified for payment: {payment_id}")
                return {
                    "status": "success",
                    "message": "Payment signature verified successfully",
                    "payment_id": payment_id,
                    "order_id": order_id
                }
            else:
                logger.warning(f"Invalid payment signature for payment: {payment_id}")
                return {
                    "status": "error",
                    "message": "Invalid payment signature"
                }
                
        except Exception as e:
            logger.error(f"Error verifying payment signature: {str(e)}")
            return {
                "status": "error",
                "message": f"Signature verification error: {str(e)}"
            }
    
    async def fetch_payment(self, payment_id: str) -> Dict[str, Any]:
        """Fetch payment details by payment ID"""
        try:
            response = await self.client.get(f"{self.base_url}/payments/{payment_id}")
            
            if response.status_code == 200:
                payment_data = response.json()
                logger.info(f"Successfully fetched payment: {payment_id}")
                return {
                    "status": "success",
                    "payment": payment_data
                }
            else:
                logger.error(f"Failed to fetch payment: {response.status_code} - {response.text}")
                return {
                    "status": "error",
                    "message": f"Failed to fetch payment: {response.status_code}",
                    "details": response.text
                }
                
        except Exception as e:
            logger.error(f"Error fetching payment: {str(e)}")
            return {
                "status": "error",
                "message": f"Payment fetch error: {str(e)}"
            }
    
    async def create_payment_link(self, amount: float, currency: str = "INR", 
                                 description: str = "", reference_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a payment link"""
        try:
            # Convert amount to paise
            amount_in_paise = int(amount * 100) if currency == "INR" else int(amount)
            
            link_data = {
                "amount": amount_in_paise,
                "currency": currency,
                "description": description or f"Payment for {amount} {currency}",
                "reference_id": reference_id or f"ref_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "callback_url": os.getenv("RAZORPAY_CALLBACK_URL", "https://example.com/callback"),
                "callback_method": "get"
            }
            
            response = await self.client.post(
                f"{self.base_url}/payment_links",
                json=link_data
            )
            
            if response.status_code == 200:
                link_response = response.json()
                logger.info(f"Successfully created payment link: {link_response.get('id')}")
                return {
                    "status": "success",
                    "payment_link_id": link_response.get("id"),
                    "short_url": link_response.get("short_url"),
                    "amount": link_response.get("amount"),
                    "currency": link_response.get("currency"),
                    "description": link_response.get("description"),
                    "status": link_response.get("status"),
                    "created_at": link_response.get("created_at")
                }
            else:
                logger.error(f"Failed to create payment link: {response.status_code} - {response.text}")
                return {
                    "status": "error",
                    "message": f"Failed to create payment link: {response.status_code}",
                    "details": response.text
                }
                
        except Exception as e:
            logger.error(f"Error creating payment link: {str(e)}")
            return {
                "status": "error",
                "message": f"Payment link creation error: {str(e)}"
            }
    
    async def refund_payment(self, payment_id: str, amount: Optional[float] = None, 
                           notes: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Process a payment refund"""
        try:
            refund_data = {
                "notes": notes or {}
            }
            
            # If amount is specified, convert to paise
            if amount is not None:
                refund_data["amount"] = int(amount * 100)  # Assuming INR
            
            response = await self.client.post(
                f"{self.base_url}/payments/{payment_id}/refund",
                json=refund_data
            )
            
            if response.status_code == 200:
                refund_response = response.json()
                logger.info(f"Successfully processed refund: {refund_response.get('id')}")
                return {
                    "status": "success",
                    "refund_id": refund_response.get("id"),
                    "payment_id": refund_response.get("payment_id"),
                    "amount": refund_response.get("amount"),
                    "currency": refund_response.get("currency"),
                    "status": refund_response.get("status"),
                    "created_at": refund_response.get("created_at")
                }
            else:
                logger.error(f"Failed to process refund: {response.status_code} - {response.text}")
                return {
                    "status": "error",
                    "message": f"Failed to process refund: {response.status_code}",
                    "details": response.text
                }
                
        except Exception as e:
            logger.error(f"Error processing refund: {str(e)}")
            return {
                "status": "error",
                "message": f"Refund processing error: {str(e)}"
            }
    
    async def get_payment_methods(self) -> Dict[str, Any]:
        """Get available payment methods"""
        try:
            # Mock payment methods response
            payment_methods = {
                "status": "success",
                "methods": [
                    {
                        "id": "card",
                        "name": "Credit/Debit Card",
                        "description": "Visa, MasterCard, RuPay",
                        "enabled": True
                    },
                    {
                        "id": "netbanking",
                        "name": "Net Banking",
                        "description": "All major banks",
                        "enabled": True
                    },
                    {
                        "id": "wallet",
                        "name": "Digital Wallets",
                        "description": "Paytm, PhonePe, Google Pay",
                        "enabled": True
                    },
                    {
                        "id": "upi",
                        "name": "UPI",
                        "description": "Unified Payments Interface",
                        "enabled": True
                    },
                    {
                        "id": "emi",
                        "name": "EMI",
                        "description": "Easy Monthly Installments",
                        "enabled": True
                    }
                ]
            }
            
            logger.info("Retrieved payment methods")
            return payment_methods
            
        except Exception as e:
            logger.error(f"Error getting payment methods: {str(e)}")
            return {
                "status": "error",
                "message": f"Payment methods error: {str(e)}"
            }
    
    async def get_order_details(self, order_id: str) -> Dict[str, Any]:
        """Get order details by order ID"""
        try:
            response = await self.client.get(f"{self.base_url}/orders/{order_id}")
            
            if response.status_code == 200:
                order_data = response.json()
                logger.info(f"Successfully fetched order: {order_id}")
                return {
                    "status": "success",
                    "order": order_data
                }
            else:
                logger.error(f"Failed to fetch order: {response.status_code} - {response.text}")
                return {
                    "status": "error",
                    "message": f"Failed to fetch order: {response.status_code}",
                    "details": response.text
                }
                
        except Exception as e:
            logger.error(f"Error fetching order: {str(e)}")
            return {
                "status": "error",
                "message": f"Order fetch error: {str(e)}"
            }
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
