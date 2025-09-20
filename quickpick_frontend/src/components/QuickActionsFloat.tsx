import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { ShoppingCart, RotateCcw, Package, Plus } from 'lucide-react';

interface QuickActionsFloatProps {
  onQuickOrder?: () => void;
  onReorder?: () => void;
  onTrackOrders?: () => void;
  onAddPantry?: () => void;
}

const QuickActionsFloat: React.FC<QuickActionsFloatProps> = ({
  onQuickOrder,
  onReorder,
  onTrackOrders,
  onAddPantry
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const actions = [
    { 
      icon: <ShoppingCart className="w-5 h-5" />, 
      label: 'Quick Order', 
      action: onQuickOrder,
      color: 'bg-primary hover:bg-primary/90'
    },
    { 
      icon: <RotateCcw className="w-5 h-5" />, 
      label: 'Reorder Last', 
      action: onReorder,
      color: 'bg-success hover:bg-success/90'
    },
    { 
      icon: <Package className="w-5 h-5" />, 
      label: 'Track Orders', 
      action: onTrackOrders,
      color: 'bg-warning hover:bg-warning/90'
    },
    { 
      icon: <Plus className="w-5 h-5" />, 
      label: 'Add to Pantry', 
      action: onAddPantry,
      color: 'bg-accent hover:bg-accent/90'
    }
  ];

  return (
    <>
      {/* Desktop Floating Actions */}
      <div className="hidden lg:block fixed bottom-6 right-6 z-50">
        <div className="flex flex-col gap-3">
          {actions.map((action, index) => (
            <Button
              key={index}
              onClick={action.action}
              className={`w-12 h-12 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 ${action.color}`}
              size="icon"
            >
              {action.icon}
            </Button>
          ))}
        </div>
      </div>

      {/* Mobile Bottom Bar */}
      <div className="lg:hidden fixed bottom-0 left-0 right-0 bg-card/95 backdrop-blur-sm border-t border-border z-50">
        <div className="flex items-center justify-around p-4">
          {actions.map((action, index) => (
            <Button
              key={index}
              onClick={action.action}
              variant="ghost"
              size="sm"
              className="flex flex-col gap-1 h-auto py-2"
            >
              {action.icon}
              <span className="text-xs">{action.label.split(' ')[0]}</span>
            </Button>
          ))}
        </div>
      </div>
    </>
  );
};

export default QuickActionsFloat;