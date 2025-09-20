import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { 
  Activity, 
  Target, 
  TrendingUp, 
  Calendar,
  Apple,
  Zap
} from 'lucide-react';

interface NutritionData {
  calories: {
    consumed: number;
    target: number;
  };
  protein: {
    consumed: number;
    target: number;
  };
  budget: {
    spent: number;
    target: number;
  };
  weeklyTrend: {
    day: string;
    calories: number;
    spending: number;
  }[];
}

const mockNutritionData: NutritionData = {
  calories: {
    consumed: 1650,
    target: 2200
  },
  protein: {
    consumed: 85,
    target: 120
  },
  budget: {
    spent: 2840,
    target: 4000
  },
  weeklyTrend: [
    { day: 'Mon', calories: 2100, spending: 450 },
    { day: 'Tue', calories: 1950, spending: 380 },
    { day: 'Wed', calories: 2200, spending: 520 },
    { day: 'Thu', calories: 1800, spending: 340 },
    { day: 'Fri', calories: 2300, spending: 590 },
    { day: 'Sat', calories: 2400, spending: 670 },
    { day: 'Sun', calories: 1650, spending: 290 }
  ]
};

const NutritionDashboard: React.FC = () => {
  const calorieProgress = (mockNutritionData.calories.consumed / mockNutritionData.calories.target) * 100;
  const proteinProgress = (mockNutritionData.protein.consumed / mockNutritionData.protein.target) * 100;
  const budgetProgress = (mockNutritionData.budget.spent / mockNutritionData.budget.target) * 100;

  return (
    <div className="w-full space-y-6">
      <div className="text-center space-y-2">
        <h3 className="text-2xl font-bold">Nutrition & Budget Dashboard</h3>
        <p className="text-muted-foreground">Track your health and spending goals</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Calories */}
        <Card className="fade-in">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Daily Calories</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {mockNutritionData.calories.consumed}
              <span className="text-sm text-muted-foreground font-normal">
                /{mockNutritionData.calories.target}
              </span>
            </div>
            <Progress value={calorieProgress} className="mt-3" />
            <p className="text-xs text-muted-foreground mt-2">
              {Math.round(calorieProgress)}% of daily goal
            </p>
          </CardContent>
        </Card>

        {/* Protein */}
        <Card className="fade-in">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Protein Intake</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {mockNutritionData.protein.consumed}g
              <span className="text-sm text-muted-foreground font-normal">
                /{mockNutritionData.protein.target}g
              </span>
            </div>
            <Progress value={proteinProgress} className="mt-3" />
            <p className="text-xs text-muted-foreground mt-2">
              {Math.round(proteinProgress)}% of daily goal
            </p>
          </CardContent>
        </Card>

        {/* Budget */}
        <Card className="fade-in">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Monthly Budget</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ₹{mockNutritionData.budget.spent}
              <span className="text-sm text-muted-foreground font-normal">
                /₹{mockNutritionData.budget.target}
              </span>
            </div>
            <Progress value={budgetProgress} className="mt-3" />
            <p className="text-xs text-muted-foreground mt-2">
              {Math.round(budgetProgress)}% of monthly budget
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Weekly Trends */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Weekly Calories Chart */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5" />
              Weekly Nutrition Trend
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {mockNutritionData.weeklyTrend.map((day, index) => (
                <div key={day.day} className="flex items-center justify-between">
                  <span className="text-sm font-medium w-12">{day.day}</span>
                  <div className="flex-1 mx-3">
                    <Progress 
                      value={(day.calories / 2500) * 100} 
                      className="h-2"
                    />
                  </div>
                  <span className="text-sm text-muted-foreground w-16 text-right">
                    {day.calories} cal
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Meal Planning */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calendar className="w-5 h-5" />
              Meal Planning
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="p-3 rounded-lg bg-muted/50 text-center">
                <Apple className="w-6 h-6 mx-auto mb-2 text-success" />
                <p className="font-medium">Breakfast</p>
                <p className="text-sm text-muted-foreground">Planned</p>
              </div>
              <div className="p-3 rounded-lg bg-muted/50 text-center">
                <Apple className="w-6 h-6 mx-auto mb-2 text-success" />
                <p className="font-medium">Lunch</p>
                <p className="text-sm text-muted-foreground">Planned</p>
              </div>
            </div>
            
            <div className="space-y-2">
              <p className="font-medium">Shopping List for Tomorrow:</p>
              <div className="flex flex-wrap gap-2">
                {['Spinach', 'Chicken', 'Quinoa', 'Greek Yogurt'].map((item) => (
                  <Badge key={item} variant="secondary" className="text-xs">
                    {item}
                  </Badge>
                ))}
              </div>
            </div>

            <div className="p-3 rounded-lg bg-success/10 border border-success/20">
              <p className="text-sm text-success font-medium">
                💡 Based on your goals, consider adding more protein-rich foods
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default NutritionDashboard;