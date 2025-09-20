from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentMessage
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class PaymentAgent(BaseAgent):
    """Agent specialized in payment processing and financial transactions"""
    
    def __init__(self):
        super().__init__("PaymentAgent")
        self.payment_methods = []
        self.transaction_history = []
        self.preferred_currencies = ["INR", "USD", "EUR"]
        
        # Import Razorpay client
        try:
            from mcp.razorpay_api_client import RazorpayAPIClient
            self.razorpay_client = RazorpayAPIClient()
            logger.info("PaymentAgent initialized with Razorpay client")
        except ImportError:
            self.razorpay_client = None
            logger.warning("Razorpay client not available")
    
    async def process_request(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Process payment-related requests"""
        request_type = data.get("type", "general")
        
        if request_type == "create_order":
            return await self._create_payment_order(data, context)
        elif request_type == "verify_payment":
            return await self._verify_payment(data, context)
        elif request_type == "create_payment_link":
            return await self._create_payment_link(data, context)
        elif request_type == "refund_payment":
            return await self._refund_payment(data, context)
        elif request_type == "get_payment_methods":
            return await self._get_payment_methods(data, context)
        elif request_type == "get_transaction_history":
            return await self._get_transaction_history(data, context)
        else:
            return await self._general_payment_assistance(data, context)
    
    async def _create_payment_order(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new payment order"""
        amount = data.get("amount", 0)
        currency = data.get("currency", "INR")
        receipt = data.get("receipt")
        notes = data.get("notes", {})
        
        if not self.razorpay_client:
            return {
                "status": "error",
                "message": "Razorpay client not available",
                "agent_id": self.agent_id
            }
        
        # Create order using Razorpay
        result = self.razorpay_client.create_order(
            amount=amount,
            currency=currency,
            receipt=receipt,
            notes=notes
        )
        
        if result["status"] == "success":
            # Add to transaction history
            transaction = {
                "order_id": result["order_id"],
                "amount": amount,
                "currency": currency,
                "status": "created",
                "timestamp": datetime.now().isoformat(),
                "type": "order_creation"
            }
            self.transaction_history.append(transaction)
            
            logger.info(f"PaymentAgent created order: {result['order_id']}")
            return {
                "status": "success",
                "data": result,
                "agent_id": self.agent_id
            }
        else:
            return {
                "status": "error",
                "message": result["message"],
                "agent_id": self.agent_id
            }
    
    async def _verify_payment(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Verify payment signature and status"""
        payment_id = data.get("payment_id")
        order_id = data.get("order_id")
        signature = data.get("signature")
        
        if not self.razorpay_client:
            return {
                "status": "error",
                "message": "Razorpay client not available",
                "agent_id": self.agent_id
            }
        
        # Verify payment signature
        params_dict = {
            "razorpay_payment_id": payment_id,
            "razorpay_order_id": order_id,
            "razorpay_signature": signature
        }
        
        verification_result = self.razorpay_client.verify_payment_signature(params_dict)
        
        if verification_result["status"] == "success":
            # Get payment details
            payment_details = self.razorpay_client.fetch_payment(payment_id)
            
            # Update transaction history
            for transaction in self.transaction_history:
                if transaction.get("order_id") == order_id:
                    transaction["payment_id"] = payment_id
                    transaction["status"] = "verified"
                    transaction["verified_at"] = datetime.now().isoformat()
                    break
            
            logger.info(f"PaymentAgent verified payment: {payment_id}")
            return {
                "status": "success",
                "data": {
                    "verification": verification_result,
                    "payment_details": payment_details.get("payment", {}) if payment_details["status"] == "success" else {}
                },
                "agent_id": self.agent_id
            }
        else:
            return {
                "status": "error",
                "message": verification_result["message"],
                "agent_id": self.agent_id
            }
    
    async def _create_payment_link(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a payment link for easy sharing"""
        amount = data.get("amount", 0)
        currency = data.get("currency", "INR")
        description = data.get("description", "")
        reference_id = data.get("reference_id")
        
        if not self.razorpay_client:
            return {
                "status": "error",
                "message": "Razorpay client not available",
                "agent_id": self.agent_id
            }
        
        result = self.razorpay_client.create_payment_link(
            amount=amount,
            currency=currency,
            description=description,
            reference_id=reference_id
        )
        
        if result["status"] == "success":
            # Add to transaction history
            transaction = {
                "payment_link_id": result["payment_link_id"],
                "amount": amount,
                "currency": currency,
                "description": description,
                "status": "link_created",
                "timestamp": datetime.now().isoformat(),
                "type": "payment_link"
            }
            self.transaction_history.append(transaction)
            
            logger.info(f"PaymentAgent created payment link: {result['payment_link_id']}")
            return {
                "status": "success",
                "data": result,
                "agent_id": self.agent_id
            }
        else:
            return {
                "status": "error",
                "message": result["message"],
                "agent_id": self.agent_id
            }
    
    async def _refund_payment(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Process payment refund"""
        payment_id = data.get("payment_id")
        amount = data.get("amount")  # Optional, if not provided, full refund
        notes = data.get("notes", {})
        
        if not self.razorpay_client:
            return {
                "status": "error",
                "message": "Razorpay client not available",
                "agent_id": self.agent_id
            }
        
        result = self.razorpay_client.refund_payment(
            payment_id=payment_id,
            amount=amount,
            notes=notes
        )
        
        if result["status"] == "success":
            # Add to transaction history
            transaction = {
                "refund_id": result["refund_id"],
                "payment_id": payment_id,
                "amount": amount,
                "status": "refunded",
                "timestamp": datetime.now().isoformat(),
                "type": "refund"
            }
            self.transaction_history.append(transaction)
            
            logger.info(f"PaymentAgent processed refund: {result['refund_id']}")
            return {
                "status": "success",
                "data": result,
                "agent_id": self.agent_id
            }
        else:
            return {
                "status": "error",
                "message": result["message"],
                "agent_id": self.agent_id
            }
    
    async def _get_payment_methods(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Get available payment methods"""
        if not self.razorpay_client:
            return {
                "status": "error",
                "message": "Razorpay client not available",
                "agent_id": self.agent_id
            }
        
        result = self.razorpay_client.get_payment_methods()
        
        logger.info("PaymentAgent retrieved payment methods")
        return {
            "status": "success",
            "data": result,
            "agent_id": self.agent_id
        }
    
    async def _get_transaction_history(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Get transaction history for user"""
        user_id = context.get("user_id", "default_user")
        limit = data.get("limit", 50)
        
        # Filter transactions by user (in a real system, you'd have user-specific transactions)
        user_transactions = self.transaction_history[-limit:] if self.transaction_history else []
        
        logger.info(f"PaymentAgent retrieved {len(user_transactions)} transactions for user {user_id}")
        return {
            "status": "success",
            "data": {
                "transactions": user_transactions,
                "total_count": len(user_transactions),
                "user_id": user_id
            },
            "agent_id": self.agent_id
        }
    
    async def _general_payment_assistance(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Provide general payment assistance"""
        query = data.get("query", "")
        
        response = {
            "suggestion": f"Based on your payment query '{query}', I can help with order creation, payment verification, refunds, and payment links.",
            "available_actions": [
                "create_order",
                "verify_payment",
                "create_payment_link",
                "refund_payment",
                "get_payment_methods",
                "get_transaction_history"
            ]
        }
        
        logger.info(f"PaymentAgent provided general assistance for: {query}")
        return {
            "status": "success",
            "data": response,
            "agent_id": self.agent_id
        }
    
    def update_payment_preferences(self, preferred_currencies: List[str], 
                                 payment_methods: List[str]):
        """Update payment preferences"""
        self.preferred_currencies = preferred_currencies
        self.payment_methods = payment_methods
        logger.info(f"Updated payment preferences: currencies={preferred_currencies}, methods={payment_methods}") 