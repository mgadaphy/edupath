import React from 'react';
import { AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { useNavigate } from 'react-router-dom';

export const UnauthorizedPage: React.FC = () => {
  const navigate = useNavigate();
  
  const handleGoBack = () => navigate(-1);
  const handleGoHome = () => navigate('/');

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <div className="flex items-center justify-center mb-4">
            <div className="rounded-full bg-red-100 p-3">
              <AlertCircle className="h-8 w-8 text-red-600" />
            </div>
          </div>
          <CardTitle className="text-2xl font-bold text-center">Access Denied</CardTitle>
        </CardHeader>
        <CardContent className="text-center">
          <p className="text-gray-600 mb-4">
            You don't have permission to access this page. Please contact an administrator if you believe this is an error.
          </p>
        </CardContent>
        <CardFooter className="flex flex-col space-y-3">
          <Button 
            className="w-full bg-blue-600 hover:bg-blue-700 text-white mb-2" 
            onClick={handleGoBack}
          >
            Go Back
          </Button>
          <Button 
            className="w-full border border-gray-300 bg-white text-gray-700 hover:bg-gray-50" 
            onClick={handleGoHome}
          >
            Return Home
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
};
