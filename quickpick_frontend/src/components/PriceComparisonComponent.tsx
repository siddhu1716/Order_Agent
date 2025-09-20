import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Clock, Star, TrendingDown, Filter, ArrowUpDown } from 'lucide-react';
import { usePlaceQuickOrder, useApproveOrder } from '@/hooks/useQuickOrder';
import { transformPlatformData, PlatformData } from '@/lib/api';
import { toast } from 'sonner';

// Remove duplicate interface - using the one from api.ts

interface PriceComparisonComponentProps {
  items?: string;
  onPlatformSelect?: (platformId: string) => void;
}

const mockPlatforms: PlatformData[] = [
  {
    id: 'zepto',
    name: 'Zepto',
    logo: '⚡',
    price: 245,
    deliveryTime: '8-12 min',
    rating: 4.5,
    isBestDeal: true,
    savings: 35,
    discount: '15% OFF',
    deliveryFee: 0
  },
  {
    id: 'blinkit',
    name: 'Blinkit',
    logo: '🛒',
    price: 280,
    deliveryTime: '10-15 min',
    rating: 4.3,
    deliveryFee: 15
  },
  {
    id: 'swiggy',
    name: 'Swiggy Instamart',
    logo: '🍊',
    price: 265,
    deliveryTime: '15-20 min',
    rating: 4.4,
    deliveryFee: 25
  },
  {
    id: 'bigbasket',
    name: 'BigBasket',
    logo: '🥬',
    price: 290,
    deliveryTime: '25-30 min',
    rating: 4.2,
    deliveryFee: 30
  }
];

const PriceComparisonComponent: React.FC<PriceComparisonComponentProps> = ({ 
  items = "Tomatoes, Milk, Bread", 
  onPlatformSelect 
}) => {
  const [sortBy, setSortBy] = useState<'price' | 'delivery' | 'rating'>('price');
  const [expandedCard, setExpandedCard] = useState<string | null>(null);
  const [showConfetti, setShowConfetti] = useState(false);
  const [platforms, setPlatforms] = useState<PlatformData[]>(mockPlatforms);
  const [isLoading, setIsLoading] = useState(false);
  
  // API hooks
  const placeOrderMutation = usePlaceQuickOrder();
  const approveOrderMutation = useApproveOrder();

  // Fetch price comparison when items change
  useEffect(() => {
    if (items && items !== "Tomatoes, Milk, Bread") {
      fetchPriceComparison();
    }
  }, [items]);

  const fetchPriceComparison = async () => {
    setIsLoading(true);
    try {
      const itemsArray = items.split(',').map(item => item.trim());
      const response = await placeOrderMutation.mutateAsync({
        items: itemsArray,
        delivery_preference: 'fastest',
        auto_approve: false,
      });
      
      // Transform backend data to frontend format
      const transformedPlatforms = transformPlatformData(response);
      if (transformedPlatforms.length > 0) {
        setPlatforms(transformedPlatforms);
      }
    } catch (error) {
      console.error('Failed to fetch price comparison:', error);
      toast.error('Failed to fetch price comparison', {
        description: 'Using cached data. Please try again.',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handlePlatformSelect = (platformId: string, platform: PlatformData) => {
    if (platform.isBestDeal) {
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 2000);
    }
    
    // Place order through backend
    const itemsArray = items.split(',').map(item => item.trim());
    placeOrderMutation.mutate(
      {
        items: itemsArray,
        delivery_preference: 'fastest',
        auto_approve: true,
      },
      {
        onSuccess: (data) => {
          toast.success('Order placed successfully!', {
            description: `Order ID: ${data.data.order_result?.order_id}`,
          });
          onPlatformSelect?.(platformId);
        },
        onError: (error) => {
          toast.error('Failed to place order', {
            description: 'Please try again or contact support.',
          });
        }
      }
    );
  };

  const sortedPlatforms = [...platforms].sort((a, b) => {
    switch (sortBy) {
      case 'price':
        return a.price - b.price;
      case 'delivery':
        return parseInt(a.deliveryTime) - parseInt(b.deliveryTime);
      case 'rating':
        return b.rating - a.rating;
      default:
        return 0;
    }
  });

  return (
    <div className="w-full space-y-6">
      {/* Header with Sorting */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="space-y-2">
          <h3 className="text-2xl font-bold">Price Comparison</h3>
          <p className="text-muted-foreground">For: {items}</p>
        </div>
        
        <div className="flex items-center gap-3">
          <Filter className="w-4 h-4 text-muted-foreground" />
          <div className="flex gap-2">
            {[
              { key: 'price', label: 'Cheapest' },
              { key: 'delivery', label: 'Fastest' },
              { key: 'rating', label: 'Best Rated' }
            ].map(({ key, label }) => (
              <Button
                key={key}
                variant={sortBy === key ? "default" : "outline"}
                size="sm"
                onClick={() => setSortBy(key as any)}
                className="transition-all hover:scale-105"
              >
                <ArrowUpDown className="w-3 h-3 mr-1" />
                {label}
              </Button>
            ))}
          </div>
        </div>
      </div>

      {/* Confetti Effect */}
      {showConfetti && (
        <div className="fixed inset-0 pointer-events-none z-50 flex items-center justify-center">
          <div className="text-6xl animate-confetti">🎉</div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {sortedPlatforms.map((platform) => (
          <Card 
            key={platform.id} 
            className={`relative transition-all duration-300 cursor-pointer group ${
              platform.isBestDeal 
                ? 'ring-2 ring-success shadow-success bg-gradient-to-br from-success/5 to-success/10 hover:scale-105' 
                : 'hover:shadow-xl hover:scale-102'
            } ${expandedCard === platform.id ? 'scale-105 shadow-xl' : ''}`}
            onClick={() => handlePlatformSelect(platform.id, platform)}
            onMouseEnter={() => setExpandedCard(platform.id)}
            onMouseLeave={() => setExpandedCard(null)}
          >
            {platform.isBestDeal && (
              <Badge className="absolute -top-2 -right-2 bg-gradient-success text-success-foreground animate-pulse">
                <TrendingDown className="w-3 h-3 mr-1" />
                Best Deal
              </Badge>
            )}

            {platform.discount && (
              <Badge variant="destructive" className="absolute -top-2 -left-2 animate-bounce">
                {platform.discount}
              </Badge>
            )}

            <CardHeader className="text-center pb-4">
              <div className="text-4xl mb-2 group-hover:scale-110 transition-transform">
                {platform.logo}
              </div>
              <CardTitle className="text-lg">{platform.name}</CardTitle>
            </CardHeader>

            <CardContent className="space-y-4">
              <div className="text-center">
                <p className="text-3xl font-bold text-foreground">₹{platform.price}</p>
                {platform.deliveryFee ? (
                  <p className="text-xs text-muted-foreground">+ ₹{platform.deliveryFee} delivery</p>
                ) : (
                  <p className="text-xs text-success">Free delivery</p>
                )}
                {platform.savings && (
                  <p className="text-sm text-success font-medium animate-pulse">
                    Save ₹{platform.savings}
                  </p>
                )}
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-center gap-1 text-sm text-muted-foreground">
                  <Clock className="w-4 h-4" />
                  {platform.deliveryTime}
                </div>
                
                <div className="flex items-center justify-center gap-1 text-sm text-muted-foreground">
                  <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                  {platform.rating}
                </div>
              </div>

              {/* Expanded Info */}
              {expandedCard === platform.id && (
                <div className="space-y-2 animate-slide-down">
                  <div className="text-xs text-muted-foreground text-center">
                    • 24/7 Support
                  </div>
                  <div className="text-xs text-muted-foreground text-center">
                    • Fresh guarantee
                  </div>
                  {platform.isBestDeal && (
                    <div className="text-xs text-success text-center font-medium">
                      • Extra 5% cashback
                    </div>
                  )}
                </div>
              )}

              <Button 
                variant={platform.isBestDeal ? "success" : "platform"}
                size="sm"
                className="w-full group-hover:scale-105 transition-transform"
              >
                {platform.isBestDeal ? "Order Now 🎉" : "Select"}
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="text-center p-4 rounded-lg bg-muted/50 border animate-fade-in">
        <p className="text-sm text-muted-foreground">
          💡 Choosing Zepto saves you <span className="font-semibold text-success animate-pulse">₹35</span> and 
          <span className="font-semibold text-primary"> 15+ minutes</span>
        </p>
      </div>
    </div>
  );
};

export default PriceComparisonComponent;