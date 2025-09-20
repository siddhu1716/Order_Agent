from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
import json
from datetime import datetime

# Import our agents
from master.master_agent import MasterAgent

# Import MCP clients
from mcp.speech_to_text_client import GroqWhisperClient
from mcp.razorpay_api_client import RazorpayAPIClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Agent AI System",
    description="A FastAPI-based multi-agent system for food, travel, shopping, and payment assistance",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MasterAgent
master_agent = MasterAgent()

# Initialize MCP clients
speech_client = GroqWhisperClient()
razorpay_client = RazorpayAPIClient()

# Pydantic models for request/response
class AssistantRequest(BaseModel):
    message: str
    user_id: Optional[str] = "default_user"
    context: Optional[Dict[str, Any]] = {}

class AssistantResponse(BaseModel):
    status: str
    message: str
    primary_response: Optional[Dict[str, Any]] = None
    agent_used: Optional[str] = None
    timestamp: str
    context: Optional[Dict[str, Any]] = None
    additional_suggestions: Optional[Dict[str, Any]] = None
    recommendations: Optional[list] = None

class AgentStatusResponse(BaseModel):
    status: str
    agents: Dict[str, Any]
    timestamp: str

class PaymentOrderRequest(BaseModel):
    amount: float
    currency: str = "INR"
    receipt: Optional[str] = None
    notes: Optional[Dict[str, str]] = None

class PaymentVerificationRequest(BaseModel):
    payment_id: str
    order_id: str
    signature: str

class PaymentLinkRequest(BaseModel):
    amount: float
    currency: str = "INR"
    description: str = ""
    reference_id: Optional[str] = None

@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "message": "Multi-Agent AI System API",
        "version": "1.0.0",
        "description": "AI-powered assistance for food, travel, shopping, and payments",
        "endpoints": {
            "/assistant": "POST - Main assistant endpoint",
            "/speech-to-text": "POST - Speech to text conversion",
            "/payment/create-order": "POST - Create payment order",
            "/payment/verify": "POST - Verify payment",
            "/payment/create-link": "POST - Create payment link",
            "/status": "GET - System status",
            "/health": "GET - Health check"
        }
    }

@app.post("/assistant", response_model=AssistantResponse)
async def handle_assistant_request(request: AssistantRequest):
    """
    Main assistant endpoint that processes user requests and routes them to appropriate agents.
    
    Example requests:
    - "Plan a healthy dinner for tonight"
    - "Find flights from NYC to LAX for next week"
    - "Compare prices for wireless headphones"
    - "Create a payment order for 500 rupees"
    """
    try:
        logger.info(f"Received request from user {request.user_id}: {request.message}")
        
        # Process request through MasterAgent
        response = await master_agent.process({
            "message": request.message,
            "user_id": request.user_id,
            "context": request.context
        })
        
        logger.info(f"Successfully processed request for user {request.user_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing assistant request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/speech-to-text")
async def speech_to_text(
    file: UploadFile = File(...),
    language: str = Form("en")
):
    """
    Convert speech to text using Groq's Whisper API
    
    Upload an audio file (WAV, MP3, etc.) and get the transcribed text.
    """
    try:
        # Validate file type
        if not file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Read file content
        audio_content = await file.read()
        
        # Transcribe using Groq Whisper
        result = await speech_client.transcribe_audio_bytes(
            audio_bytes=audio_content,
            filename=file.filename,
            language=language
        )
        
        if result["status"] == "success":
            return {
                "status": "success",
                "text": result["text"],
                "language": result["language"],
                "duration": result.get("duration", 0),
                "filename": file.filename,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail=result["message"])
            
    except Exception as e:
        logger.error(f"Error in speech-to-text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Speech-to-text error: {str(e)}")

@app.post("/payment/create-order")
async def create_payment_order(request: PaymentOrderRequest):
    """
    Create a new payment order using Razorpay
    
    This endpoint creates a payment order that can be used to initiate a payment.
    """
    try:
        result = razorpay_client.create_order(
            amount=request.amount,
            currency=request.currency,
            receipt=request.receipt,
            notes=request.notes
        )
        
        if result["status"] == "success":
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])
            
    except Exception as e:
        logger.error(f"Error creating payment order: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Payment order creation failed: {str(e)}")

@app.post("/payment/verify")
async def verify_payment(request: PaymentVerificationRequest):
    """
    Verify a payment signature using Razorpay
    
    This endpoint verifies that a payment was legitimate and not tampered with.
    """
    try:
        params_dict = {
            "razorpay_payment_id": request.payment_id,
            "razorpay_order_id": request.order_id,
            "razorpay_signature": request.signature
        }
        
        verification_result = razorpay_client.verify_payment_signature(params_dict)
        
        if verification_result["status"] == "success":
            # Get payment details
            payment_details = razorpay_client.fetch_payment(request.payment_id)
            
            return {
                "status": "success",
                "verification": verification_result,
                "payment_details": payment_details.get("payment", {}) if payment_details["status"] == "success" else {},
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=400, detail=verification_result["message"])
            
    except Exception as e:
        logger.error(f"Error verifying payment: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Payment verification failed: {str(e)}")

@app.post("/payment/create-link")
async def create_payment_link(request: PaymentLinkRequest):
    """
    Create a payment link using Razorpay
    
    This endpoint creates a shareable payment link for easy payments.
    """
    try:
        result = razorpay_client.create_payment_link(
            amount=request.amount,
            currency=request.currency,
            description=request.description,
            reference_id=request.reference_id
        )
        
        if result["status"] == "success":
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])
            
    except Exception as e:
        logger.error(f"Error creating payment link: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Payment link creation failed: {str(e)}")

@app.get("/payment/methods")
async def get_payment_methods():
    """
    Get available payment methods
    
    Returns a list of supported payment methods.
    """
    try:
        result = razorpay_client.get_payment_methods()
        
        if result["status"] == "success":
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])
            
    except Exception as e:
        logger.error(f"Error getting payment methods: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get payment methods: {str(e)}")

@app.get("/speech/languages")
async def get_supported_languages():
    """
    Get supported languages for speech-to-text
    
    Returns a list of languages supported by the Whisper model.
    """
    try:
        result = await speech_client.get_supported_languages()
        
        if result["status"] == "success":
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])
            
    except Exception as e:
        logger.error(f"Error getting supported languages: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get supported languages: {str(e)}")

@app.get("/status", response_model=AgentStatusResponse)
async def get_system_status():
    """Get the status of all agents in the system"""
    try:
        agent_status = master_agent.get_agent_status()
        
        return {
            "status": "healthy",
            "agents": agent_status,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting system status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving system status: {str(e)}")

@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Multi-Agent AI System",
        "features": ["food", "travel", "shopping", "payment", "speech-to-text"]
    }

@app.post("/test/food")
async def test_food_agent():
    """Test endpoint for FoodAgent functionality"""
    try:
        test_request = {
            "message": "Plan a 500-calorie dinner using chicken and vegetables",
            "user_id": "test_user"
        }
        
        response = await master_agent.process(test_request)
        return {
            "test_type": "food_agent",
            "request": test_request,
            "response": response
        }
        
    except Exception as e:
        logger.error(f"Error in food agent test: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")

@app.post("/test/travel")
async def test_travel_agent():
    """Test endpoint for TravelAgent functionality"""
    try:
        test_request = {
            "message": "Find flights from New York to Los Angeles for next week",
            "user_id": "test_user"
        }
        
        response = await master_agent.process(test_request)
        return {
            "test_type": "travel_agent",
            "request": test_request,
            "response": response
        }
        
    except Exception as e:
        logger.error(f"Error in travel agent test: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")

@app.post("/test/shopping")
async def test_shopping_agent():
    """Test endpoint for ShoppingAgent functionality"""
    try:
        test_request = {
            "message": "Compare prices for wireless headphones under $100",
            "user_id": "test_user"
        }
        
        response = await master_agent.process(test_request)
        return {
            "test_type": "shopping_agent",
            "request": test_request,
            "response": response
        }
        
    except Exception as e:
        logger.error(f"Error in shopping agent test: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")

@app.post("/test/payment")
async def test_payment_agent():
    """Test endpoint for PaymentAgent functionality"""
    try:
        test_request = {
            "message": "Create a payment order for 500 rupees",
            "user_id": "test_user"
        }
        
        response = await master_agent.process(test_request)
        return {
            "test_type": "payment_agent",
            "request": test_request,
            "response": response
        }
        
    except Exception as e:
        logger.error(f"Error in payment agent test: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 