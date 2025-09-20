# Multi-Agent AI System 🚀

A FastAPI-based multi-agent AI system designed to manage complex tasks across different life domains. The system features specialized agents for food, travel, and shopping assistance, all coordinated by a central MasterAgent.

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

### 🛒 ShoppingAgent
- **Product Discovery**: Find products based on search criteria and preferences
- **Price Comparison**: Compare prices across multiple vendors
- **Order Optimization**: Optimize orders for best value and delivery
- **Deal Finding**: Discover current deals and discounts
- **Shopping Lists**: Create organized shopping lists with budget tracking

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │   MasterAgent   │    │   Domain Agents │
│                 │    │                 │    │                 │
│  /assistant     │───▶│  Intent Analysis│───▶│  FoodAgent      │
│  /status        │    │  Task Routing   │    │  TravelAgent    │
│  /health        │    │  Response Synth │    │  ShoppingAgent  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   MCP Clients   │
                       │                 │
                       │  Food APIs      │
                       │  Travel APIs    │
                       │  Shopping APIs  │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- uv (recommended) or pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd multi-agent-ai-system
   ```

2. **Install dependencies**
   ```bash
   uv sync
   # or with pip
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional)
   ```bash
   export SPOONACULAR_API_KEY="your_api_key"
   export GEMINI_API_KEY="your_gemini_key"
   export SERPAPI_API_KEY="your_serpapi_key"
   ```

4. **Run the application**
   ```bash
   python main.py
   # or
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Access the API**
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

```json
{
  "message": "Create a shopping list for home office supplies"
}
```

### Test Endpoints
- `POST /test/food` - Test FoodAgent functionality
- `POST /test/travel` - Test TravelAgent functionality  
- `POST /test/shopping` - Test ShoppingAgent functionality

## 🔧 Configuration

### Environment Variables
```bash
# API Keys for external services
SPOONACULAR_API_KEY=your_spoonacular_key
GEMINI_API_KEY=your_gemini_key
SERPAPI_API_KEY=your_serpapi_key

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
```

## 🧪 Testing

### Manual Testing
```bash
# Test food agent
curl -X POST "http://localhost:8000/test/food"

# Test travel agent
curl -X POST "http://localhost:8000/test/travel"

# Test shopping agent
curl -X POST "http://localhost:8000/test/shopping"
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
```

## 📁 Project Structure

```
multi-agent-ai-system/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py          # Base agent class
│   ├── food_agent.py          # Food domain agent
│   ├── travel_agent.py        # Travel domain agent
│   └── shopping_agent.py      # Shopping domain agent
├── master/
│   ├── __init__.py
│   └── master_agent.py        # Central coordinator
├── mcp/
│   ├── __init__.py
│   ├── food_api_client.py     # Food API integrations
│   ├── travel_api_client.py   # Travel API integrations
│   └── shopping_api_client.py # Shopping API integrations
├── main.py                    # FastAPI application
├── pyproject.toml            # Project dependencies
├── README.md                 # This file
└── requirements.txt          # Python dependencies
```

## 🔄 Message Flow

1. **User Request**: User sends natural language request to `/assistant`
2. **Intent Analysis**: MasterAgent analyzes intent and determines required agents
3. **Task Routing**: Request is routed to appropriate domain agents
4. **Agent Processing**: Domain agents process requests using their specialized logic
5. **Response Synthesis**: MasterAgent combines responses from multiple agents
6. **Unified Response**: Single, coherent response is returned to user

## 🚧 Future Enhancements

### Planned Features
- [ ] Redis integration for message queuing
- [ ] Vector database for preference learning
- [ ] Real API integrations (Spoonacular, Skyscanner, etc.)
- [ ] WebSocket support for real-time updates
- [ ] User authentication and session management
- [ ] Advanced conversation memory
- [ ] Multi-language support
- [ ] Mobile app integration

### Agent Extensions
- [ ] FinanceAgent for budgeting and expense tracking
- [ ] HealthAgent for fitness and wellness
- [ ] EntertainmentAgent for movies, books, and events
- [ ] ProductivityAgent for task management and scheduling

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

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Pydantic for data validation
- LangChain for LLM integration
- The open-source community for inspiration and tools

---

**Happy coding! 🎉**

