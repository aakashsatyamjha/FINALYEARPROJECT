import React, { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import Chatbot from './components/Chatbot';

import LandingPage from './pages/LandingPage';
import AuthPage from './pages/AuthPage';
import Home from './pages/Home';
import BarcodeScanner from './pages/BarcodeScanner';
import ProductAnalysis from './pages/ProductAnalysis';
import ScanHistory from './pages/ScanHistory';
import ConsumerIntelligence from './pages/ConsumerIntelligence';

function AppContent() {
  const { isAuthenticated, logout } = useAuth();

  // Navigation View: 'landing' | 'auth' | 'app'
  const [currentView, setCurrentView] = useState(() => {
    try {
      const saved = sessionStorage.getItem('foodguard_current_view');
      if (saved) return saved;
      return 'landing';
    } catch {
      return 'landing';
    }
  });

  const [authInitialMode, setAuthInitialMode] = useState('login');

  // Active Tab inside Authenticated App: 'home' | 'barcode' | 'ingredient' | 'analysis' | 'history' | 'consumer'
  const [activeTab, setActiveTab] = useState('home');
  const [currentAnalysis, setCurrentAnalysis] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    try {
      sessionStorage.setItem('foodguard_current_view', currentView);
    } catch (e) {}
  }, [currentView]);

  const safeFetchWithTimeout = async (url, options = {}, timeoutMs = 25000) => {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const response = await fetch(url, { ...options, signal: controller.signal });
      clearTimeout(timer);
      return response;
    } catch (err) {
      clearTimeout(timer);
      if (err.name === 'AbortError') {
        throw new Error('Network request timed out. Please check your connection or backend server.');
      }
      throw err;
    }
  };

  const handleBarcodeScan = async (barcode) => {
    setLoading(true);
    setError(null);
    try {
      const res = await safeFetchWithTimeout(`/api/barcode/${barcode}?country=IN`);
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || `Product with barcode ${barcode} could not be retrieved.`);
      }
      const data = await res.json();
      setCurrentAnalysis(data);
      setActiveTab('analysis');
      setCurrentView('app');
    } catch (err) {
      console.error(err);
      setError(err.message || 'Error occurred while scanning barcode.');
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeIngredients = async (ingredientsText, productName = "Custom Food Product") => {
    setLoading(true);
    setError(null);
    try {
      const res = await safeFetchWithTimeout('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_name: productName,
          ingredients: ingredientsText,
          selected_country: 'IN',
          category: 'Packaged Food'
        })
      });
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Ingredient evaluation could not be completed.');
      }
      const data = await res.json();
      setCurrentAnalysis(data);
      setActiveTab('analysis');
      setCurrentView('app');
    } catch (err) {
      console.error(err);
      setError(err.message || 'Error occurred while evaluating ingredients.');
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = async (file) => {
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      if (file) formData.append('file', file);
      
      const res = await safeFetchWithTimeout('/api/ocr/analyze', {
        method: 'POST',
        body: formData
      }, 35000); // Allow 35s for deep image OCR
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Image OCR analysis could not be completed.');
      }
      const data = await res.json();
      setCurrentAnalysis(data);
      setActiveTab('analysis');
      setCurrentView('app');
    } catch (err) {
      console.error(err);
      setError(err.message || 'Error occurred during image OCR processing.');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectHistoryRecord = async (recordId) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/history/${recordId}`);
      if (res.ok) {
        const data = await res.json();
        setCurrentAnalysis(data);
        setActiveTab('analysis');
        setCurrentView('app');
      }
    } catch (err) {
      console.error("Failed to load history record:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    setCurrentView('landing');
  };

  // 1. Authentication View
  if (!isAuthenticated && currentView === 'auth') {
    return (
      <AuthPage
        initialMode={authInitialMode}
        onBackToHome={() => setCurrentView('landing')}
        onAuthSuccess={() => {
          setActiveTab('home');
          setCurrentView('app');
        }}
      />
    );
  }

  // 2. Landing Page View for non-authenticated users
  if (!isAuthenticated) {
    return (
      <LandingPage
        onScanProduct={() => {
          setAuthInitialMode('login');
          setCurrentView('auth');
        }}
        onUploadIngredients={() => {
          setAuthInitialMode('login');
          setCurrentView('auth');
        }}
        onSignIn={() => {
          setAuthInitialMode('login');
          setCurrentView('auth');
        }}
        onOpenDashboard={() => {
          setCurrentView('app');
          setActiveTab('home');
        }}
      />
    );
  }

  // 3. Authenticated App View
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans flex flex-col justify-between">
      
      {/* Navbar */}
      <Navbar
        currentView={currentView}
        setCurrentView={setCurrentView}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        isAuthenticated={isAuthenticated}
        onLogout={handleLogout}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-5xl w-full mx-auto p-4 sm:p-6 my-4">
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded text-xs text-red-900 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="font-bold text-red-700">Notice:</span>
              <span>{error}</span>
            </div>
            <button
              onClick={() => setError(null)}
              className="text-red-700 hover:text-red-900 font-bold px-2 py-0.5 rounded cursor-pointer"
            >
              ✕
            </button>
          </div>
        )}

        {activeTab === 'home' && (
          <Home
            setActiveTab={setActiveTab}
            onSelectSample={handleBarcodeScan}
          />
        )}

        {(activeTab === 'barcode' || activeTab === 'ingredient') && (
          <BarcodeScanner
            onScanSuccess={handleBarcodeScan}
            onAnalyzeIngredients={handleAnalyzeIngredients}
            onAnalyzeImage={handleImageUpload}
            loading={loading}
            error={error}
          />
        )}

        {activeTab === 'analysis' && (
          <ProductAnalysis
            data={currentAnalysis}
            onReset={() => {
              setCurrentAnalysis(null);
              setActiveTab('barcode');
            }}
          />
        )}

        {activeTab === 'history' && (
          <ScanHistory
            onSelectRecord={handleSelectHistoryRecord}
          />
        )}

        {activeTab === 'consumer' && (
          <ConsumerIntelligence
            onTestScan={handleBarcodeScan}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white py-4 px-6 text-center text-xs text-gray-500">
        FoodGuard — Packaged Food Safety & Regulatory Assessment System (Capstone Project)
      </footer>

      {/* Floating Chatbot Assistant */}
      <Chatbot />

    </div>
  );
}

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4 font-sans text-gray-900">
          <div className="bg-white border border-gray-200 rounded-lg p-6 max-w-md w-full text-center space-y-4">
            <h2 className="text-lg font-bold text-gray-900">Something went wrong</h2>
            <p className="text-xs text-gray-600">
              A temporary camera or display error occurred. Please click below to return to the home screen.
            </p>
            <button
              onClick={() => {
                this.setState({ hasError: false });
                window.location.reload();
              }}
              className="px-4 py-2 rounded bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs cursor-pointer"
            >
              Reload Application
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

export default function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </ErrorBoundary>
  );
}
