import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { TrendingDown, Trophy, Target } from 'lucide-react';

interface SavingsTrackerProps {
  monthlySavings?: number;
  yearlyGoal?: number;
}

const SavingsTracker: React.FC<SavingsTrackerProps> = ({ 
  monthlySavings = 1250, 
  yearlyGoal = 15000 
}) => {
  const [animatedSavings, setAnimatedSavings] = useState(0);
  const progressPercentage = Math.min((monthlySavings * 12 / yearlyGoal) * 100, 100);

  useEffect(() => {
    // Animate counter
    const timer = setInterval(() => {
      setAnimatedSavings(prev => {
        if (prev < monthlySavings) {
          return prev + 25;
        }
        clearInterval(timer);
        return monthlySavings;
      });
    }, 20);

    return () => clearInterval(timer);
  }, [monthlySavings]);

  const badges = [
    { label: 'Money Saver', earned: monthlySavings > 1000 },
    { label: 'Smart Shopper', earned: monthlySavings > 800 },
    { label: 'Deal Hunter', earned: monthlySavings > 500 }
  ];

  return (
    <Card className="bg-gradient-to-br from-success/5 to-success/10 border-success/20 hover:shadow-lg transition-all duration-300">
      <CardHeader className="pb-4">
        <CardTitle className="flex items-center gap-2 text-success">
          <TrendingDown className="w-5 h-5" />
          Monthly Savings Tracker
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Animated Savings Counter */}
        <div className="text-center space-y-2">
          <div className="text-4xl font-bold text-success">
            ₹{animatedSavings.toLocaleString()}
          </div>
          <p className="text-sm text-muted-foreground">
            Saved this month with QuickPick
          </p>
        </div>

        {/* Progress towards yearly goal */}
        <div className="space-y-3">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Yearly Goal Progress</span>
            <span className="font-medium">{progressPercentage.toFixed(0)}%</span>
          </div>
          <div className="relative h-3 bg-muted rounded-full overflow-hidden">
            <div 
              className="absolute inset-y-0 left-0 bg-gradient-to-r from-success to-success-glow rounded-full transition-all duration-1000 ease-out"
              style={{ width: `${progressPercentage}%` }}
            />
          </div>
          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <span>₹0</span>
            <span>₹{yearlyGoal.toLocaleString()}</span>
          </div>
        </div>

        {/* Achievement Badges */}
        <div className="space-y-3">
          <div className="flex items-center gap-2 text-sm font-medium">
            <Trophy className="w-4 h-4 text-warning" />
            Achievements
          </div>
          <div className="flex flex-wrap gap-2">
            {badges.map((badge, index) => (
              <Badge
                key={index}
                variant={badge.earned ? "default" : "outline"}
                className={`transition-all duration-300 ${
                  badge.earned 
                    ? 'bg-success text-success-foreground animate-pulse' 
                    : 'opacity-50'
                }`}
              >
                {badge.label} {badge.earned && '🏆'}
              </Badge>
            ))}
          </div>
        </div>

        {/* Quick Tip */}
        <div className="p-3 rounded-lg bg-muted/50 border">
          <div className="flex items-start gap-2">
            <Target className="w-4 h-4 text-primary mt-0.5" />
            <div>
              <p className="text-sm font-medium">Quick Tip</p>
              <p className="text-xs text-muted-foreground">
                Order during off-peak hours (2-5 PM) for better delivery deals!
              </p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default SavingsTracker;