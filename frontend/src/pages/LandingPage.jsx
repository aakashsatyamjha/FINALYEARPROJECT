import React from 'react';
import { Barcode, FileText, ShieldCheck, ArrowRight, CheckCircle2 } from 'lucide-react';
import Navbar from '../components/Navbar';
import { useAuth } from '../context/AuthContext';

export default function LandingPage({ onScanProduct, onUploadIngredients, onSignIn, onOpenDashboard }) {
  const { isAuthenticated, user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-white text-gray-900 font-sans flex flex-col justify-between">
      
      {/* Simple Header Navbar */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-blue-600" />
            <span className="text-lg font-bold text-gray-900 tracking-tight">FoodGuard</span>
          </div>

          <nav className="flex items-center gap-6 text-sm font-medium text-gray-600">
            <a href="#about-section" className="hover:text-blue-600 transition-colors">About</a>
            {isAuthenticated ? (
              <button 
                onClick={onOpenDashboard}
                className="px-3.5 py-1.5 rounded-md bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs transition-colors"
              >
                Dashboard
              </button>
            ) : (
              <button 
                onClick={onSignIn}
                className="px-3.5 py-1.5 rounded-md bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs transition-colors"
              >
                Login
              </button>
            )}
          </nav>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-4xl mx-auto px-4 sm:px-6 py-12 md:py-16 space-y-16">
        
        {/* ── 1. Hero Section ── */}
        <section className="text-center space-y-6 max-w-2xl mx-auto">
          <div className="space-y-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-blue-600 bg-blue-50 px-2.5 py-1 rounded border border-blue-100">
              College Capstone Project
            </span>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
              FoodGuard
            </h1>
            <p className="text-lg font-semibold text-gray-700">
              Packaged Food Safety & Regulatory Assessment
            </p>
          </div>

          <p className="text-sm text-gray-600 leading-relaxed max-w-lg mx-auto">
            Scan packaged food products for ingredient details, regulatory compliance (FSSAI, FDA, EFSA), and potential health risks.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
            <button
              onClick={onScanProduct}
              className="w-full sm:w-auto px-6 py-2.5 rounded-md bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors flex items-center justify-center gap-2 cursor-pointer"
            >
              <Barcode className="w-4 h-4" />
              <span>Scan Barcode</span>
            </button>

            <button
              onClick={onUploadIngredients}
              className="w-full sm:w-auto px-6 py-2.5 rounded-md bg-gray-100 hover:bg-gray-200 border border-gray-300 text-gray-800 font-medium text-sm transition-colors flex items-center justify-center gap-2 cursor-pointer"
            >
              <FileText className="w-4 h-4 text-gray-600" />
              <span>Upload Ingredients</span>
            </button>
          </div>
        </section>

        {/* ── 2. Three Simple Features ── */}
        <section id="about-section" className="space-y-4 pt-4 border-t border-gray-100">
          <h2 className="text-center text-xs font-bold uppercase tracking-wider text-gray-400">
            System Modules
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            {/* Module 1 */}
            <div className="p-5 rounded-lg bg-white border border-gray-200 space-y-2">
              <div className="w-8 h-8 rounded bg-blue-50 text-blue-600 flex items-center justify-center">
                <Barcode className="w-4 h-4" />
              </div>
              <h3 className="font-bold text-base text-gray-900">Barcode Scanning</h3>
              <p className="text-xs text-gray-600 leading-relaxed">
                Scan a product barcode or enter numbers manually to identify the product and fetch nutritional information.
              </p>
            </div>

            {/* Module 2 */}
            <div className="p-5 rounded-lg bg-white border border-gray-200 space-y-2">
              <div className="w-8 h-8 rounded bg-green-50 text-green-600 flex items-center justify-center">
                <FileText className="w-4 h-4" />
              </div>
              <h3 className="font-bold text-base text-gray-900">Ingredient Analysis</h3>
              <p className="text-xs text-gray-600 leading-relaxed">
                Upload an ingredient label image. The OCR engine extracts text and parses additives, preservatives, and allergens.
              </p>
            </div>

            {/* Module 3 */}
            <div className="p-5 rounded-lg bg-white border border-gray-200 space-y-2">
              <div className="w-8 h-8 rounded bg-purple-50 text-purple-600 flex items-center justify-center">
                <ShieldCheck className="w-4 h-4" />
              </div>
              <h3 className="font-bold text-base text-gray-900">Safety Assessment</h3>
              <p className="text-xs text-gray-600 leading-relaxed">
                Check ingredients against regulatory rules (FSSAI, FDA, EFSA) to identify banned chemicals or excess limits.
              </p>
            </div>

          </div>
        </section>

      </main>

      {/* Simple Footer */}
      <footer className="border-t border-gray-200 bg-white py-6 px-4 text-center text-xs text-gray-500">
        <p>FoodGuard — Packaged Food Safety & Regulatory Assessment System (Final Year Capstone Project)</p>
      </footer>

    </div>
  );
}
