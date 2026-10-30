import React, { useState, useRef, useEffect } from 'react';
import { 
  Menu, 
  Search, 
  Bell, 
  Sun, 
  Moon, 
  Laptop, 
  CheckCircle2, 
  ChevronDown, 
  User, 
  LogOut,
  X,
  ExternalLink,
  ShieldCheck,
  Home
} from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { useAuth } from '../context/AuthContext';

export default function Header({ 
  onToggleSidebar, 
  onSearchSubmit,
  onOpenSettings,
  onOpenHelp,
  onGoToLanding
}) {
  const { theme, resolvedTheme, setTheme } = useTheme();
  const { user, logout } = useAuth();
  
  const [themeDropdownOpen, setThemeDropdownOpen] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const themeDropdownRef = useRef(null);
  const notificationsRef = useRef(null);
  const userMenuRef = useRef(null);

  // Close dropdowns on outside click
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (themeDropdownRef.current && !themeDropdownRef.current.contains(event.target)) {
        setThemeDropdownOpen(false);
      }
      if (notificationsRef.current && !notificationsRef.current.contains(event.target)) {
        setNotificationsOpen(false);
      }
      if (userMenuRef.current && !userMenuRef.current.contains(event.target)) {
        setUserMenuOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSearchKey = (e) => {
    if (e.key === 'Enter' && searchQuery.trim()) {
      onSearchSubmit(searchQuery.trim());
      setSearchQuery('');
    }
  };

  const notifications = [
    {
      id: 1,
      type: 'danger',
      title: 'High-risk adulterant detected in Spice Mix Powder',
      time: '2 min ago'
    },
    {
      id: 2,
      type: 'success',
      title: 'FSSAI 2025 compliance audit completed',
      time: '18 min ago'
    },
    {
      id: 3,
      type: 'info',
      title: 'New product verified: Britannia Milk Bikis',
      time: '45 min ago'
    },
    {
      id: 4,
      type: 'warning',
      title: 'Ingredient OCR completed for 1 packaging image',
      time: '1 hr ago'
    }
  ];

  return (
    <header className="sticky top-0 z-30 h-16 glass-panel border-b px-4 sm:px-6 lg:px-8 flex items-center justify-between gap-4 transition-colors">
      
      {/* Left: Mobile menu button & Search */}
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleSidebar}
          className="p-2 rounded-xl text-slate-600 hover:bg-slate-100 transition-colors lg:hidden cursor-pointer"
          aria-label="Toggle Navigation Drawer"
        >
          <Menu className="w-5 h-5" />
        </button>

        {/* Search Bar with Ctrl+K */}
        <div className="relative w-48 sm:w-72 md:w-96">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={handleSearchKey}
            placeholder="Search products, scans, ingredients..."
            className="w-full pl-9 pr-12 py-1.5 rounded-xl bg-slate-100 border border-slate-200 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all"
          />
          <kbd className="hidden sm:inline-block absolute right-2.5 top-1/2 -translate-y-1/2 text-[10px] font-mono text-slate-400 bg-white px-1.5 py-0.5 rounded border border-slate-200">
            Ctrl+K
          </kbd>
        </div>
      </div>

      {/* Right Actions Toolbar */}
      <div className="flex items-center gap-2 sm:gap-3">
        
        {/* Public Homepage Link */}
        {onGoToLanding && (
          <button
            onClick={onGoToLanding}
            className="hidden lg:flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100 transition-colors cursor-pointer"
            title="View Public Homepage"
          >
            <Home className="w-3.5 h-3.5 text-emerald-500" />
            <span>Public Site</span>
          </button>
        )}

        {/* FSSAI Status Pill */}
        <div className="hidden md:inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/25 text-emerald-600 text-xs font-semibold">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>FSSAI 2025 Rules Active</span>
        </div>

        {/* Notifications Dropdown */}
        <div className="relative" ref={notificationsRef}>
          <button
            onClick={() => setNotificationsOpen(!notificationsOpen)}
            className="relative p-2 rounded-xl text-slate-600 hover:bg-slate-100 border border-slate-200/80 transition-colors cursor-pointer"
            title="Notifications"
          >
            <Bell className="w-4 h-4" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-emerald-500 rounded-full"></span>
          </button>

          {notificationsOpen && (
            <div className="absolute right-0 mt-2 w-80 sm:w-96 rounded-2xl glass-panel p-4 shadow-xl space-y-3 z-50">
              <div className="flex items-center justify-between pb-2 border-b border-slate-200">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-slate-900">Recent Activity & Alerts</span>
                  <span className="text-[10px] px-1.5 py-0.2 rounded-full bg-emerald-500 text-slate-950 font-bold">4</span>
                </div>
                <button 
                  onClick={() => setNotificationsOpen(false)}
                  className="text-slate-400 hover:text-slate-600 cursor-pointer"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
                {notifications.map((n) => (
                  <div 
                    key={n.id}
                    className={`p-2.5 rounded-xl border text-xs space-y-1 transition-colors ${
                      n.type === 'danger' 
                        ? 'bg-rose-500/10 border-rose-500/25 text-rose-300'
                        : n.type === 'success'
                        ? 'bg-emerald-500/10 border-emerald-500/25 text-emerald-300'
                        : 'bg-slate-100/70 border-slate-200 text-slate-600'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <span className="font-semibold text-slate-900 leading-tight">{n.title}</span>
                    </div>
                    <span className="text-[10px] text-slate-400">{n.time}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Theme Switcher Dropdown */}
        <div className="relative" ref={themeDropdownRef}>
          <button
            onClick={() => setThemeDropdownOpen(!themeDropdownOpen)}
            className="flex items-center gap-1.5 p-2 rounded-xl text-slate-600 hover:bg-slate-100 border border-slate-200/80 transition-colors cursor-pointer"
            title={`Current theme: ${theme}`}
          >
            {resolvedTheme === 'dark' ? (
              <Moon className="w-4 h-4 text-cyan-400" />
            ) : (
              <Sun className="w-4 h-4 text-amber-500" />
            )}
            <ChevronDown className="w-3 h-3 opacity-60" />
          </button>

          {themeDropdownOpen && (
            <div className="absolute right-0 mt-2 w-40 rounded-2xl glass-panel p-1.5 shadow-xl space-y-1 z-50">
              <button
                onClick={() => { setTheme('light'); setThemeDropdownOpen(false); }}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-medium transition-colors cursor-pointer ${
                  theme === 'light'
                    ? 'bg-emerald-500/15 text-emerald-600 font-bold'
                    : 'text-slate-600 hover:bg-slate-100'
                }`}
              >
                <div className="flex items-center gap-2">
                  <Sun className="w-3.5 h-3.5 text-amber-500" />
                  <span>Light</span>
                </div>
                {theme === 'light' && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />}
              </button>

              <button
                onClick={() => { setTheme('dark'); setThemeDropdownOpen(false); }}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-medium transition-colors cursor-pointer ${
                  theme === 'dark'
                    ? 'bg-emerald-500/15 text-emerald-600 font-bold'
                    : 'text-slate-600 hover:bg-slate-100'
                }`}
              >
                <div className="flex items-center gap-2">
                  <Moon className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Dark</span>
                </div>
                {theme === 'dark' && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />}
              </button>

              <button
                onClick={() => { setTheme('system'); setThemeDropdownOpen(false); }}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-medium transition-colors cursor-pointer ${
                  theme === 'system'
                    ? 'bg-emerald-500/15 text-emerald-600 font-bold'
                    : 'text-slate-600 hover:bg-slate-100'
                }`}
              >
                <div className="flex items-center gap-2">
                  <Laptop className="w-3.5 h-3.5 text-indigo-400" />
                  <span>System</span>
                </div>
                {theme === 'system' && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />}
              </button>
            </div>
          )}
        </div>

        {/* User Profile Pill */}
        <div className="relative" ref={userMenuRef}>
          <button
            onClick={() => setUserMenuOpen(!userMenuOpen)}
            className="flex items-center gap-2 p-1.5 sm:px-2.5 sm:py-1 rounded-xl hover:bg-slate-100 border border-slate-200/80 transition-colors cursor-pointer"
          >
            <div className="w-7 h-7 rounded-lg bg-gradient-to-tr from-emerald-500 to-teal-400 text-slate-950 font-extrabold text-xs flex items-center justify-center shadow-xs">
              {user?.avatar || 'AS'}
            </div>
            <div className="hidden sm:flex flex-col text-left">
              <span className="text-xs font-bold text-slate-900 leading-tight">
                {user?.name || 'Aakash S.'}
              </span>
              <span className="text-[10px] text-slate-500 leading-none">
                {user?.role || 'Admin'}
              </span>
            </div>
            <ChevronDown className="w-3 h-3 text-slate-400 hidden sm:block" />
          </button>

          {userMenuOpen && (
            <div className="absolute right-0 mt-2 w-52 rounded-2xl glass-panel p-2 shadow-xl space-y-1 z-50">
              <div className="px-3 py-2 border-b border-slate-200">
                <p className="text-xs font-bold text-slate-900">{user?.name || 'Aakash S.'}</p>
                <p className="text-[11px] text-slate-500 truncate">{user?.email || 'akash@foodguard.ai'}</p>
              </div>

              {onGoToLanding && (
                <button
                  onClick={() => { onGoToLanding(); setUserMenuOpen(false); }}
                  className="w-full flex items-center gap-2 px-3 py-2 rounded-xl text-xs text-slate-600 hover:bg-slate-100 transition-colors text-left cursor-pointer"
                >
                  <Home className="w-3.5 h-3.5 text-emerald-500" />
                  <span>Public Landing Page</span>
                </button>
              )}

              <button
                onClick={() => { onOpenSettings(); setUserMenuOpen(false); }}
                className="w-full flex items-center gap-2 px-3 py-2 rounded-xl text-xs text-slate-600 hover:bg-slate-100 transition-colors text-left cursor-pointer"
              >
                <User className="w-3.5 h-3.5 text-slate-400" />
                <span>Account Settings</span>
              </button>

              <button
                onClick={() => { onOpenHelp(); setUserMenuOpen(false); }}
                className="w-full flex items-center gap-2 px-3 py-2 rounded-xl text-xs text-slate-600 hover:bg-slate-100 transition-colors text-left cursor-pointer"
              >
                <ExternalLink className="w-3.5 h-3.5 text-slate-400" />
                <span>Documentation & Guide</span>
              </button>

              <div className="pt-1 border-t border-slate-200">
                <button
                  onClick={() => { logout(); setUserMenuOpen(false); }}
                  className="w-full flex items-center gap-2 px-3 py-2 rounded-xl text-xs text-rose-500 hover:bg-rose-500/10 transition-colors text-left font-semibold cursor-pointer"
                >
                  <LogOut className="w-3.5 h-3.5" />
                  <span>Log Out</span>
                </button>
              </div>
            </div>
          )}
        </div>

      </div>

    </header>
  );
}
