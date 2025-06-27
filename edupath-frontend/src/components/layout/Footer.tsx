import React from 'react';
import { Link } from 'react-router-dom';
import { GraduationCap, Heart, Github, Mail } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-50 border-t">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <div className="flex items-center justify-center w-8 h-8 bg-gradient-to-br from-blue-600 to-green-600 rounded-lg">
                <GraduationCap className="h-5 w-5 text-white" />
              </div>
              <h3 className="text-lg font-bold bg-gradient-to-r from-blue-600 to-green-600 bg-clip-text text-transparent">
                EduPath
              </h3>
            </div>
            <p className="text-gray-600 text-sm mb-4 max-w-md">
              AI-powered educational guidance system helping Cameroonian students 
              make informed decisions about their academic and career paths.
            </p>
            <div className="text-xs text-gray-500">
              Empowering students • Bridging education and employment • Building Cameroon's future
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-semibold text-gray-900 mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/" className="text-gray-600 hover:text-blue-600 transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/profile" className="text-gray-600 hover:text-blue-600 transition-colors">
                  Student Profile
                </Link>
              </li>
              <li>
                <Link to="/recommendations" className="text-gray-600 hover:text-blue-600 transition-colors">
                  Get Recommendations
                </Link>
              </li>
              <li>
                <Link to="/universities" className="text-gray-600 hover:text-blue-600 transition-colors">
                  Universities
                </Link>
              </li>
              <li>
                <Link to="/about" className="text-gray-600 hover:text-blue-600 transition-colors">
                  About EduPath
                </Link>
              </li>
            </ul>
          </div>

          {/* Education Systems */}
          <div>
            <h4 className="font-semibold text-gray-900 mb-4">Education Systems</h4>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>GCE O-Level & A-Level</li>
              <li>French System (BEPC/BAC)</li>
              <li>University Programs</li>
              <li>Career Guidance</li>
              <li>Scholarship Opportunities</li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-200 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-1 text-sm text-gray-600 mb-4 md:mb-0">
              <span>Made with</span>
              <Heart className="h-4 w-4 text-red-500 fill-current" />
              <span>for Cameroonian students</span>
            </div>

            <div className="flex items-center space-x-4">
              <div className="text-xs text-gray-500">
                © 2025 EduPath. Hackathon Demo Project.
              </div>
            </div>
          </div>

          <div className="mt-4 text-center">
            <p className="text-xs text-gray-500">
              This is a demonstration project showcasing AI-powered educational guidance for Cameroon.
              <br />
              Built with React, TypeScript, FastAPI, and Google Gemini AI.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
