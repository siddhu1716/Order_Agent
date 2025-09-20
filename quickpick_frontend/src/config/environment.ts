// Environment configuration for QuickPick frontend
export const config = {
  // API Configuration
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  
  // App Configuration
  appName: import.meta.env.VITE_APP_NAME || 'QuickPick',
  appVersion: import.meta.env.VITE_APP_VERSION || '1.0.0',
  
  // Feature Flags
  enableVoiceCommands: import.meta.env.VITE_ENABLE_VOICE_COMMANDS === 'true',
  enableRealTimeUpdates: import.meta.env.VITE_ENABLE_REAL_TIME_UPDATES === 'true',
  enableNotifications: import.meta.env.VITE_ENABLE_NOTIFICATIONS === 'true',
  
  // Analytics
  analyticsId: import.meta.env.VITE_ANALYTICS_ID || '',
  
  // Environment
  nodeEnv: import.meta.env.VITE_NODE_ENV || 'development',
  isDevelopment: import.meta.env.DEV,
  isProduction: import.meta.env.PROD,
  
  // Quick Commerce Platforms
  supportedPlatforms: [
    { id: 'zepto', name: 'Zepto', logo: '⚡', color: '#00D4AA' },
    { id: 'blinkit', name: 'Blinkit', logo: '🛒', color: '#FF6B35' },
    { id: 'swiggy_instamart', name: 'Swiggy Instamart', logo: '🍊', color: '#FF6B35' },
    { id: 'bigbasket', name: 'BigBasket', logo: '🥬', color: '#00A651' },
  ],
  
  // Default Settings
  defaultDeliveryPreference: 'fastest' as const,
  defaultAutoApproveThreshold: 50, // ₹50
  defaultQualityThreshold: 4.0,
  
  // API Endpoints
  endpoints: {
    quickOrder: '/quick-order',
    orderApproval: '/quick-order/approve',
    orderStatus: '/quick-order/status',
    assistant: '/assistant',
    speechToText: '/speech-to-text',
    health: '/health',
    status: '/status',
    testQuickCommerce: '/test/quick-commerce',
    testFood: '/test/food',
    testTravel: '/test/travel',
    testShopping: '/test/shopping',
    testPayment: '/test/payment',
  },
  
  // UI Configuration
  ui: {
    animationDuration: 300,
    toastDuration: 5000,
    refetchInterval: 30000, // 30 seconds
    maxRetries: 3,
  },
  
  // Voice Configuration
  voice: {
    language: 'en-US',
    continuous: false,
    interimResults: false,
    maxAlternatives: 1,
  },
  
  // Order Configuration
  order: {
    maxItems: 20,
    maxQuantity: 10,
    supportedCurrencies: ['INR'],
    defaultCurrency: 'INR',
  },
};

export default config;
