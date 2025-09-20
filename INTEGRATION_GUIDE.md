# 🔗 Frontend-Backend Integration Guide

This guide explains how the QuickPick frontend and backend are integrated and how to run the complete system.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    QuickPick System                        │
├─────────────────────────────────────────────────────────────┤
│  Frontend (React + TypeScript)                             │
│  ├── VoiceOrderComponent     →  /assistant                 │
│  ├── PriceComparisonComponent → /quick-order               │
│  ├── OrderTrackingComponent  → /quick-order/status/{id}    │
│  └── API Client (api.ts)     → All Backend Endpoints       │
├─────────────────────────────────────────────────────────────┤
│  Backend (FastAPI + Python)                                │
│  ├── MasterAgent            → Coordinates all agents       │
│  ├── QuickCommerceAgent     → Handles quick commerce       │
│  ├── QuickCommerceScraper   → Web scraping & automation    │
│  ├── FoodAgent              → Food recommendations         │
│  ├── TravelAgent            → Travel bookings              │
│  ├── ShoppingAgent          → General shopping             │
│  └── PaymentAgent           → Payment processing           │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Option 1: Automated Startup (Recommended)
```bash
# Make script executable and run
chmod +x start_dev.sh
./start_dev.sh
```

This script will:
- ✅ Check prerequisites (Python, Node.js/Bun)
- ✅ Create/activate virtual environment
- ✅ Install dependencies
- ✅ Start backend API on port 8000
- ✅ Start frontend dev server on port 5173
- ✅ Display status and logs

### Option 2: Manual Startup

#### Backend Setup
```bash
# 1. Activate virtual environment
source myenv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start backend
python main.py
```

#### Frontend Setup
```bash
# 1. Navigate to frontend directory
cd quickpick_frontend

# 2. Install dependencies
npm install  # or bun install

# 3. Start frontend
npm run dev  # or bun dev
```

## 🔌 API Integration Details

### 1. Voice Order Integration

**Frontend Flow:**
```typescript
// VoiceOrderComponent.tsx
const voiceCommandMutation = useVoiceCommand();

// When user speaks
voiceCommandMutation.mutate(
  { message: "Order tomatoes and milk" },
  {
    onSuccess: (data) => {
      // Show price comparison
      onOrderPlaced?.(data.data.recommendation.summary);
    }
  }
);
```

**Backend Processing:**
```python
# main.py - /assistant endpoint
@app.post("/assistant")
async def assistant(request: AssistantRequest):
    response = await master_agent.process_request(
        message=request.message,
        user_id=request.user_id,
        context=request.context
    )
    return response
```

### 2. Price Comparison Integration

**Frontend Flow:**
```typescript
// PriceComparisonComponent.tsx
const placeOrderMutation = usePlaceQuickOrder();

// Fetch price comparison
const response = await placeOrderMutation.mutateAsync({
  items: ['tomatoes', 'milk', 'bread'],
  delivery_preference: 'fastest',
  auto_approve: false
});

// Transform backend data to frontend format
const platforms = transformPlatformData(response);
```

**Backend Processing:**
```python
# main.py - /quick-order endpoint
@app.post("/quick-order")
async def quick_order(request: QuickOrderRequest):
    response = await master_agent.process_request(
        message=f"quick_order: {', '.join(request.items)}",
        user_id=request.user_id or "default_user",
        context={"items": request.items}
    )
    return response
```

### 3. Order Tracking Integration

**Frontend Flow:**
```typescript
// OrderTrackingComponent.tsx
const { data: orders, isLoading } = useOrders();

// Real-time updates every 30 seconds
const { data: orderStatus } = useOrderStatus(orderId, true);
```

**Backend Processing:**
```python
# main.py - /quick-order/status/{order_id} endpoint
@app.get("/quick-order/status/{order_id}")
async def get_order_status(order_id: str, user_id: str = "default_user"):
    response = await master_agent.process_request(
        message=f"order_status: {order_id}",
        user_id=user_id,
        context={"order_id": order_id}
    )
    return response
```

## 📊 Data Flow

### 1. Voice Order → Price Comparison
```
User Voice Input
    ↓
VoiceOrderComponent (Frontend)
    ↓
/assistant API (Backend)
    ↓
MasterAgent.process_request()
    ↓
QuickCommerceAgent._quick_order()
    ↓
QuickCommerceScraper.find_best_deals()
    ↓
Price Comparison Data
    ↓
Frontend PriceComparisonComponent
```

### 2. Order Placement → Tracking
```
User Clicks "Order Now"
    ↓
PriceComparisonComponent (Frontend)
    ↓
/quick-order API (Backend)
    ↓
QuickCommerceAgent._place_order_automation()
    ↓
QuickCommerceScraper.place_order()
    ↓
Order Confirmation
    ↓
Frontend OrderTrackingComponent
```

## 🔧 Configuration

### Backend Configuration
```python
# main.py
app = FastAPI(
    title="QuickPick API",
    description="AI-powered quick commerce system",
    version="1.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Frontend Configuration
```typescript
// src/config/environment.ts
export const config = {
  apiBaseUrl: 'http://localhost:8000',
  endpoints: {
    quickOrder: '/quick-order',
    assistant: '/assistant',
    orderStatus: '/quick-order/status',
    // ... other endpoints
  }
};
```

## 🧪 Testing Integration

### Backend API Testing
```bash
# Test all endpoints
curl -X POST "http://localhost:8000/assistant" \
  -H "Content-Type: application/json" \
  -d '{"message": "Order tomatoes", "user_id": "test_user"}'

curl -X POST "http://localhost:8000/quick-order" \
  -H "Content-Type: application/json" \
  -d '{"items": ["tomatoes", "milk"], "delivery_preference": "fastest"}'
```

### Frontend Testing
```bash
# Test frontend components
cd quickpick_frontend
npm run test

# Test API integration
npm run test:integration
```

## 🐛 Troubleshooting

### Common Issues

#### 1. CORS Errors
**Problem:** Frontend can't connect to backend
**Solution:** Check CORS configuration in `main.py`
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Ensure this matches frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 2. API Connection Failed
**Problem:** Frontend shows "Failed to fetch" errors
**Solution:** 
- Verify backend is running on port 8000
- Check `VITE_API_BASE_URL` in frontend config
- Ensure no firewall blocking the connection

#### 3. Voice Recognition Not Working
**Problem:** Microphone not working in browser
**Solution:**
- Check browser permissions for microphone access
- Ensure HTTPS in production (Web Speech API requirement)
- Verify browser compatibility

#### 4. Order Placement Failing
**Problem:** Orders not being placed successfully
**Solution:**
- Check backend logs for scraping errors
- Verify Selenium WebDriver is properly configured
- Ensure quick commerce platforms are accessible

### Debug Mode

#### Backend Debug
```bash
# Run with debug logging
python main.py --debug

# Check logs
tail -f logs/backend.log
```

#### Frontend Debug
```bash
# Run with debug mode
cd quickpick_frontend
npm run dev -- --debug

# Check browser console for errors
# Check Network tab for API calls
```

## 📈 Performance Optimization

### Backend Optimization
- **Caching**: Implement Redis for price comparison caching
- **Async Processing**: Use background tasks for order placement
- **Rate Limiting**: Implement rate limiting for API endpoints
- **Database**: Add PostgreSQL for persistent data storage

### Frontend Optimization
- **Code Splitting**: Implement lazy loading for components
- **Caching**: Use React Query for intelligent caching
- **Bundle Size**: Optimize bundle size with tree shaking
- **PWA**: Add Progressive Web App features

## 🔒 Security Considerations

### Backend Security
- **Authentication**: Implement JWT-based authentication
- **Rate Limiting**: Prevent API abuse
- **Input Validation**: Validate all user inputs
- **HTTPS**: Use HTTPS in production

### Frontend Security
- **Environment Variables**: Don't expose sensitive data
- **Content Security Policy**: Implement CSP headers
- **XSS Protection**: Sanitize user inputs
- **API Keys**: Store API keys securely

## 🚀 Deployment

### Production Deployment

#### Backend Deployment
```bash
# Using Docker
docker build -t quickpick-backend .
docker run -p 8000:8000 quickpick-backend

# Using cloud platforms
# Deploy to AWS, GCP, or Azure
```

#### Frontend Deployment
```bash
# Build for production
cd quickpick_frontend
npm run build

# Deploy to Vercel, Netlify, or AWS S3
```

### Environment Variables
```bash
# Backend
export DATABASE_URL="postgresql://..."
export REDIS_URL="redis://..."
export API_KEY="your-api-key"

# Frontend
export VITE_API_BASE_URL="https://api.quickpick.com"
export VITE_ANALYTICS_ID="your-analytics-id"
```

## 📚 Additional Resources

- [Backend API Documentation](http://localhost:8000/docs)
- [Frontend Component Library](./quickpick_frontend/README.md)
- [Quick Commerce Scraper Documentation](./mcp/quick_commerce_scrapper.py)
- [Master Agent Documentation](./master/master_agent.py)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both frontend and backend
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
