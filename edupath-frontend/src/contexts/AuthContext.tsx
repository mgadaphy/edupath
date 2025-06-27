import React, { createContext, useContext, useState, ReactNode, useEffect, useCallback } from 'react';

export interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  // Add other user properties as needed
}

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterData extends LoginCredentials {
  firstName: string;
  lastName: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check for existing session on initial load
  const checkAuth = useCallback(async () => {
    try {
      // TODO: Implement actual session check with backend
      // For now, we'll simulate a loading state
      await new Promise(resolve => setTimeout(resolve, 1000));
      // TODO: Remove this mock user in production
      const mockUser = {
        id: '1',
        email: 'test@example.com',
        name: 'Test User',
        role: 'user',
      };
      setUser(mockUser);
    } catch (error) {
      console.error('Auth check failed:', error);
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const login = useCallback(async ({ email, password }: LoginCredentials) => {
    try {
      setIsLoading(true);
      // TODO: Implement actual login logic with backend
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const mockUser: User = {
        id: '1',
        email,
        name: 'Test User',
        role: 'user',
      };
      setUser(mockUser);
    } catch (error) {
      console.error('Login failed:', error);
      throw new Error('Failed to login. Please check your credentials and try again.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const register = useCallback(async (data: RegisterData) => {
    try {
      setIsLoading(true);
      // TODO: Implement actual registration logic with backend
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const newUser: User = {
        id: Date.now().toString(),
        email: data.email,
        name: `${data.firstName} ${data.lastName}`,
        role: 'user',
      };
      setUser(newUser);
    } catch (error) {
      console.error('Registration failed:', error);
      throw new Error('Failed to register. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      setIsLoading(true);
      // TODO: Implement actual logout logic with backend
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500));
      setUser(null);
    } catch (error) {
      console.error('Logout failed:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const value = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {!isLoading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
