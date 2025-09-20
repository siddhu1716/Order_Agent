import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import VoiceOrderComponent from '@/components/VoiceOrderComponent';
import PriceComparisonComponent from '@/components/PriceComparisonComponent';
import OrderTrackingComponent from '@/components/OrderTrackingComponent';
import NutritionDashboard from '@/components/NutritionDashboard';
import QuickActionsFloat from '@/components/QuickActionsFloat';
import SavingsTracker from '@/components/SavingsTracker';
import heroBanner from '@/assets/hero-banner.jpg';
import { 
  ShoppingCart, 
  TrendingDown, 
  Clock, 
  User, 
  Bell,
  Zap,
  Sparkles
} from 'lucide-react';

const Index = () => {
  const [currentOrder, setCurrentOrder] = useState<string>('');
  const [showComparison, setShowComparison] = useState(false);

  const handleOrderPlaced = (items: string) => {
    setCurrentOrder(items);
    setShowComparison(true);
    
    // Confetti effect for high savings orders
    if (items.includes('tomatoes')) {
      // Trigger confetti animation
      setTimeout(() => {
        console.log('🎉 High savings order!');
      }, 1000);
    }
  };

  const quickActions = {
    onQuickOrder: () => setShowComparison(true),
    onReorder: () => handleOrderPlaced("Previous order: Milk, Bread, Eggs"),
    onTrackOrders: () => console.log("Track orders"),
    onAddPantry: () => console.log("Add to pantry")
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-gradient-hero flex items-center justify-center">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <h1 className="text-xl font-bold bg-gradient-hero bg-clip-text text-transparent">
                QuickPick
              </h1>
            </div>
            
            <div className="flex items-center gap-4">
              <Badge variant="secondary" className="hidden md:flex animate-pulse">
                <TrendingDown className="w-3 h-3 mr-1" />
                Save 20-30 mins
              </Badge>
              <Badge variant="outline" className="hidden md:flex">
                <Sparkles className="w-3 h-3 mr-1" />
                AI Powered
              </Badge>
              <Button variant="ghost" size="icon" className="hover:scale-110 transition-transform">
                <Bell className="w-5 h-5" />
              </Button>
              <Button variant="ghost" size="icon" className="hover:scale-110 transition-transform">
                <User className="w-5 h-5" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-8">
        <div className="text-center space-y-4 mb-8">
          <div className="relative mb-8">
            <img 
              src={heroBanner} 
              alt="QuickPick - Smart grocery shopping with voice ordering and price comparison"
              className="w-full max-w-4xl mx-auto rounded-2xl shadow-xl"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-background/80 to-transparent rounded-2xl" />
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold">
            Smart Grocery Shopping
            <span className="block text-3xl md:text-4xl bg-gradient-primary bg-clip-text text-transparent">
              Made Effortless with QuickPick
            </span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Compare prices across Zepto, Blinkit, Swiggy Instamart & BigBasket. 
            Order with your voice and save time & money automatically.
          </p>
          
          <div className="flex items-center justify-center gap-6 text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-success" />
              <span>Saves 20-30 mins</span>
            </div>
            <div className="flex items-center gap-2">
              <TrendingDown className="w-4 h-4 text-success" />
              <span>Best prices guaranteed</span>
            </div>
            <div className="flex items-center gap-2">
              <ShoppingCart className="w-4 h-4 text-success" />
              <span>One-click ordering</span>
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
          {/* Voice Order Component */}
          <div className="lg:col-span-1 space-y-6">
            <VoiceOrderComponent onOrderPlaced={handleOrderPlaced} />
            <SavingsTracker />
          </div>

          {/* Price Comparison */}
          <div className="lg:col-span-2">
            {showComparison ? (
              <div className="space-y-6 animate-fade-in">
                <PriceComparisonComponent 
                  items={currentOrder}
                  onPlatformSelect={(platform) => console.log('Selected:', platform)}
                />
              </div>
            ) : (
              <div className="h-full flex items-center justify-center p-8 border-2 border-dashed border-muted-foreground/25 rounded-lg hover:border-muted-foreground/50 transition-colors">
                <div className="text-center space-y-4">
                  <ShoppingCart className="w-12 h-12 mx-auto text-muted-foreground animate-pulse" />
                  <p className="text-lg font-medium text-muted-foreground">
                    Place a voice order to see price comparison
                  </p>
                  <p className="text-sm text-muted-foreground">
                    Or type your items manually to get started
                  </p>
                  <Button 
                    variant="outline" 
                    onClick={() => handleOrderPlaced("Tomatoes, Milk, Bread")}
                    className="hover:scale-105 transition-transform"
                  >
                    Try Sample Order
                  </Button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Order Tracking Section */}
        <div className="mb-12">
          <OrderTrackingComponent />
        </div>

        {/* Nutrition Dashboard */}
        <div className="mb-12">
          <NutritionDashboard />
        </div>
      </section>

      {/* Quick Actions Float */}
      <QuickActionsFloat {...quickActions} />

      {/* Footer */}
      <footer className="border-t border-border bg-card/50 py-8">
        <div className="container mx-auto px-4 text-center">
          <p className="text-sm text-muted-foreground">
            QuickPick - Making grocery shopping intelligent and effortless
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
