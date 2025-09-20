import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { 
  Package, 
  CheckCircle, 
  Truck, 
  MapPin, 
  Clock, 
  Phone,
  Star
} from 'lucide-react';
import { useOrders } from '@/hooks/useQuickOrder';
import { OrderData } from '@/lib/api';

// Remove duplicate interface - using the one from api.ts

const mockOrders: OrderData[] = [
  {
    id: 'ZEP001',
    platform: 'Zepto',
    items: 'Tomatoes, Milk, Bread',
    total: 245,
    status: 'out_for_delivery',
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
    status: 'confirmed',
    estimatedTime: '12 mins'
  }
];

const getStatusProgress = (status: OrderData['status']) => {
  switch (status) {
    case 'placed': return 25;
    case 'confirmed': return 50;
    case 'preparing': return 65;
    case 'out_for_delivery': return 85;
    case 'delivered': return 100;
    default: return 0;
  }
};

const getStatusColor = (status: OrderData['status']) => {
  switch (status) {
    case 'placed':
    case 'confirmed':
      return 'bg-primary';
    case 'preparing':
      return 'bg-warning';
    case 'out_for_delivery':
      return 'bg-warning';
    case 'delivered':
      return 'bg-success';
    default:
      return 'bg-muted';
  }
};

const getStatusIcon = (status: OrderData['status']) => {
  switch (status) {
    case 'placed':
      return <Package className="w-5 h-5" />;
    case 'confirmed':
      return <CheckCircle className="w-5 h-5" />;
    case 'preparing':
      return <Package className="w-5 h-5" />;
    case 'out_for_delivery':
      return <Truck className="w-5 h-5" />;
    case 'delivered':
      return <CheckCircle className="w-5 h-5" />;
    default:
      return <Package className="w-5 h-5" />;
  }
};

const getStatusText = (status: OrderData['status']) => {
  switch (status) {
    case 'placed': return 'Order Placed';
    case 'confirmed': return 'Order Confirmed';
    case 'preparing': return 'Being Prepared';
    case 'out_for_delivery': return 'Out for Delivery';
    case 'delivered': return 'Delivered';
    default: return 'Unknown';
  }
};

const OrderTrackingComponent: React.FC = () => {
  const { data: orders, isLoading, error } = useOrders();

  if (isLoading) {
    return (
      <div className="w-full space-y-6">
        <div className="text-center space-y-2">
          <h3 className="text-2xl font-bold">Active Orders</h3>
          <p className="text-muted-foreground">Loading your orders...</p>
        </div>
        <div className="grid gap-6">
          {[1, 2].map((i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="p-6">
                <div className="h-4 bg-muted rounded w-1/4 mb-2"></div>
                <div className="h-3 bg-muted rounded w-1/2 mb-4"></div>
                <div className="h-2 bg-muted rounded w-full"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="w-full space-y-6">
        <div className="text-center space-y-2">
          <h3 className="text-2xl font-bold">Active Orders</h3>
          <p className="text-muted-foreground text-destructive">Failed to load orders</p>
        </div>
      </div>
    );
  }

  const displayOrders = orders || mockOrders;

  return (
    <div className="w-full space-y-6">
      <div className="text-center space-y-2">
        <h3 className="text-2xl font-bold">Active Orders</h3>
        <p className="text-muted-foreground">Track your deliveries in real-time</p>
      </div>

      <div className="grid gap-6">
        {displayOrders.map((order) => (
          <Card key={order.id} className="fade-in">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">Order #{order.id}</CardTitle>
                <Badge variant="outline" className="font-mono">
                  {order.platform}
                </Badge>
              </div>
              <p className="text-sm text-muted-foreground">{order.items}</p>
            </CardHeader>

            <CardContent className="space-y-6">
              {/* Status Progress */}
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    {getStatusIcon(order.status)}
                    <span className="font-medium">{getStatusText(order.status)}</span>
                  </div>
                  <div className="flex items-center gap-1 text-sm text-muted-foreground">
                    <Clock className="w-4 h-4" />
                    {order.estimatedTime}
                  </div>
                </div>
                
                <Progress 
                  value={getStatusProgress(order.status)} 
                  className="h-2"
                />
              </div>

              {/* Order Details */}
              <div className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                <div>
                  <p className="font-medium">Total Amount</p>
                  <p className="text-2xl font-bold">₹{order.total}</p>
                </div>
                
                {order.deliveryPerson && (
                  <div className="text-right">
                    <p className="font-medium">{order.deliveryPerson.name}</p>
                    <div className="flex items-center gap-1 text-sm text-muted-foreground">
                      <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                      {order.deliveryPerson.rating}
                    </div>
                  </div>
                )}
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3">
                {order.deliveryPerson && (
                  <Button variant="outline" size="sm" className="flex-1">
                    <Phone className="w-4 h-4 mr-2" />
                    Call Delivery Person
                  </Button>
                )}
                <Button variant="outline" size="sm" className="flex-1">
                  <MapPin className="w-4 h-4 mr-2" />
                  Track Live
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Quick Reorder */}
      <Card className="border-dashed border-2 border-muted-foreground/25">
        <CardContent className="text-center py-8">
          <p className="text-muted-foreground mb-4">Need something else?</p>
          <Button variant="premium" size="lg">
            Start New Order
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default OrderTrackingComponent;