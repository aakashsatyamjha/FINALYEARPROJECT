import React, { useState } from 'react';
import { ShieldCheck, Loader2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function AuthPage({ initialMode = 'login', onBackToHome, onAuthSuccess }) {
  const { login, signup } = useAuth();
  const [mode, setMode] = useState(initialMode); // 'login' | 'signup' | 'forgot'

  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccessMessage(null);

    if (mode === 'signup' && password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);

    try {
      if (mode === 'login') {
        const res = await login(email, password);
        if (res.success) {
          onAuthSuccess();
        } else {
          setError(res.message || 'Invalid email or password.');
        }
      } else if (mode === 'signup') {
        const res = await signup(fullName, email, password);
        if (res.success) {
          onAuthSuccess();
        } else {
          setError(res.message || 'Failed to create account.');
        }
      } else if (mode === 'forgot') {
        setSuccessMessage('Password reset link has been sent to your email.');
      }
    } catch (err) {
      setError(err.message || 'Authentication error.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans flex flex-col justify-between p-4">
      
      {/* Top Brand Link */}
      <div className="max-w-md mx-auto w-full pt-6 flex items-center justify-between">
        <div 
          onClick={onBackToHome}
          className="flex items-center gap-2 cursor-pointer"
        >
          <ShieldCheck className="w-5 h-5 text-blue-600" />
          <span className="text-lg font-bold text-gray-900">FoodGuard</span>
        </div>

        {onBackToHome && (
          <button 
            onClick={onBackToHome}
            className="text-xs text-gray-500 hover:text-blue-600 transition-colors"
          >
            ← Back to Home
          </button>
        )}
      </div>

      {/* Auth Card Box */}
      <main className="max-w-md mx-auto w-full bg-white border border-gray-200 rounded-lg p-6 sm:p-8 space-y-6 shadow-xs my-auto">
        
        {/* Header */}
        <div className="space-y-1">
          <h1 className="text-xl font-bold text-gray-900">
            {mode === 'login' && 'Login to your account'}
            {mode === 'signup' && 'Create Account'}
            {mode === 'forgot' && 'Reset Password'}
          </h1>
          <p className="text-xs text-gray-500">
            {mode === 'login' && 'Enter your email and password to access FoodGuard.'}
            {mode === 'signup' && 'Register to check food products and save history.'}
            {mode === 'forgot' && 'Enter your email address to reset your password.'}
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="p-3 rounded bg-red-50 border border-red-200 text-xs text-red-700">
            {error}
          </div>
        )}

        {/* Success Alert */}
        {successMessage && (
          <div className="p-3 rounded bg-green-50 border border-green-200 text-xs text-green-700">
            {successMessage}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          
          {/* Name (Signup only) */}
          {mode === 'signup' && (
            <div className="space-y-1">
              <label className="text-xs font-semibold text-gray-700 block">
                Name
              </label>
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Full Name"
                className="w-full px-3 py-2 border border-gray-300 rounded text-sm text-gray-900 focus:outline-none focus:border-blue-600"
              />
            </div>
          )}

          {/* Email */}
          <div className="space-y-1">
            <label className="text-xs font-semibold text-gray-700 block">
              Email
            </label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@example.com"
              className="w-full px-3 py-2 border border-gray-300 rounded text-sm text-gray-900 focus:outline-none focus:border-blue-600"
            />
          </div>

          {/* Password */}
          {mode !== 'forgot' && (
            <div className="space-y-1">
              <div className="flex items-center justify-between">
                <label className="text-xs font-semibold text-gray-700">
                  Password
                </label>
                {mode === 'login' && (
                  <button
                    type="button"
                    onClick={() => { setMode('forgot'); setError(null); }}
                    className="text-xs text-blue-600 hover:underline"
                  >
                    Forgot Password?
                  </button>
                )}
              </div>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                className="w-full px-3 py-2 border border-gray-300 rounded text-sm text-gray-900 focus:outline-none focus:border-blue-600"
              />
            </div>
          )}

          {/* Confirm Password */}
          {mode === 'signup' && (
            <div className="space-y-1">
              <label className="text-xs font-semibold text-gray-700 block">
                Confirm Password
              </label>
              <input
                type="password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Re-enter password"
                className="w-full px-3 py-2 border border-gray-300 rounded text-sm text-gray-900 focus:outline-none focus:border-blue-600"
              />
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 px-4 rounded bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors cursor-pointer flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Processing...</span>
              </>
            ) : (
              <span>
                {mode === 'login' && 'Login'}
                {mode === 'signup' && 'Create Account'}
                {mode === 'forgot' && 'Send Reset Link'}
              </span>
            )}
          </button>
        </form>

        {/* Footer Links */}
        <div className="pt-2 text-center text-xs text-gray-600 border-t border-gray-100">
          {mode === 'login' && (
            <p>
              Don't have an account?{' '}
              <button
                type="button"
                onClick={() => { setMode('signup'); setError(null); }}
                className="font-bold text-blue-600 hover:underline"
              >
                Sign Up
              </button>
            </p>
          )}

          {mode === 'signup' && (
            <p>
              Already have an account?{' '}
              <button
                type="button"
                onClick={() => { setMode('login'); setError(null); }}
                className="font-bold text-blue-600 hover:underline"
              >
                Login
              </button>
            </p>
          )}

          {mode === 'forgot' && (
            <p>
              Remembered password?{' '}
              <button
                type="button"
                onClick={() => { setMode('login'); setError(null); }}
                className="font-bold text-blue-600 hover:underline"
              >
                Back to Login
              </button>
            </p>
          )}
        </div>

      </main>

      {/* Footer */}
      <footer className="text-center text-xs text-gray-400 py-4">
        FoodGuard Safety & Assessment System
      </footer>

    </div>
  );
}
