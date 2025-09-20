import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Mic, MicOff, Loader2, Check, AlertCircle } from 'lucide-react';
import { useVoiceCommand, usePlaceQuickOrder } from '@/hooks/useQuickOrder';
import { toast } from 'sonner';

type VoiceState = 'idle' | 'listening' | 'processing' | 'success' | 'error';

interface VoiceOrderComponentProps {
  onOrderPlaced?: (items: string) => void;
}

const VoiceOrderComponent: React.FC<VoiceOrderComponentProps> = ({ onOrderPlaced }) => {
  const [voiceState, setVoiceState] = useState<VoiceState>('idle');
  const [transcription, setTranscription] = useState('');
  const [lastOrder, setLastOrder] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [waveformBars, setWaveformBars] = useState<number[]>([]);
  
  // API hooks
  const voiceCommandMutation = useVoiceCommand();
  const placeOrderMutation = usePlaceQuickOrder();

  // Animated waveform effect
  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (voiceState === 'listening') {
      interval = setInterval(() => {
        setWaveformBars(Array.from({ length: 8 }, () => Math.random() * 100));
      }, 100);
    } else {
      setWaveformBars([]);
    }
    
    return () => clearInterval(interval);
  }, [voiceState]);

  const startListening = () => {
    setVoiceState('listening');
    setTranscription('Listening...');
    setSuggestions([]);
    
    // Simulate voice recognition with AI suggestions
    setTimeout(() => {
      setSuggestions(['Tomatoes', 'Cherry Tomatoes', 'Tomato Puree']);
      setTranscription('Order tomatoes...');
    }, 1000);
    
    setTimeout(() => {
      setVoiceState('processing');
      setTranscription('Processing your order...');
      setSuggestions([]);
      
      // Process voice command through backend
      const mockOrder = 'Order tomatoes and milk';
      voiceCommandMutation.mutate(
        { message: mockOrder },
        {
          onSuccess: (data) => {
            setTranscription(`"${mockOrder}"`);
            setLastOrder(mockOrder);
            setVoiceState('success');
            
            // Show success message
            toast.success('Order processed successfully!', {
              description: `Best deal found: ${data.data.recommendation.summary}`,
            });
            
            onOrderPlaced?.(mockOrder);
            
            // Reset after success
            setTimeout(() => {
              setVoiceState('idle');
              setTranscription('');
            }, 2000);
          },
          onError: (error) => {
            setVoiceState('error');
            setTranscription('Error processing order');
            toast.error('Failed to process voice command', {
              description: 'Please try again or type your order manually.',
            });
            
            setTimeout(() => {
              setVoiceState('idle');
              setTranscription('');
            }, 2000);
          }
        }
      );
    }, 2000);
  };

  const getVoiceIcon = () => {
    switch (voiceState) {
      case 'listening':
        return <Mic className="w-8 h-8 animate-pulse" />;
      case 'processing':
        return <Loader2 className="w-8 h-8 animate-spin" />;
      case 'success':
        return <Check className="w-8 h-8 animate-bounce" />;
      case 'error':
        return <AlertCircle className="w-8 h-8 animate-shake" />;
      default:
        return <MicOff className="w-8 h-8" />;
    }
  };

  const getButtonVariant = () => {
    switch (voiceState) {
      case 'listening':
        return 'voice-listening';
      case 'processing':
        return 'voice-processing';
      case 'success':
        return 'voice-success';
      case 'error':
        return 'voice-error';
      default:
        return 'voice';
    }
  };

  const quickCommands = [
    { text: 'Repeat last order', action: () => onOrderPlaced?.(lastOrder) },
    { text: 'Reorder cheapest', action: () => onOrderPlaced?.('Cheapest items') },
    { text: 'Show my pantry', action: () => console.log('Show pantry') }
  ];

  return (
    <Card className="w-full max-w-md mx-auto slide-up hover:shadow-lg transition-all duration-300">
      <CardHeader className="text-center">
        <CardTitle className="text-2xl font-bold bg-gradient-primary bg-clip-text text-transparent">
          Quick Voice Order
        </CardTitle>
        <p className="text-muted-foreground">
          Tap the mic and say what you need
        </p>
      </CardHeader>
      <CardContent className="text-center space-y-6">
        {/* Voice Button with Waveform */}
        <div className="relative">
          <Button
            variant={getButtonVariant()}
            size="voice"
            onClick={startListening}
            disabled={voiceState !== 'idle'}
            className="mx-auto relative overflow-hidden"
          >
            {getVoiceIcon()}
          </Button>
          
          {/* Animated Waveform */}
          {voiceState === 'listening' && (
            <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 flex gap-1 items-end">
              {waveformBars.map((height, index) => (
                <div
                  key={index}
                  className="w-1 bg-primary transition-all duration-100"
                  style={{ height: `${Math.max(height * 0.3, 4)}px` }}
                />
              ))}
            </div>
          )}
        </div>

        {/* AI Suggestions Overlay */}
        {suggestions.length > 0 && (
          <div className="absolute top-0 left-0 right-0 bg-card/95 backdrop-blur-sm border rounded-lg p-3 z-10 animate-slide-down">
            <p className="text-sm font-medium mb-2">Did you mean:</p>
            <div className="flex flex-wrap gap-2">
              {suggestions.map((suggestion, index) => (
                <button
                  key={index}
                  className="px-3 py-1 bg-primary/10 hover:bg-primary/20 text-primary text-xs rounded-full transition-colors"
                  onClick={() => onOrderPlaced?.(suggestion)}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Transcription with Keywords Highlighting */}
        {transcription && (
          <div className="p-4 rounded-lg bg-muted/50 border fade-in">
            <p className="text-lg font-medium text-foreground">
              {transcription.includes('tomatoes') ? (
                <>
                  Order <span className="text-primary font-bold">tomatoes</span>...
                </>
              ) : (
                transcription
              )}
            </p>
          </div>
        )}

        {/* Quick Voice Commands */}
        <div className="space-y-3">
          <p className="text-sm text-muted-foreground">Voice Shortcuts:</p>
          <div className="grid grid-cols-1 gap-2">
            {quickCommands.map((command, index) => (
              <button
                key={index}
                onClick={command.action}
                className="px-3 py-2 text-xs bg-secondary hover:bg-secondary/80 rounded-lg transition-colors text-left"
              >
                "{command.text}"
              </button>
            ))}
          </div>
        </div>

        <div className="space-y-2">
          <p className="text-sm text-muted-foreground">Or try saying:</p>
          <div className="flex flex-wrap gap-2 justify-center">
            {['Order tomatoes', 'Get milk and bread', 'Find cheapest rice'].map((suggestion) => (
              <span
                key={suggestion}
                className="px-3 py-1 bg-secondary text-secondary-foreground text-xs rounded-full hover:bg-secondary/80 transition-colors cursor-pointer"
                onClick={() => onOrderPlaced?.(suggestion)}
              >
                "{suggestion}"
              </span>
            ))}
          </div>
        </div>

        {lastOrder && (
          <div className="p-3 rounded-lg bg-success/10 border border-success/20 animate-fade-in">
            <p className="text-sm text-success font-medium">
              Last order: {lastOrder}
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default VoiceOrderComponent;