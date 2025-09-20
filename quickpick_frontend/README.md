# QuickPick Frontend

A modern, AI-powered frontend for the QuickPick quick commerce system that automatically compares prices across multiple delivery platforms and places optimized orders.

## 🚀 Features

### Core Functionality
- **Voice-Enabled Ordering**: Place orders using natural voice commands
- **Real-time Price Comparison**: Compare prices across Zepto, Blinkit, Swiggy Instamart, and BigBasket
- **Smart Order Management**: Track orders with real-time status updates
- **Nutrition Dashboard**: Track calories and protein from purchases
- **Savings Tracker**: Monitor time and money saved

### Technical Features
- **React 18** with TypeScript for type safety
- **Tailwind CSS** for modern, responsive design
- **React Query** for efficient data fetching and caching
- **Radix UI** components for accessibility
- **Framer Motion** for smooth animations
- **Web Speech API** for voice recognition
- **Real-time updates** with WebSocket support

## 🏗️ Architecture

### Component Structure
```
src/
├── components/           # Reusable UI components
│   ├── ui/              # Base UI components (Radix UI)
│   ├── VoiceOrderComponent.tsx
│   ├── PriceComparisonComponent.tsx
│   ├── OrderTrackingComponent.tsx
│   ├── NutritionDashboard.tsx
│   └── QuickActionsFloat.tsx
├── hooks/               # Custom React hooks
│   ├── useQuickOrder.ts
│   └── use-mobile.tsx
├── lib/                 # Utility libraries
│   ├── api.ts          # API client and data transformation
│   └── utils.ts        # General utilities
├── config/             # Configuration files
│   └── environment.ts  # Environment variables and settings
└── pages/              # Page components
    ├── Index.tsx       # Main dashboard
    └── NotFound.tsx    # 404 page
```

### API Integration
- **RESTful API** communication with FastAPI backend
- **React Query** for state management and caching
- **Type-safe** API calls with TypeScript interfaces
- **Error handling** with user-friendly notifications
- **Loading states** and optimistic updates

## 🛠️ Setup & Installation

### Prerequisites
- Node.js 18+ or Bun
- Backend API running on `http://localhost:8000`

### Installation
```bash
# Install dependencies
npm install
# or
bun install

# Start development server
npm run dev
# or
bun dev

# Build for production
npm run build
# or
bun build
```

### Environment Configuration
Create a `.env.local` file in the root directory:
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=QuickPick
VITE_ENABLE_VOICE_COMMANDS=true
VITE_ENABLE_REAL_TIME_UPDATES=true
```

## 🎨 Design System

### Color Palette
- **Primary**: Blue (#2563EB) - Trust and reliability
- **Success**: Green (#10B981) - Success and savings
- **Warning**: Amber (#F59E0B) - Attention and deals
- **Error**: Red (#EF4444) - Errors and cancellations

### Typography
- **Font**: Inter (Google Fonts)
- **Headers**: 600-700 weight, 24-32px
- **Body**: 400 weight, 16px
- **Captions**: 500 weight, 14px

### Components
- **Cards**: Rounded corners, subtle shadows
- **Buttons**: Multiple variants (primary, secondary, outline, ghost)
- **Badges**: Status indicators and labels
- **Progress**: Order tracking and loading states

## 🔌 API Integration

### Quick Order API
```typescript
// Place a quick order
const response = await apiClient.placeQuickOrder({
  items: ['tomatoes', 'milk', 'bread'],
  delivery_preference: 'fastest',
  auto_approve: false
});
```

### Voice Command API
```typescript
// Process voice command
const response = await apiClient.processVoiceCommand({
  message: 'Order tomatoes and milk',
  user_id: 'user123'
});
```

### Order Status API
```typescript
// Get order status
const order = await apiClient.getOrderStatus('order123');
```

## 🎯 Key Components

### VoiceOrderComponent
- **Voice Recognition**: Web Speech API integration
- **Real-time Transcription**: Live voice-to-text conversion
- **AI Suggestions**: Smart product recommendations
- **Visual Feedback**: Animated waveform and status indicators

### PriceComparisonComponent
- **Multi-platform Comparison**: Side-by-side price comparison
- **Sorting Options**: By price, delivery time, or rating
- **Best Deal Highlighting**: Visual emphasis on optimal choices
- **One-click Ordering**: Direct order placement

### OrderTrackingComponent
- **Real-time Updates**: Live order status tracking
- **Progress Visualization**: Step-by-step delivery progress
- **Delivery Person Info**: Contact details and ratings
- **Interactive Actions**: Call delivery person, track live location

## 🚀 Deployment

### Production Build
```bash
# Build optimized production bundle
npm run build

# Preview production build
npm run preview
```

### Environment Variables
Set the following environment variables in production:
- `VITE_API_BASE_URL`: Backend API URL
- `VITE_APP_NAME`: Application name
- `VITE_ANALYTICS_ID`: Analytics tracking ID (optional)

### Hosting
The built application can be deployed to:
- **Vercel**: Zero-config deployment
- **Netlify**: Drag-and-drop deployment
- **AWS S3**: Static website hosting
- **GitHub Pages**: Free hosting for public repos

## 🧪 Testing

### Component Testing
```bash
# Run component tests
npm run test

# Run tests in watch mode
npm run test:watch
```

### E2E Testing
```bash
# Run end-to-end tests
npm run test:e2e
```

## 📱 Responsive Design

### Breakpoints
- **Mobile**: 320px - 768px
- **Tablet**: 768px - 1024px
- **Desktop**: 1024px+

### Mobile Features
- Touch-friendly interface
- Swipe gestures
- Bottom navigation
- Optimized voice controls

## 🔧 Development

### Code Style
- **ESLint**: Code linting and formatting
- **Prettier**: Code formatting
- **TypeScript**: Type checking
- **Husky**: Git hooks for quality checks

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/voice-commands

# Make changes and commit
git add .
git commit -m "feat: add voice command processing"

# Push and create PR
git push origin feature/voice-commands
```

## 🐛 Troubleshooting

### Common Issues

#### Voice Recognition Not Working
- Check browser permissions for microphone access
- Ensure HTTPS in production (required for Web Speech API)
- Verify browser compatibility

#### API Connection Issues
- Verify backend is running on correct port
- Check CORS configuration
- Validate API endpoints

#### Build Errors
- Clear node_modules and reinstall dependencies
- Check TypeScript errors
- Verify environment variables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Radix UI** for accessible component primitives
- **Tailwind CSS** for utility-first styling
- **React Query** for data fetching
- **Lucide React** for beautiful icons
- **Framer Motion** for smooth animations