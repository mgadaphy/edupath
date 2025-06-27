import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { GraduationCap, Menu, X, Globe, User } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { useSession } from '@/contexts/SessionContext';

const Header: React.FC = () => {
  const location = useLocation();
  const { language, setLanguage, sessionId, clearSession } = useSession();
  const [isOpen, setIsOpen] = useState(false);

  const navigation = [
    { name: 'Home', href: '/', current: location.pathname === '/' },
    { name: 'My Profile', href: '/profile', current: location.pathname === '/profile' },
    { name: 'Recommendations', href: '/recommendations', current: location.pathname === '/recommendations' },
    { name: 'Universities', href: '/universities', current: location.pathname === '/universities' },
    { name: 'About', href: '/about', current: location.pathname === '/about' },
  ];

  const toggleLanguage = () => {
    setLanguage(language === 'en' ? 'fr' : 'en');
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
            {/* Language Toggle */}
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleLanguage}
              className="hidden sm:flex"
              title={language === 'en' ? 'Switch to French' : 'Passer à l\'anglais'}
            >
              <Globe className="h-4 w-4" />
              <span className="ml-1 text-xs">{language.toUpperCase()}</span>
            </Button>

            {/* Session Status */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="hidden sm:flex">
                  <User className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                {sessionId ? (
                  <>
                    <DropdownMenuItem disabled>
                      Session: {sessionId.slice(0, 8)}...
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={clearSession}>
                      Clear Session
                    </DropdownMenuItem>
                  </>
                ) : (
                  <DropdownMenuItem disabled>
                    No active session
                  </DropdownMenuItem>
                )}
              </DropdownMenuContent>
            </DropdownMenu>

            {/* Mobile Menu */}
            <Sheet open={isOpen} onOpenChange={setIsOpen}>
              <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="md:hidden">
                  <Menu className="h-5 w-5" />
                </Button>
              </SheetTrigger>
              <SheetContent side="right" className="w-64">
                <div className="flex flex-col space-y-4 mt-8">
                  {navigation.map((item) => (
                    <Link
                      key={item.name}
                      to={item.href}
                      onClick={() => setIsOpen(false)}
                      className={`block px-3 py-2 rounded-md text-base font-medium transition-colors ${
                        item.current
                          ? 'bg-blue-100 text-blue-700'
                          : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
                      }`}
                    >
                      {item.name}
                    </Link>
                  ))}
                  
                  <div className="border-t pt-4">
                    <Button
                      variant="ghost"
                      onClick={toggleLanguage}
                      className="w-full justify-start"
                    >
                      <Globe className="h-4 w-4 mr-2" />
                      {language === 'en' ? 'Français' : 'English'}
                    </Button>
                    
                    {sessionId && (
                      <Button
                        variant="ghost"
                        onClick={() => {
                          clearSession();
                          setIsOpen(false);
                        }}
                        className="w-full justify-start mt-2"
                      >
                        <User className="h-4 w-4 mr-2" />
                        Clear Session
                      </Button>
                    )}
                  </div>
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
