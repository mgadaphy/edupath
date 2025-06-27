import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'sonner';
import { SessionProvider } from '@/contexts/SessionContext';
import { ThemeProvider } from '@/contexts/ThemeContext';
import { AuthProvider } from '@/contexts/AuthContext';
import { ProtectedRoute } from '@/components/auth/ProtectedRoute';
import Layout from '@/components/layout/Layout';
import HomePage from '@/pages/HomePage';
import ProfilePage from '@/pages/ProfilePage';
import RecommendationsPage from '@/pages/RecommendationsPage';
import UniversitiesPage from '@/pages/UniversitiesPage';
import AboutPage from '@/pages/AboutPage';
import LoginPage from '@/pages/LoginPage';
import RegisterPage from '@/pages/RegisterPage';
import { UnauthorizedPage } from '@/pages/UnauthorizedPage';
import './App.css';

function App() {
  return (
    <ThemeProvider defaultTheme="light" storageKey="edupath-theme">
      <SessionProvider>
        <AuthProvider>
          <Router>
            <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
              <Layout>
                <Routes>
                  {/* Public Routes */}
                  <Route path="/" element={<HomePage />} />
                  <Route path="/universities" element={<UniversitiesPage />} />
                  <Route path="/about" element={<AboutPage />} />
                  <Route path="/login" element={<LoginPage />} />
                  <Route path="/register" element={<RegisterPage />} />
                  <Route path="/unauthorized" element={<UnauthorizedPage />} />

                  {/* Protected Routes */}
                  <Route 
                    path="/profile" 
                    element={
                      <ProtectedRoute>
                        <ProfilePage />
                      </ProtectedRoute>
                    } 
                  />
                  <Route 
                    path="/recommendations" 
                    element={
                      <ProtectedRoute>
                        <RecommendationsPage />
                      </ProtectedRoute>
                    } 
                  />

                  {/* Catch-all route - redirect to home */}
                  <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
              </Layout>
              <Toaster />
            </div>
          </Router>
        </AuthProvider>
        </SessionProvider>
      </ThemeProvider>
  );
}

export default App;
