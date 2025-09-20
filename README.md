# Multi-Agent AI System 🚀

A comprehensive FastAPI-based multi-agent AI system designed to handle complex tasks across different life domains. The system features specialized agents for food assistance, travel planning, shopping optimization, and payment processing, all coordinated by a central MasterAgent.

## 🌟 Features

### 🍽️ FoodAgent
- **Meal Planning**: Create personalized meal plans based on dietary preferences and calorie goals
- **Recipe Generation**: Discover and generate recipes using available ingredients
- **Grocery List Creation**: Automatically generate shopping lists from meal plans
- **Dietary Analysis**: Analyze nutritional content and provide health recommendations

### ✈️ TravelAgent
- **Trip Planning**: Plan complete trips with budget breakdowns and recommendations
- **Flight Search**: Find and compare flights across multiple airlines
- **Hotel Search**: Discover accommodations with detailed amenities and pricing
- **Itinerary Generation**: Create detailed day-by-day travel itineraries
- **Booking Assistance**: Help with booking confirmations and next steps

### 🛒 ShoppingAgent & QuickCommerceAgent
- **Product Discovery**: Find products based on search criteria and preferences
- **Price Comparison**: Compare prices across multiple vendors
- **Order Optimization**: Optimize orders for best value and delivery
- **Deal Finding**: Discover current deals and discounts
- **Shopping Lists**: Create organized shopping lists with budget tracking
- **Quick Commerce Integration**: Compare prices across Zepto, Blinkit, Swiggy Instamart, BigBasket
- **Automated Ordering**: Place orders automatically via headless browser automation
- **Real-time Tracking**: Track order status and delivery progress

### 💳 PaymentAgent
- **Order Creation**: Create payment orders using Razorpay
- **Payment Verification**: Verify payment signatures for security
- **Payment Links**: Generate shareable payment links
- **Refund Processing**: Handle payment refunds
- **Transaction History**: Track payment history and methods

### 🎤 Speech-to-Text
- **Audio Transcription**: Convert speech to text using Groq's Whisper API
- **Multi-language Support**: Support for 99+ languages
- **Timestamp Support**: Get word-level timestamps for audio
- **Format Validation**: Validate audio file formats

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │   MasterAgent   │    │   Domain Agents │
│                 │    │                 │    │                 │
│  /assistant     │───▶│  Intent Analysis│───▶│  FoodAgent      │
│  /speech-to-text│    │  Task Routing   │    │  TravelAgent    │
│  /payment/*     │    │  Response Synth │    │  ShoppingAgent  │
│  /quick-order   │    │                 │    │  QuickCommerce  │
│  /status        │    │                 │    │  PaymentAgent   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   MCP Clients   │
                       │                 │
                       │  FoodAPIClient  │
                       │  GroqWhisper    │
                       │  RazorpayAPI    │
                       │  QuickCommerce  │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+ (for frontend)
- uv (recommended) or pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Order_Agent
   ```

2. **Install dependencies**
   ```bash
   uv sync
   # or with pip
   pip install -e .
   ```

3. **Set up environment variables**
   ```bash
   # API Keys for external services
   export SPOONACULAR_API_KEY="your_spoonacular_key"
   export GROQ_API_KEY="your_groq_key"
   export RAZORPAY_API_KEY="your_razorpay_key"
   export RAZORPAY_API_SECRET="your_razorpay_secret"
   export RAZORPAY_CALLBACK_URL="https://your-domain.com/callback"
   
   # Optional: Redis configuration
   export REDIS_URL="redis://localhost:6379"
   
   # Logging
   export LOG_LEVEL="INFO"
   ```

4. **Run the application**

   **Option 1: Automated startup (Recommended)**
   ```bash
   ./start_dev.sh
   ```

   **Option 2: Manual startup**
   ```bash
   # Backend
   python main.py
   
   # Frontend (in another terminal)
   cd quickpick_frontend
   npm install
   npm run dev
   ```

5. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health
   - System Status: http://localhost:8000/status

## 📡 API Endpoints

### Main Assistant Endpoint
```http
POST /assistant
Content-Type: application/json

{
  "message": "Plan a healthy dinner for tonight",
  "user_id": "user123",
  "context": {}
}
```

### Speech-to-Text Endpoint
```http
POST /speech-to-text
Content-Type: multipart/form-data

file: [audio file]
language: en
```

### Payment Endpoints
```http
POST /payment/create-order
POST /payment/verify
POST /payment/create-link
GET /payment/methods
```

### Quick Commerce Endpoints
```http
POST /quick-order
POST /quick-order/approve
GET /quick-order/status/{order_id}
POST /test/quick-commerce
```

### Example Requests

#### Food Requests
```json
{
  "message": "Plan a 500-calorie dinner using chicken and vegetables"
}
```

```json
{
  "message": "Find recipes for vegetarian pasta dishes"
}
```

```json
{
  "message": "Create a grocery list for a week of healthy meals"
}
```

#### Travel Requests
```json
{
  "message": "Find flights from New York to Los Angeles for next week"
}
```

```json
{
  "message": "Plan a 5-day trip to Paris with $2000 budget"
}
```

```json
{
  "message": "Find hotels in downtown Tokyo for 3 people"
}
```

#### Shopping Requests
```json
{
  "message": "Compare prices for wireless headphones under $100"
}
```

```json
{
  "message": "Find deals on running shoes this week"
}
```

#### Payment Requests
```json
{
  "message": "Create a payment order for 500 rupees"
}
```

```json
{
  "message": "Verify payment with ID pay_1234567890"
}
```

#### Quick Commerce Requests
```json
{
  "message": "Order tomatoes and milk"
}
```

```json
{
  "message": "Find cheapest rice delivery"
}
```

```json
{
  "message": "Compare prices for groceries across platforms"
}
```

## 🔧 Configuration

### Environment Variables
```bash
# API Keys for external services
SPOONACULAR_API_KEY=your_spoonacular_key
GROQ_API_KEY=your_groq_key
RAZORPAY_API_KEY=your_razorpay_key
RAZORPAY_API_SECRET=your_razorpay_secret
RAZORPAY_CALLBACK_URL=https://your-domain.com/callback

# Redis configuration (for future use)
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO
```

### Agent Configuration
Each agent can be configured with user preferences:

```python
# Food preferences
food_agent.update_dietary_preferences(
    restrictions=["vegetarian"],
    allergies=["nuts"],
    cuisine_preferences=["Italian", "Mediterranean"]
)

# Travel preferences
travel_agent.update_travel_preferences(
    preferred_airlines=["Delta", "American"],
    preferred_hotels=["Marriott", "Hilton"],
    budget_preferences={"flights": 500, "hotels": 200},
    travel_style="luxury"
)

# Shopping preferences
shopping_agent.update_shopping_preferences(
    preferred_vendors=["Amazon", "Walmart"],
    budget_constraints={"electronics": 1000, "clothing": 200},
    product_preferences={"brands": ["Apple", "Nike"]}
)

# Payment preferences
payment_agent.update_payment_preferences(
    preferred_currencies=["INR", "USD"],
    payment_methods=["card", "upi", "netbanking"]
)
```

## 📁 Project Structure

```
Order_Agent/
├── agents/                    # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py          # Base agent class with common functionality
│   ├── food_agent.py          # Food domain agent
│   ├── travel_agent.py        # Travel domain agent
│   ├── shopping_agent.py      # Shopping domain agent (includes QuickCommerceAgent)
│   └── payment_agent.py       # Payment processing agent
├── master/                    # Master agent coordination
│   ├── __init__.py
│   └── master_agent.py        # Central coordinator and router
├── mcp/                       # Model Context Protocol clients
│   ├── __init__.py
│   ├── food_api_client.py     # Food API integrations (Spoonacular)
│   ├── speech_to_text_client.py # Groq Whisper API client
│   ├── razorpay_api_client.py # Razorpay payment gateway client
│   └── quick_commerce_scrapper.py # Quick commerce web scraping
├── config/                    # Configuration management
│   ├── __init__.py
│   └── settings.py            # Application settings and configuration
├── utils/                     # Utility functions
│   ├── __init__.py
│   ├── logger.py              # Logging utilities
│   └── helpers.py             # Helper functions
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── conftest.py            # Pytest configuration and fixtures
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   ├── e2e/                   # End-to-end tests
│   ├── fixtures/              # Test data and fixtures
│   └── mocks/                 # Mock objects
├── quickpick_frontend/        # React frontend application
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── hooks/             # Custom React hooks
│   │   ├── lib/               # Utility libraries
│   │   ├── config/            # Frontend configuration
│   │   └── pages/             # Page components
│   ├── package.json
│   └── README.md
├── main.py                    # FastAPI application entry point
├── pyproject.toml            # Project dependencies and configuration
├── pytest.ini               # Pytest configuration
├── run_tests.py              # Test runner script
├── start_dev.sh              # Development startup script
├── .gitignore                # Git ignore rules
├── TESTING.md                # Testing documentation
├── INTEGRATION_GUIDE.md      # Frontend-backend integration guide
├── catalog.json              # Product catalog data
├── restaurant.json           # Restaurant data sample
├── sample.json               # Sample API request data
├── full_response.json        # Sample response data
├── sample_result.json        # Sample result data
├── text_to_speech.py         # Text-to-speech functionality
├── foodagent.py              # Standalone food agent (legacy)
├── menu-brows.py             # Menu browsing functionality
├── res-api-test.py           # Restaurant API testing
├── resapi2.py                # Restaurant API implementation
└── README.md                 # This file
```

## 🔄 Message Flow

1. **User Request**: User sends natural language request to `/assistant`
2. **Intent Analysis**: MasterAgent analyzes intent and determines required agents
3. **Task Routing**: Request is routed to appropriate domain agents
4. **Agent Processing**: Domain agents process requests using their specialized logic
5. **Response Synthesis**: MasterAgent combines responses from multiple agents
6. **Unified Response**: Single, coherent response is returned to user

## 🧪 Testing

### Automated Testing

The project includes a comprehensive test suite with unit, integration, and end-to-end tests.

#### Quick Start
```bash
# Install test dependencies
python run_tests.py --install-deps

# Run all tests
python run_tests.py --all

# Run with coverage
python run_tests.py --all --coverage

# Run CI pipeline
python run_tests.py --ci
```

#### Test Types
```bash
# Unit tests
python run_tests.py --unit

# Integration tests
python run_tests.py --integration

# End-to-end tests
python run_tests.py --e2e

# Specific test file
python run_tests.py --test tests/unit/test_food_agent.py
```

#### Code Quality
```bash
# Run linting
python run_tests.py --lint

# Format code
python run_tests.py --format

# Type checking
python run_tests.py --types
```

For detailed testing information, see [TESTING.md](TESTING.md).

### Manual Testing
```bash
# Test food agent
curl -X POST "http://localhost:8000/test/food"

# Test travel agent
curl -X POST "http://localhost:8000/test/travel"

# Test shopping agent
curl -X POST "http://localhost:8000/test/shopping"

# Test payment agent
curl -X POST "http://localhost:8000/test/payment"

# Test quick commerce
curl -X POST "http://localhost:8000/test/quick-commerce"
```

### API Testing
```bash
# Test main assistant endpoint
curl -X POST "http://localhost:8000/assistant" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Plan a healthy dinner for tonight",
    "user_id": "test_user"
  }'

# Test speech-to-text
curl -X POST "http://localhost:8000/speech-to-text" \
  -F "file=@audio.wav" \
  -F "language=en"

# Test payment order creation
curl -X POST "http://localhost:8000/payment/create-order" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 500.0,
    "currency": "INR",
    "receipt": "test_receipt_001"
  }'

# Test quick commerce order
curl -X POST "http://localhost:8000/quick-order" \
  -H "Content-Type: application/json" \
  -d '{
    "items": ["tomatoes", "milk", "bread"],
    "delivery_preference": "fastest",
    "auto_approve": false
  }'

# Test quick commerce approval
curl -X POST "http://localhost:8000/quick-order/approve" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "order_123",
    "approved": true,
    "user_id": "user_123"
  }'

# Test order status
curl -X GET "http://localhost:8000/quick-order/status/order_123?user_id=user_123"
```

## 📚 Function Documentation

### MasterAgent Class

#### `process(request_data: Dict[str, Any]) -> Dict[str, Any]`
Main entry point for processing user requests. Analyzes intent, routes to appropriate agents, and synthesizes responses.

**Parameters:**
- `request_data`: Dictionary containing message, user_id, and context

**Returns:**
- Unified response with primary response, additional suggestions, and recommendations

#### `_analyze_intent(user_message: str) -> Dict[str, Any]`
Analyzes user intent using pattern matching to determine which agents should handle the request.

**Parameters:**
- `user_message`: The user's natural language input

**Returns:**
- Intent analysis with primary intent, involved agents, task type, and extracted data

#### `_route_to_agents(intent_analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]`
Routes the request to appropriate agents based on intent analysis.

**Parameters:**
- `intent_analysis`: Result from intent analysis
- `context`: Request context including user information

**Returns:**
- Dictionary of agent responses

#### `_synthesize_responses(agent_responses: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]`
Combines responses from multiple agents into a unified response.

**Parameters:**
- `agent_responses`: Responses from individual agents
- `context`: Request context

**Returns:**
- Unified response with primary response and additional suggestions

### FoodAgent Class

#### `process_request(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]`
Processes food-related requests including meal planning, recipe generation, and grocery lists.

**Supported Request Types:**
- `meal_planning`: Create meal plans based on calories and preferences
- `recipe_generation`: Generate recipes from ingredients
- `grocery_list`: Create shopping lists from meal plans
- `dietary_analysis`: Analyze nutritional content

#### `update_dietary_preferences(restrictions: List[str], allergies: List[str], cuisine_preferences: List[str])`
Updates dietary preferences and restrictions for personalized recommendations.

### TravelAgent Class

#### `process_request(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]`
Processes travel-related requests including trip planning, flight searches, and hotel bookings.

**Supported Request Types:**
- `trip_planning`: Plan complete trips with budget breakdowns
- `flight_search`: Search and compare flights
- `hotel_search`: Find accommodations with amenities
- `itinerary_generation`: Create detailed travel itineraries
- `booking_assistance`: Help with booking confirmations

#### `update_travel_preferences(preferred_airlines: List[str], preferred_hotels: List[str], budget_preferences: Dict[str, Any], travel_style: str)`
Updates travel preferences for personalized recommendations.

### ShoppingAgent Class

#### `process_request(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]`
Processes shopping-related requests including product discovery, price comparison, and deal finding.

**Supported Request Types:**
- `product_discovery`: Find products based on search criteria
- `price_comparison`: Compare prices across vendors
- `order_optimization`: Optimize orders for best value
- `deal_finding`: Discover current deals and discounts
- `shopping_list`: Create organized shopping lists

#### `update_shopping_preferences(preferred_vendors: List[str], budget_constraints: Dict[str, Any], product_preferences: Dict[str, Any])`
Updates shopping preferences for personalized recommendations.

### QuickCommerceAgent Class

#### `process_request(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]`
Processes quick commerce requests including price comparison, order placement, and tracking.

**Supported Request Types:**
- `quick_order`: Compare prices and place orders across quick commerce platforms
- `compare_prices_quick_commerce`: Compare prices without placing orders
- `place_order`: Place orders on specific platforms
- `order_status`: Check order status and tracking information

#### `_quick_order(items: List[str], preferences: Dict[str, Any]) -> Dict[str, Any]`
Handles quick order requests by comparing prices across platforms and placing orders.

**Parameters:**
- `items`: List of items to order
- `preferences`: User preferences for delivery and platform selection

**Returns:**
- Order response with recommendations and order details

#### `_compare_prices_across_platforms(items: List[str]) -> Dict[str, Any]`
Compares prices for items across all supported quick commerce platforms.

**Parameters:**
- `items`: List of items to compare

**Returns:**
- Price comparison data with best options for each platform

#### `_place_order_automation(platform: str, items: List[Dict], user_id: str) -> Dict[str, Any]`
Automates order placement using headless browser automation.

**Parameters:**
- `platform`: Target platform (zepto, blinkit, swiggy_instamart, bigbasket)
- `items`: List of items with quantities and details
- `user_id`: User identifier

**Returns:**
- Order placement result with order ID and tracking information

#### `update_quick_commerce_preferences(delivery_priority: str, max_delivery_time: int, preferred_platforms: List[str], auto_approve_threshold: float, quality_threshold: float)`
Updates quick commerce preferences for personalized recommendations.

**Parameters:**
- `delivery_priority`: Priority preference (fastest, cheapest, best_rated)
- `max_delivery_time`: Maximum acceptable delivery time in minutes
- `preferred_platforms`: List of preferred platforms
- `auto_approve_threshold`: Minimum savings threshold for auto-approval
- `quality_threshold`: Minimum quality rating threshold

### PaymentAgent Class

#### `process_request(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]`
Processes payment-related requests using Razorpay integration.

**Supported Request Types:**
- `create_order`: Create payment orders
- `verify_payment`: Verify payment signatures
- `create_payment_link`: Generate shareable payment links
- `refund_payment`: Process payment refunds
- `get_payment_methods`: Retrieve available payment methods
- `get_transaction_history`: Get payment history

#### `update_payment_preferences(preferred_currencies: List[str], payment_methods: List[str])`
Updates payment preferences for personalized recommendations.

### RazorpayAPIClient Class

#### `create_order(amount: float, currency: str = "INR", receipt: Optional[str] = None, notes: Optional[Dict[str, str]] = None) -> Dict[str, Any]`
Creates a new payment order using Razorpay API.

**Parameters:**
- `amount`: Payment amount
- `currency`: Currency code (default: INR)
- `receipt`: Receipt identifier
- `notes`: Additional notes

**Returns:**
- Order creation response with order ID and details

#### `verify_payment_signature(params_dict: Dict[str, str]) -> Dict[str, Any]`
Verifies payment signature for security.

**Parameters:**
- `params_dict`: Dictionary containing payment_id, order_id, and signature

**Returns:**
- Verification result with success/error status

#### `create_payment_link(amount: float, currency: str = "INR", description: str = "", reference_id: Optional[str] = None) -> Dict[str, Any]`
Creates a shareable payment link.

**Parameters:**
- `amount`: Payment amount
- `currency`: Currency code
- `description`: Payment description
- `reference_id`: Reference identifier

**Returns:**
- Payment link creation response with link URL

### GroqWhisperClient Class

#### `transcribe_audio(audio_file_path: str, language: str = "en") -> Dict[str, Any]`
Transcribes audio file using Groq's Whisper API.

**Parameters:**
- `audio_file_path`: Path to audio file
- `language`: Language code (default: en)

**Returns:**
- Transcription result with text, language, and duration

#### `transcribe_audio_bytes(audio_bytes: bytes, filename: str = "audio.wav", language: str = "en") -> Dict[str, Any]`
Transcribes audio from bytes data.

**Parameters:**
- `audio_bytes`: Audio data as bytes
- `filename`: Original filename
- `language`: Language code

**Returns:**
- Transcription result

#### `get_supported_languages() -> Dict[str, Any]`
Returns list of supported languages for transcription.

**Returns:**
- Dictionary with supported languages and their codes

### QuickCommerceScraper Class

#### `search_products(platform: str, query: str) -> List[Dict[str, Any]]`
Searches for products on a specific quick commerce platform.

**Parameters:**
- `platform`: Platform name (zepto, blinkit, swiggy_instamart, bigbasket)
- `query`: Search query for products

**Returns:**
- List of product dictionaries with name, price, rating, and availability

#### `place_order(platform: str, items: List[Dict], user_id: str) -> Dict[str, Any]`
Places an order on a specific platform using headless browser automation.

**Parameters:**
- `platform`: Target platform for order placement
- `items`: List of items with quantities and details
- `user_id`: User identifier for order tracking

**Returns:**
- Order placement result with order ID, status, and tracking information

#### `_scrape_with_selenium(platform: str, query: str) -> List[Dict[str, Any]]`
Private method to handle Selenium-based web scraping for product data.

**Parameters:**
- `platform`: Platform to scrape
- `query`: Search query

**Returns:**
- Scraped product data

### QuickCommerceOptimizer Class

#### `find_best_deals(items: List[str], preferences: Dict[str, Any]) -> Dict[str, Any]`
Finds the best deals across all platforms for given items.

**Parameters:**
- `items`: List of items to find deals for
- `preferences`: User preferences for optimization

**Returns:**
- Optimization result with best platform recommendations and savings

#### `_select_best_product(products: List[Dict], preferences: Dict) -> Dict`
Selects the best product from a list based on preferences.

**Parameters:**
- `products`: List of products to choose from
- `preferences`: User preferences for selection

**Returns:**
- Best product based on price, rating, and availability

#### `_optimize_order(all_results: Dict, preferences: Dict) -> Dict`
Optimizes the entire order across platforms.

**Parameters:**
- `all_results`: Results from all platforms
- `preferences`: User preferences

**Returns:**
- Optimized order recommendation with platform selection and savings

### FoodAPIClient Class

#### `search_recipes(query: str, max_results: int = 10, diet: Optional[str] = None, cuisine: Optional[str] = None) -> List[Dict[str, Any]]`
Searches for recipes based on query and filters.

**Parameters:**
- `query`: Search query
- `max_results`: Maximum number of results
- `diet`: Dietary restrictions
- `cuisine`: Cuisine type

**Returns:**
- List of recipe dictionaries

#### `get_recipe_by_id(recipe_id: int) -> Optional[Dict[str, Any]]`
Gets detailed recipe information by ID.

**Parameters:**
- `recipe_id`: Recipe identifier

**Returns:**
- Detailed recipe information or None if not found

#### `get_meal_plan(calories: int, diet: str = "balanced", time_frame: str = "day") -> Dict[str, Any]`
Generates a meal plan based on calories and diet preferences.

**Parameters:**
- `calories`: Target calorie count
- `diet`: Diet type
- `time_frame`: Planning timeframe

**Returns:**
- Meal plan with meals and shopping list

## 🚧 Future Enhancements

### Planned Features
- [ ] Redis integration for message queuing and caching
- [ ] Vector database for preference learning and recommendations
- [ ] Real API integrations (Spoonacular, Skyscanner, etc.)
- [ ] WebSocket support for real-time updates
- [ ] User authentication and session management
- [ ] Advanced conversation memory and context
- [ ] Multi-language support for all agents
- [ ] Mobile app integration
- [ ] Voice response capabilities
- [ ] Advanced analytics and reporting

### Agent Extensions
- [ ] FinanceAgent for budgeting and expense tracking
- [ ] HealthAgent for fitness and wellness
- [ ] EntertainmentAgent for movies, books, and events
- [ ] ProductivityAgent for task management and scheduling
- [ ] WeatherAgent for weather information and alerts
- [ ] NewsAgent for personalized news delivery

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the API documentation at `/docs`
- Review the test endpoints for examples
- Check the logs for debugging information


## 🔍 Troubleshooting

### Common Issues

1. **Missing API Keys**: Ensure all required environment variables are set
2. **Import Errors**: Check that all dependencies are installed correctly
3. **Payment Failures**: Verify Razorpay credentials and callback URLs
4. **Audio Transcription Issues**: Check audio file format and size limits
5. **Agent Routing Problems**: Review intent analysis patterns and agent configurations

### Debug Mode
Enable debug logging by setting `LOG_LEVEL=DEBUG` in your environment variables.

---

**Happy coding! 🎉**