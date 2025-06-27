import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { toast } from 'sonner';

interface SessionContextType {
  sessionId: string | null;
  language: 'en' | 'fr';
  isSessionActive: boolean;
  createSession: (language?: 'en' | 'fr') => Promise<string>;
  clearSession: () => void;
  setLanguage: (language: 'en' | 'fr') => void;
}

const SessionContext = createContext<SessionContextType | undefined>(undefined);

interface SessionProviderProps {
  children: ReactNode;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export function SessionProvider({ children }: SessionProviderProps) {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [language, setLanguageState] = useState<'en' | 'fr'>('en');
  const [isSessionActive, setIsSessionActive] = useState(false);

  // Load session from localStorage on mount
  useEffect(() => {
    const savedSessionId = localStorage.getItem('edupath-session-id');
    const savedLanguage = localStorage.getItem('edupath-language') as 'en' | 'fr' | null;
    
    if (savedSessionId) {
      setSessionId(savedSessionId);
      setIsSessionActive(true);
    }
    
    if (savedLanguage) {
      setLanguageState(savedLanguage);
    }
  }, []);

  const createSession = async (selectedLanguage: 'en' | 'fr' = 'en'): Promise<string> => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          language_preference: selectedLanguage,
          user_agent: navigator.userAgent,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to create session');
      }

      const data = await response.json();
      const newSessionId = data.session_id;

      setSessionId(newSessionId);
      setLanguageState(selectedLanguage);
      setIsSessionActive(true);

      // Save to localStorage
      localStorage.setItem('edupath-session-id', newSessionId);
      localStorage.setItem('edupath-language', selectedLanguage);

      toast.success('Session created successfully!');
      return newSessionId;
    } catch (error) {
      console.error('Failed to create session:', error);
      toast.error('Failed to create session. Please try again.');
      throw error;
    }
  };

  const clearSession = () => {
    setSessionId(null);
    setIsSessionActive(false);
    localStorage.removeItem('edupath-session-id');
    localStorage.removeItem('edupath-language');
    toast.info('Session cleared');
  };

  const setLanguage = (newLanguage: 'en' | 'fr') => {
    setLanguageState(newLanguage);
    localStorage.setItem('edupath-language', newLanguage);
  };

  const value: SessionContextType = {
    sessionId,
    language,
    isSessionActive,
    createSession,
    clearSession,
    setLanguage,
  };

  return (
    <SessionContext.Provider value={value}>
      {children}
    </SessionContext.Provider>
  );
}

export function useSession() {
  const context = useContext(SessionContext);
  if (context === undefined) {
    throw new Error('useSession must be used within a SessionProvider');
  }
  return context;
}
