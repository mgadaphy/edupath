import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'sonner';
import { SessionProvider } from './contexts/SessionContext';
import { ThemeProvider } from './contexts/ThemeContext';
import Layout from './components/layout/Layout';
import HomePage from './pages/HomePage';
import ProfilePage from './pages/ProfilePage';
import RecommendationsPage from './pages/RecommendationsPage';
import UniversitiesPage from './pages/UniversitiesPage';
import AboutPage from './pages/AboutPage';
import './App.css';

function App() {
  return (
    <ThemeProvider defaultTheme="light" storageKey="edupath-theme">
      <SessionProvider>
        <Router>
          <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
            <Layout>
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/profile" element={<ProfilePage />} />
                <Route path="/recommendations" element={<RecommendationsPage />} />
                <Route path="/universities" element={<UniversitiesPage />} />
                <Route path="/about" element={<AboutPage />} />
              </Routes>
            </Layout>
            <Toaster position="top-right" richColors />
          </div>
        </Router>
      </SessionProvider>
    </ThemeProvider>
  );
}

export default App;
