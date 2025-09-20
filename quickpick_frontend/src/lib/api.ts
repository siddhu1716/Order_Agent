// API integration layer for QuickPick frontend
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export interface QuickOrderRequest {
  items: string[];
  user_id?: string;
  delivery_preference?: 'fastest' | 'cheapest' | 'best_rated';
  auto_approve?: boolean;
}

export interface OrderApprovalRequest {
  order_id: string;
  approved: boolean;
  user_id?: string;
}

export interface PlatformData {
  id: string;
  name: string;
  logo: string;
  price: number;
  deliveryTime: string;
  rating: number;
  isBestDeal?: boolean;
  savings?: number;
  discount?: string;
  deliveryFee?: number;
}

export interface OrderData {
  id: string;
  platform: string;
  items: string;
  total: number;
  status: 'placed' | 'confirmed' | 'preparing' | 'out_for_delivery' | 'delivered';
  estimatedTime: string;
  deliveryPerson?: {
    name: string;
    phone: string;
    rating: number;
  };
}

export interface VoiceOrderResponse {
  status: string;
  data: {
    action: 'auto_ordered' | 'awaiting_approval';
    recommendation: {
      best_platform: string;
      total_cost: number;
      items: any[];
      platform_breakdown: any;
      savings: number;
      delivery_time: number;
      summary: string;
    };
    order_result?: {
      order_id: string;
      platform: string;
      items: any[];
      total_amount: number;
      estimated_delivery: string;
      tracking_url: string;
    };
    time_saved: string;
  };
  agent_used: string;
  timestamp: string;
}

class ApiClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const defaultHeaders = {
      'Content-Type': 'application/json',
    };

    const config: RequestInit = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Voice Order API
  async placeQuickOrder(request: QuickOrderRequest): Promise<VoiceOrderResponse> {
    return this.request<VoiceOrderResponse>('/quick-order', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // Assistant API (for voice commands)
  async processVoiceCommand(message: string, user_id: string = 'default_user'): Promise<VoiceOrderResponse> {
    return this.request<VoiceOrderResponse>('/assistant', {
      method: 'POST',
      body: JSON.stringify({
        message,
        user_id,
        context: {}
      }),
    });
  }

  // Order Approval API
  async approveOrder(request: OrderApprovalRequest): Promise<any> {
    return this.request('/quick-order/approve', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // Order Status API
  async getOrderStatus(order_id: string, user_id: string = 'default_user'): Promise<any> {
    return this.request(`/quick-order/status/${order_id}?user_id=${user_id}`, {
      method: 'GET',
    });
  }

  // Speech to Text API
  async transcribeAudio(audioFile: File, language: string = 'en'): Promise<any> {
    const formData = new FormData();
    formData.append('file', audioFile);
    formData.append('language', language);

    return this.request('/speech-to-text', {
      method: 'POST',
      headers: {}, // Let browser set Content-Type for FormData
      body: formData,
    });
  }

  // Test APIs
  async testQuickCommerce(): Promise<any> {
    return this.request('/test/quick-commerce', {
      method: 'POST',
    });
  }

  async testFoodAgent(): Promise<any> {
    return this.request('/test/food', {
      method: 'POST',
    });
  }

  async testTravelAgent(): Promise<any> {
    return this.request('/test/travel', {
      method: 'POST',
    });
  }

  async testShoppingAgent(): Promise<any> {
    return this.request('/test/shopping', {
      method: 'POST',
    });
  }

  async testPaymentAgent(): Promise<any> {
    return this.request('/test/payment', {
      method: 'POST',
    });
  }

  // Health Check
  async healthCheck(): Promise<any> {
    return this.request('/health', {
      method: 'GET',
    });
  }

  // System Status
  async getSystemStatus(): Promise<any> {
    return this.request('/status', {
      method: 'GET',
    });
  }
}

// Create and export API client instance
export const apiClient = new ApiClient();

// Utility functions for data transformation
export const transformPlatformData = (backendData: any): PlatformData[] => {
  // Transform backend platform data to frontend format
  if (!backendData?.recommendation?.platform_breakdown) {
    return [];
  }

  const platforms: PlatformData[] = [];
  const breakdown = backendData.recommendation.platform_breakdown;

  Object.entries(breakdown).forEach(([platformName, data]: [string, any]) => {
    platforms.push({
      id: platformName.toLowerCase(),
      name: platformName.charAt(0).toUpperCase() + platformName.slice(1),
      logo: getPlatformLogo(platformName),
      price: data.subtotal + data.delivery_fee,
      deliveryTime: `${data.delivery_time} min`,
      rating: 4.0 + Math.random() * 1.0, // Mock rating
      isBestDeal: platformName === backendData.recommendation.best_platform,
      savings: platformName === backendData.recommendation.best_platform ? backendData.recommendation.savings : 0,
      discount: Math.random() > 0.5 ? `${Math.floor(Math.random() * 20) + 5}% OFF` : undefined,
      deliveryFee: data.delivery_fee,
    });
  });

  return platforms;
};

export const transformOrderData = (backendData: any): OrderData[] => {
  // Transform backend order data to frontend format
  if (!backendData?.data?.orders) {
    return [];
  }

  return backendData.data.orders.map((order: any) => ({
    id: order.order_id,
    platform: order.platform,
    items: Array.isArray(order.items) ? order.items.map((item: any) => item.name || item).join(', ') : order.items,
    total: order.total_amount,
    status: mapOrderStatus(order.status),
    estimatedTime: order.estimated_delivery ? calculateTimeRemaining(order.estimated_delivery) : 'Unknown',
    deliveryPerson: order.delivery_person || undefined,
  }));
};

// Helper functions
const getPlatformLogo = (platformName: string): string => {
  const logos: { [key: string]: string } = {
    zepto: '⚡',
    blinkit: '🛒',
    swiggy_instamart: '🍊',
    bigbasket: '🥬',
  };
  return logos[platformName.toLowerCase()] || '🛍️';
};

const mapOrderStatus = (status: string): OrderData['status'] => {
  const statusMap: { [key: string]: OrderData['status'] } = {
    placed: 'placed',
    confirmed: 'confirmed',
    preparing: 'preparing',
    out_for_delivery: 'out_for_delivery',
    delivered: 'delivered',
  };
  return statusMap[status] || 'placed';
};

const calculateTimeRemaining = (estimatedDelivery: string): string => {
  try {
    const deliveryTime = new Date(estimatedDelivery);
    const now = new Date();
    const diffMs = deliveryTime.getTime() - now.getTime();
    const diffMins = Math.max(0, Math.round(diffMs / (1000 * 60)));
    return `${diffMins} mins`;
  } catch {
    return 'Unknown';
  }
};

// React Query hooks for API integration
export const useQuickOrder = () => {
  return {
    placeOrder: apiClient.placeQuickOrder,
    processVoiceCommand: apiClient.processVoiceCommand,
    approveOrder: apiClient.approveOrder,
    getOrderStatus: apiClient.getOrderStatus,
  };
};

export const useApiHealth = () => {
  return {
    healthCheck: apiClient.healthCheck,
    getSystemStatus: apiClient.getSystemStatus,
  };
};

export const useTestApis = () => {
  return {
    testQuickCommerce: apiClient.testQuickCommerce,
    testFoodAgent: apiClient.testFoodAgent,
    testTravelAgent: apiClient.testTravelAgent,
    testShoppingAgent: apiClient.testShoppingAgent,
    testPaymentAgent: apiClient.testPaymentAgent,
  };
};
