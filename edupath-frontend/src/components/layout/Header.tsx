import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { 
  GraduationCap, 
  Menu, 
  X,
  LogIn,
  LogOut,
  UserPlus,
  Globe,
  User as UserIcon
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { useSession } from '@/contexts/SessionContext';
import { useAuth } from '@/contexts/AuthContext';

const NewHeader: React.FC = () => {
  const location = useLocation();
  const { language, setLanguage, sessionId, clearSession } = useSession();
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  // Navigation items
  const navigation = [
    { name: 'Home', href: '/', current: location.pathname === '/' },
    { name: 'Universities', href: '/universities', current: location.pathname === '/universities' },
    { name: 'About', href: '/about', current: location.pathname === '/about' },
  ];

  if (isAuthenticated) {
    navigation.unshift(
      { name: 'Dashboard', href: '/dashboard', current: location.pathname === '/dashboard' },
      { name: 'My Profile', href: '/profile', current: location.pathname === '/profile' },
      { name: 'Recommendations', href: '/recommendations', current: location.pathname === '/recommendations' }
    );
  }

  const toggleLanguage = () => {
    setLanguage(language === 'en' ? 'fr' : 'en');
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-white/80 backdrop-blur-md">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-blue-600 to-green-600 rounded-lg">
              <GraduationCap className="h-6 w-6 text-white" />
            </div>
            <div className="hidden sm:block">
              <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-green-600 bg-clip-text text-transparent">
                EduPath
              </h1>
              <p className="text-xs text-gray-500">
                {language === 'en' ? 'Your Academic Journey' : 'Votre Parcours Académique'}
              </p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-1">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                  item.current
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
                }`}
              >
                {item.name}
              </Link>
            ))}
          </nav>

          {/* Right Side Actions */}
          <div className="flex items-center space-x-2">
            {/* Language Switcher */}
            <button
              onClick={toggleLanguage}
              className="px-3 py-1 text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors"
              aria-label={language === 'en' ? 'Switch to French' : 'Switch to English'}
            >
              {language === 'en' ? 'FR' : 'EN'}
            </button>

            {/* Authentication Buttons */}
            {isAuthenticated ? (
              <div className="hidden md:flex items-center space-x-2">
                <Button 
                  variant="outline"
                  onClick={() => navigate('/profile')}
                  className="h-9 px-4 text-gray-700 border-gray-300 hover:bg-gray-50 hover:text-gray-900"
                >
                  <UserIcon className="h-4 w-4 mr-2" />
                  Profile
                </Button>
                <Button 
                  variant="outline"
                  onClick={handleLogout}
                  className="h-9 px-4 text-red-600 border-red-200 hover:bg-red-50 hover:text-red-700"
                >
                  <LogOut className="h-4 w-4 mr-2" />
                  Sign out
                </Button>
              </div>
            ) : (
              <div className="hidden md:flex items-center space-x-2">
                <Button 
                  variant="outline"
                  onClick={() => navigate('/login')}
                  className="h-9 px-4 text-gray-700 border-gray-300 hover:bg-gray-50 hover:text-gray-900"
                >
                  <LogIn className="h-4 w-4 mr-2" />
                  Sign in
                </Button>
                <Button 
                  onClick={() => navigate('/register')}
                  className="h-9 px-4 bg-blue-600 hover:bg-blue-700 text-white"
                >
                  <UserPlus className="h-4 w-4 mr-2" />
                  Sign up
                </Button>
              </div>
            )}

            {/* Mobile Menu Button */}
            <div className="md:hidden">
              <Sheet>
                <SheetTrigger asChild>
                  <Button className="h-10 w-10 p-0">
                    <Menu className="h-5 w-5" />
                  </Button>
                </SheetTrigger>
                <SheetContent side="right" className="w-64 p-0">
                  <div className="flex flex-col h-full">
                    <div className="p-4 border-b flex justify-between items-center">
                      <h3 className="text-lg font-semibold">Menu</h3>
                      <SheetTrigger asChild>
                        <Button className="h-8 w-8 p-0 hover:bg-accent hover:text-accent-foreground">
                          <X className="h-4 w-4" />
                        </Button>
                      </SheetTrigger>
                    </div>
                    <div className="flex-1 overflow-y-auto p-4">
                      <div className="flex flex-col space-y-2">
                        {navigation.map((item) => (
                          <Link
                            key={item.name}
                            to={item.href}
                            onClick={() => document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }))}
                            className={`block px-3 py-2 rounded-md text-base font-medium transition-colors ${
                              item.current
                                ? 'bg-blue-100 text-blue-700'
                                : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
                            }`}
                          >
                            {item.name}
                          </Link>
                        ))}
                      </div>
                      
                      <div className="border-t pt-4 mt-4">
                        <button
                          onClick={() => {
                            toggleLanguage();
                            document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
                          }}
                          className="w-full flex items-center px-3 py-2 text-left text-sm font-medium hover:bg-accent rounded-md"
                        >
                          <Globe className="h-4 w-4 mr-2" />
                          {language === 'en' ? 'Français' : 'English'}
                        </button>
                        
                        {sessionId && (
                          <button
                            onClick={() => {
                              clearSession();
                              document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
                            }}
                            className="w-full flex items-center px-3 py-2 text-left text-sm font-medium hover:bg-accent rounded-md mt-2"
                          >
                            <UserIcon className="h-4 w-4 mr-2" />
                            Clear Session
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                </SheetContent>
              </Sheet>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default NewHeader;
