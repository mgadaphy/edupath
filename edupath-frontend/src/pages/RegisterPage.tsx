import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuth } from '@/contexts/AuthContext';
import { Alert, AlertDescription } from '@/components/ui/alert';

const RegisterPage: React.FC = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setIsLoading(true);

    try {
      // TODO: Replace with actual registration logic
      await register({
        email: formData.email,
        password: formData.password,
        firstName: formData.firstName,
        lastName: formData.lastName,
      });
      
      // Redirect to the page the user was trying to access, or home
      const from = (location.state as any)?.from?.pathname || '/';
      navigate(from, { replace: true });
    } catch (err) {
      const error = err as Error;
      setError(error.message || 'Failed to create an account. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">Create your account</h2>
          <p className="mt-2 text-sm text-gray-600">
            Or{' '}
            <Link to="/login" className="font-medium text-blue-600 hover:text-blue-500">
              sign in to your existing account
            </Link>
          </p>
        </div>

        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Get started</CardTitle>
            <CardDescription>Create your account to continue</CardDescription>
          </CardHeader>
          <form onSubmit={handleSubmit}>
            <CardContent className="space-y-4">
              {error && (
                <Alert variant="destructive">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="firstName">First name</Label>
                  <Input
                    id="firstName"
                    name="firstName"
                    type="text"
                    required
                    value={formData.firstName}
                    onChange={handleChange}
                    placeholder="John"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="lastName">Last name</Label>
                  <Input
                    id="lastName"
                    name="lastName"
                    type="text"
                    required
                    value={formData.lastName}
                    onChange={handleChange}
                    placeholder="Doe"
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email address</Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="you@example.com"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  name="password"
                  type="password"
                  required
                  minLength={8}
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="••••••••"
                />
                <p className="text-xs text-gray-500">
                  Must be at least 8 characters
                </p>
              </div>
              <div className="space-y-2">
                <Label htmlFor="confirmPassword">Confirm password</Label>
                <Input
                  id="confirmPassword"
                  name="confirmPassword"
                  type="password"
                  required
                  minLength={8}
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  placeholder="••••••••"
                />
              </div>
            </CardContent>
            <CardFooter className="flex flex-col space-y-4">
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? 'Creating account...' : 'Create account'}
              </Button>
              <div className="relative w-full">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-white px-2 text-gray-500">Or continue with</span>
                </div>
              </div>
              <div className="w-full">
                <Button className="w-full border border-gray-300 bg-white text-gray-700 hover:bg-gray-50" type="button" disabled={isLoading}>
                  <svg className="h-5 w-5 mr-2" viewBox="0 0 24 24" aria-hidden="true">
                    <g transform="matrix(1, 0, 0, 1, 27.009001, -39.238998)">
                      <path fill="#4285F4" d="M -3.264 51.509 C -3.264 50.719 -3.334 49.969 -3.454 49.239 L -14.754 49.239 L -14.754 53.749 L -8.28426 53.749 C -8.52426 55.229 -9.21677 56.489 -10.0802 57.329 L -10.0735 57.329 L -6.01624 60.261 L -6.00598 60.261 C -3.90298 58.268 -2.764 54.999 -2.764 51.509 C -2.764 51.039 -2.784 50.569 -2.824 50.109 C -2.864 49.559 -2.924 49.029 -3.264 48.509" />
                      <path fill="#34A853" d="M -14.754 63.239 C -11.514 63.239 -8.804 62.159 -6.715 60.261 L -10.0735 57.329 C -11.1435 58.269 -12.574 58.839 -14.114 58.839 C -16.844 58.839 -19.184 57.139 -20.064 54.659 L -24.184 54.659 L -24.214 54.749 L -24.214 57.559 C -22.114 61.459 -18.754 63.239 -14.754 63.239" />
                      <path fill="#FBBC05" d="M -20.064 54.659 C -20.404 53.629 -20.594 52.529 -20.594 51.369 C -20.594 50.209 -20.404 49.109 -20.064 48.079 L -20.064 45.269 L -24.184 45.269 C -25.334 47.579 -25.924 50.139 -25.924 52.729 C -25.924 55.319 -25.334 57.879 -24.184 60.189 L -20.064 54.659" />
                      <path fill="#EA4335" d="M -14.754 43.989 C -12.984 43.989 -11.404 44.599 -10.0735 45.789 L -6.025 42.819 C -8.494 40.569 -11.504 39.239 -14.754 39.239 C -18.754 39.239 -22.114 41.019 -24.184 44.909 L -20.064 48.079 C -19.184 45.599 -16.844 43.989 -14.754 43.989" />
                    </g>
                  </svg>
                  Google
                </Button>
              </div>
            </CardFooter>
          </form>
        </Card>
        <div className="text-center text-sm text-gray-600">
          <p>By creating an account, you agree to our <a href="#" className="font-medium text-blue-600 hover:text-blue-500">Terms of Service</a> and <a href="#" className="font-medium text-blue-600 hover:text-blue-500">Privacy Policy</a>.</p>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
