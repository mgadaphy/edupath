import React from 'react';

const serializeError = (error: any) => {
  if (error instanceof Error) {
    return `${error.name}: ${error.message}\n${error.stack || 'No stack trace available'}`;
  }
  return JSON.stringify(error, null, 2);
};

export class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean; error: any }
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: any) {
    // Log the error to the console
    console.error('ErrorBoundary caught an error:', error);
    return { hasError: true, error };
  }

  componentDidCatch(error: any, errorInfo: any) {
    // Log the error to an error reporting service
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="fixed inset-0 bg-white p-8 flex flex-col items-center justify-center">
          <div className="max-w-2xl w-full p-6 border-2 border-red-500 rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold text-red-600 mb-4">⚠️ Application Error</h2>
            <p className="mb-4 text-gray-700">
              An unexpected error occurred. Please refresh the page or try again later.
            </p>
            <details className="bg-gray-50 p-4 rounded overflow-auto max-h-96">
              <summary className="font-medium text-gray-700 cursor-pointer mb-2">Error Details</summary>
              <pre className="mt-2 p-2 bg-black text-green-400 text-xs overflow-auto">
                {serializeError(this.state.error)}
              </pre>
            </details>
            <button
              onClick={() => window.location.reload()}
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
            >
              Reload Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}