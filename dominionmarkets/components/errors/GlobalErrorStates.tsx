import React from 'react';
import { 
  WifiOff, 
  ServerCrash, 
  Clock, 
  ShieldAlert, 
  AlertCircle,
  RefreshCw 
} from 'lucide-react';

// ============================================================================
// BASE ERROR STATE COMPONENT
// ============================================================================

interface ErrorStateProps {
  message: string;
  icon: React.ReactNode;
  onRetry?: () => void;
  actionLabel?: string;
  className?: string;
}

function ErrorState({ 
  message, 
  icon, 
  onRetry, 
  actionLabel = "Retry",
  className = "" 
}: ErrorStateProps) {
  return (
    <div className={`flex flex-col items-center justify-center p-8 text-center ${className}`}>
      <div className="mb-4 text-sovereign-slate-400">
        {icon}
      </div>
      <p className="text-base text-sovereign-slate-300 mb-4 max-w-md">
        {message}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 bg-sovereign-gold text-sovereign-obsidian rounded-lg hover:bg-sovereign-gold-hover transition-colors font-medium flex items-center gap-2"
        >
          <RefreshCw className="w-4 h-4" />
          {actionLabel}
        </button>
      )}
    </div>
  );
}

// ============================================================================
// GLOBAL ERROR STATES
// ============================================================================

/**
 * Network Error
 * When: Fetch requests fail with network error
 * Message: "Unable to connect — check your connection."
 */
export function NetworkError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ErrorState
      message="Unable to connect — check your connection."
      icon={<WifiOff className="w-12 h-12" />}
      onRetry={onRetry}
    />
  );
}

/**
 * Server Error
 * When: 500, 502, 503 status codes
 * Message: "Something went wrong — try again later."
 */
export function ServerError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ErrorState
      message="Something went wrong — try again later."
      icon={<ServerCrash className="w-12 h-12" />}
      onRetry={onRetry}
    />
  );
}

/**
 * Timeout Error
 * When: Request exceeds timeout threshold (30s)
 * Message: "This is taking longer than expected — retry."
 */
export function TimeoutError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ErrorState
      message="This is taking longer than expected — retry."
      icon={<Clock className="w-12 h-12" />}
      onRetry={onRetry}
    />
  );
}

/**
 * Authentication Error
 * When: 401 status code, expired JWT
 * Message: "Your session expired — please log in again."
 */
export function AuthenticationError({ onLogin }: { onLogin?: () => void }) {
  return (
    <ErrorState
      message="Your session expired — please log in again."
      icon={<ShieldAlert className="w-12 h-12" />}
      onRetry={onLogin}
      actionLabel="Log In"
    />
  );
}

/**
 * Data Load Failure
 * When: Generic data fetch failures
 * Message: "Unable to load data — retry."
 */
export function DataLoadError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ErrorState
      message="Unable to load data — retry."
      icon={<AlertCircle className="w-12 h-12" />}
      onRetry={onRetry}
    />
  );
}

// ============================================================================
// ERROR STATE DETECTOR (Utility)
// ============================================================================

interface ErrorResponse {
  status?: number;
  message?: string;
  type?: 'network' | 'timeout' | 'server' | 'auth' | 'generic';
}

/**
 * Determines which error component to show based on error response
 */
export function detectErrorType(error: ErrorResponse): React.ComponentType<any> {
  // Network errors (no connection)
  if (error.type === 'network' || error.message?.includes('network')) {
    return NetworkError;
  }

  // Timeout errors
  if (error.type === 'timeout' || error.message?.includes('timeout')) {
    return TimeoutError;
  }

  // Authentication errors (401)
  if (error.status === 401 || error.type === 'auth') {
    return AuthenticationError;
  }

  // Server errors (5xx)
  if (error.status && error.status >= 500) {
    return ServerError;
  }

  // Default to generic data load error
  return DataLoadError;
}

// ============================================================================
// SMART ERROR BOUNDARY COMPONENT
// ============================================================================

interface SmartErrorBoundaryProps {
  error: ErrorResponse | null;
  onRetry?: () => void;
  onLogin?: () => void;
  children: React.ReactNode;
}

/**
 * Automatically shows the right error component based on error type
 */
export function SmartErrorBoundary({ 
  error, 
  onRetry, 
  onLogin,
  children 
}: SmartErrorBoundaryProps) {
  if (!error) {
    return <>{children}</>;
  }

  const ErrorComponent = detectErrorType(error);

  // Special handling for auth errors
  if (ErrorComponent === AuthenticationError) {
    return <AuthenticationError onLogin={onLogin || onRetry} />;
  }

  return <ErrorComponent onRetry={onRetry} />;
}

// ============================================================================
// COMPACT ERROR STATE (for small widgets)
// ============================================================================

interface CompactErrorProps {
  message: string;
  onRetry?: () => void;
}

/**
 * Smaller error state for widget-sized components
 */
export function CompactError({ message, onRetry }: CompactErrorProps) {
  return (
    <div className="flex items-center justify-between p-4 bg-sovereign-obsidian/50 rounded-lg border border-sovereign-slate-700">
      <div className="flex items-center gap-3">
        <AlertCircle className="w-5 h-5 text-sovereign-slate-400" />
        <span className="text-sm text-sovereign-slate-300">{message}</span>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="text-xs text-sovereign-gold hover:text-sovereign-gold-hover font-medium"
        >
          Retry
        </button>
      )}
    </div>
  );
}

// ============================================================================
// INLINE ERROR STATE (for form fields)
// ============================================================================

interface InlineErrorProps {
  message: string;
  className?: string;
}

/**
 * Inline error message for form validation
 */
export function InlineError({ message, className = "" }: InlineErrorProps) {
  return (
    <div className={`flex items-center gap-2 mt-1 ${className}`}>
      <AlertCircle className="w-4 h-4 text-red-400" />
      <span className="text-sm text-red-400">{message}</span>
    </div>
  );
}

// ============================================================================
// USAGE EXAMPLES
// ============================================================================

/**
 * Example: Dashboard widget with error handling
 * 
 * function MarketTickerWidget() {
 *   const { data, error, refetch } = useQuery('/api/markets/ticker');
 *   
 *   if (error) {
 *     return <SmartErrorBoundary error={error} onRetry={refetch} />;
 *   }
 *   
 *   return <div>{data.ticker}</div>;
 * }
 */

/**
 * Example: Compact error in small widget
 * 
 * function PortfolioSummary() {
 *   const { data, error, refetch } = useQuery('/api/portfolio/summary');
 *   
 *   if (error) {
 *     return <CompactError message="Unable to load portfolio" onRetry={refetch} />;
 *   }
 *   
 *   return <div>{data.value}</div>;
 * }
 */

/**
 * Example: Inline form error
 * 
 * function LoginForm() {
 *   const [emailError, setEmailError] = useState('');
 *   
 *   return (
 *     <div>
 *       <input type="email" />
 *       {emailError && <InlineError message={emailError} />}
 *     </div>
 *   );
 * }
 */
