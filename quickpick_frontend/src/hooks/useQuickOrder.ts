import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient, transformPlatformData, transformOrderData, QuickOrderRequest, OrderApprovalRequest } from '@/lib/api';

// Query keys
export const QUERY_KEYS = {
  orders: ['orders'] as const,
  orderStatus: (orderId: string) => ['orders', orderId] as const,
  systemStatus: ['systemStatus'] as const,
  health: ['health'] as const,
};

// Hook for placing quick orders
export const usePlaceQuickOrder = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: QuickOrderRequest) => apiClient.placeQuickOrder(request),
    onSuccess: (data) => {
      // Invalidate orders query to refetch
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.orders });
      
      // Show success notification
      console.log('Order placed successfully:', data);
    },
    onError: (error) => {
      console.error('Failed to place order:', error);
    },
  });
};

// Hook for processing voice commands
export const useVoiceCommand = () => {
  return useMutation({
    mutationFn: ({ message, user_id }: { message: string; user_id?: string }) => 
      apiClient.processVoiceCommand(message, user_id),
    onSuccess: (data) => {
      console.log('Voice command processed:', data);
    },
    onError: (error) => {
      console.error('Voice command failed:', error);
    },
  });
};

// Hook for approving orders
export const useApproveOrder = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: OrderApprovalRequest) => apiClient.approveOrder(request),
    onSuccess: (data) => {
      // Invalidate orders query
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.orders });
      console.log('Order approved:', data);
    },
    onError: (error) => {
      console.error('Order approval failed:', error);
    },
  });
};

// Hook for getting order status
export const useOrderStatus = (orderId: string, enabled: boolean = true) => {
  return useQuery({
    queryKey: QUERY_KEYS.orderStatus(orderId),
    queryFn: () => apiClient.getOrderStatus(orderId),
    enabled: enabled && !!orderId,
    refetchInterval: 30000, // Refetch every 30 seconds for active orders
    select: (data) => transformOrderData(data),
  });
};

// Hook for getting all orders (mock data for now)
export const useOrders = () => {
  return useQuery({
    queryKey: QUERY_KEYS.orders,
    queryFn: async () => {
      // For now, return mock data
      // In a real app, you'd have an endpoint to get all user orders
      return [
        {
          id: 'ZEP001',
          platform: 'Zepto',
          items: 'Tomatoes, Milk, Bread',
          total: 245,
          status: 'out_for_delivery' as const,
          estimatedTime: '6 mins',
          deliveryPerson: {
            name: 'Rahul Kumar',
            phone: '+91 98765 43210',
            rating: 4.8
          }
        },
        {
          id: 'BLK002', 
          platform: 'Blinkit',
          items: 'Rice, Dal, Oil',
          total: 520,
          status: 'confirmed' as const,
          estimatedTime: '12 mins'
        }
      ];
    },
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
};

// Hook for system health check
export const useSystemHealth = () => {
  return useQuery({
    queryKey: QUERY_KEYS.health,
    queryFn: () => apiClient.healthCheck(),
    refetchInterval: 60000, // Check every minute
    retry: 3,
  });
};

// Hook for system status
export const useSystemStatus = () => {
  return useQuery({
    queryKey: QUERY_KEYS.systemStatus,
    queryFn: () => apiClient.getSystemStatus(),
    staleTime: 1000 * 60 * 2, // 2 minutes
  });
};

// Hook for testing APIs
export const useTestApis = () => {
  const queryClient = useQueryClient();

  const testQuickCommerce = useMutation({
    mutationFn: () => apiClient.testQuickCommerce(),
    onSuccess: (data) => {
      console.log('Quick commerce test:', data);
    },
  });

  const testFoodAgent = useMutation({
    mutationFn: () => apiClient.testFoodAgent(),
    onSuccess: (data) => {
      console.log('Food agent test:', data);
    },
  });

  const testTravelAgent = useMutation({
    mutationFn: () => apiClient.testTravelAgent(),
    onSuccess: (data) => {
      console.log('Travel agent test:', data);
    },
  });

  const testShoppingAgent = useMutation({
    mutationFn: () => apiClient.testShoppingAgent(),
    onSuccess: (data) => {
      console.log('Shopping agent test:', data);
    },
  });

  const testPaymentAgent = useMutation({
    mutationFn: () => apiClient.testPaymentAgent(),
    onSuccess: (data) => {
      console.log('Payment agent test:', data);
    },
  });

  return {
    testQuickCommerce,
    testFoodAgent,
    testTravelAgent,
    testShoppingAgent,
    testPaymentAgent,
  };
};

// Hook for speech-to-text
export const useSpeechToText = () => {
  return useMutation({
    mutationFn: ({ audioFile, language }: { audioFile: File; language?: string }) => 
      apiClient.transcribeAudio(audioFile, language),
    onSuccess: (data) => {
      console.log('Speech transcribed:', data);
    },
    onError: (error) => {
      console.error('Speech transcription failed:', error);
    },
  });
};
