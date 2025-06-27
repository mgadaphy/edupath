import { useEffect } from 'react';

const ErrorLogger = () => {
  useEffect(() => {
    // Log any unhandled promise rejections
    const handleRejection = (event: PromiseRejectionEvent) => {
      console.error('Unhandled promise rejection:', event.reason);
    };

    // Log any uncaught errors
    const handleError = (event: ErrorEvent) => {
      console.error('Uncaught error:', event.error);
    };

    // Add event listeners
    window.addEventListener('unhandledrejection', handleRejection);
    window.addEventListener('error', handleError);

    // Log that the error logger is active
    console.log('ErrorLogger: Active and listening for errors');

    // Clean up event listeners on unmount
    return () => {
      window.removeEventListener('unhandledrejection', handleRejection);
      window.removeEventListener('error', handleError);
    };
  }, []);

  return null; // This component doesn't render anything
};

export default ErrorLogger;
