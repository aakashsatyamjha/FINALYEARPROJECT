import React, { useState } from 'react';
import { ShieldCheck, Menu, X } from 'lucide-react';

export default function Navbar({ 
  currentView, 
  setCurrentView, 
  activeTab, 
  setActiveTab, 
  isAuthenticated, 
  user, 
  onLogout 
}) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogoClick = () => {
    if (isAuthenticated) {
      setCurrentView('app');
      setActiveTab('home');
    } else {
      setCurrentView('landing');
    }
  };

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
        
        {/* Simple Text Logo */}
        <div 
          onClick={handleLogoClick}
          className="flex items-center gap-2 cursor-pointer select-none"
        >
          <ShieldCheck className="w-5 h-5 text-blue-600" />
          <span className="text-lg font-bold text-gray-900 tracking-tight">FoodGuard</span>
        </div>

        {/* Desktop Navigation Links */}
        <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-gray-600">
          {!isAuthenticated ? (
            <>
              <button 
                onClick={() => setCurrentView('landing')}
                className={`hover:text-blue-600 transition-colors ${currentView === 'landing' ? 'text-blue-600 font-semibold' : ''}`}
              >
                Home
              </button>
              <button 
                onClick={() => { setCurrentView('auth'); }}
                className="hover:text-blue-600 transition-colors"
              >
                Scan Product
              </button>
              <button 
                onClick={() => { setCurrentView('landing'); setTimeout(() => { document.getElementById('about-section')?.scrollIntoView({ behavior: 'smooth' }); }, 100); }}
                className="hover:text-blue-600 transition-colors"
              >
                About
              </button>
              <button 
                onClick={() => setCurrentView('auth')}
                className="px-3.5 py-1.5 rounded-md bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs transition-colors"
              >
                Login
              </button>
            </>
          ) : (
            <>
              <button 
                onClick={() => { setCurrentView('app'); setActiveTab('home'); }}
                className={`hover:text-blue-600 transition-colors ${activeTab === 'home' ? 'text-blue-600 font-semibold' : ''}`}
              >
                Dashboard
              </button>
              <button 
                onClick={() => { setCurrentView('app'); setActiveTab('barcode'); }}
                className={`hover:text-blue-600 transition-colors ${activeTab === 'barcode' || activeTab === 'ingredient' ? 'text-blue-600 font-semibold' : ''}`}
              >
                Scan Product
              </button>
              <button 
                onClick={() => { setCurrentView('app'); setActiveTab('history'); }}
                className={`hover:text-blue-600 transition-colors ${activeTab === 'history' ? 'text-blue-600 font-semibold' : ''}`}
              >
                History
              </button>
              <button 
                onClick={() => { setCurrentView('app'); setActiveTab('consumer'); }}
                className={`hover:text-blue-600 transition-colors ${activeTab === 'consumer' ? 'text-blue-600 font-semibold' : ''}`}
              >
                Profile
              </button>
              <button 
                onClick={onLogout}
                className="text-gray-500 hover:text-red-600 transition-colors text-xs font-semibold"
              >
                Logout
              </button>
            </>
          )}
        </nav>

        {/* Mobile menu toggle */}
        <div className="flex md:hidden">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-1.5 rounded-md text-gray-600 hover:bg-gray-100"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>

      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-gray-200 bg-white px-4 py-3 space-y-2 text-sm">
          {!isAuthenticated ? (
            <>
              <button 
                onClick={() => { setCurrentView('landing'); setMobileMenuOpen(false); }}
                className="block w-full text-left py-1 text-gray-700 hover:text-blue-600 font-medium"
              >
                Home
              </button>
              <button 
                onClick={() => { setCurrentView('auth'); setMobileMenuOpen(false); }}
                className="block w-full text-left py-1 text-gray-700 hover:text-blue-600 font-medium"
              >
                Scan Product
              </button>
              <button 
                onClick={() => { setCurrentView('auth'); setMobileMenuOpen(false); }}
                className="block w-full text-left py-1 text-blue-600 font-semibold"
              >
                Login
              </button>
            </>
          ) : (
            <>
              <button 
                onClick={() => { setCurrentView('app'); setActiveTab('home'); setMobileMenuOpen(false); }}
                className="block w-full text-left py-1 text-gray-700 hover:text-blue-600 font-medium"
              >
                Dashboard
              </button>
              <button 
                onClick={() => { setCurrentView('app'); setActiveTab('barcode'); setMobileMenuOpen(false); }}
                className="block w-full text-left py-1 text-gray-700 hover:text-blue-600 font-medium"
              >
                Scan Product
              </button>
              <button 
                onClick={() => { setCurrentView('app'); setActiveTab('history'); setMobileMenuOpen(false); }}
                className="block w-full text-left py-1 text-gray-700 hover:text-blue-600 font-medium"
              >
                History
              </button>
              <button 
                onClick={() => { setCurrentView('app'); setActiveTab('consumer'); setMobileMenuOpen(false); }}
                className="block w-full text-left py-1 text-gray-700 hover:text-blue-600 font-medium"
              >
                Profile
              </button>
              <button 
                onClick={() => { onLogout(); setMobileMenuOpen(false); }}
                className="block w-full text-left py-1 text-red-600 font-medium"
              >
                Logout
              </button>
            </>
          )}
        </div>
      )}
    </header>
  );
}
