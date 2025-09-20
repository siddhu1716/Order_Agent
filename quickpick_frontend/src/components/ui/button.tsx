import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90 transition-smooth",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90 transition-smooth",
        outline: "border border-input bg-card hover:bg-card-hover hover:text-accent-foreground transition-smooth",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80 transition-smooth",
        ghost: "hover:bg-accent hover:text-accent-foreground transition-smooth",
        link: "text-primary underline-offset-4 hover:underline transition-smooth",
        
        // Voice Interface Variants
        voice: "bg-voice-idle text-white hover:bg-voice-idle/90 shadow-voice transition-smooth voice-pulse",
        "voice-listening": "bg-voice-listening text-white shadow-voice transition-smooth voice-pulse",
        "voice-processing": "bg-voice-processing text-voice-processing-foreground transition-smooth voice-processing",
        "voice-success": "bg-voice-success text-white shadow-success transition-smooth success-bounce",
        "voice-error": "bg-voice-error text-white hover:bg-voice-error/90 transition-smooth",
        
        // Success & Action Variants
        success: "bg-gradient-success text-success-foreground hover:shadow-success transition-smooth",
        warning: "bg-warning text-warning-foreground hover:bg-warning/90 transition-smooth",
        
        // Hero & Premium Variants
        hero: "bg-gradient-hero text-white hover:shadow-xl transition-smooth",
        premium: "bg-gradient-primary text-white hover:shadow-xl transition-smooth",
        
        // Platform Specific
        platform: "bg-card hover:bg-card-hover border border-border hover:border-primary/20 hover:shadow-lg transition-smooth",
        "platform-selected": "bg-gradient-success text-success-foreground border-2 border-success shadow-success transition-smooth",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3 text-sm",
        lg: "h-11 rounded-md px-8 text-base",
        xl: "h-14 rounded-lg px-10 text-lg font-semibold",
        icon: "h-10 w-10",
        "icon-lg": "h-14 w-14",
        "icon-xl": "h-20 w-20",
        voice: "h-20 w-20 rounded-full text-2xl font-bold",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return <Comp className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />;
  },
);
Button.displayName = "Button";

export { Button, buttonVariants };
