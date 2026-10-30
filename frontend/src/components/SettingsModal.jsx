import React from 'react';
import { 
  X, 
  Settings, 
  Database, 
  Sun, 
  Moon, 
  Laptop, 
  Camera, 
  ShieldCheck, 
  Key, 
  CheckCircle2, 
  Cpu
} from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export default function SettingsModal({ isOpen, onClose }) {
  const { theme, setTheme } = useTheme();

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
      <div 
        className="w-full max-w-xl glass-panel rounded-3xl p-6 shadow-2xl space-y-6 relative border"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-200">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-emerald-500">
              <Settings className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-900">Platform Settings</h2>
              <p className="text-xs text-slate-500">Configure theme preferences, databases, and AI model parameters.</p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="space-y-5 text-xs text-slate-700 max-h-[70vh] overflow-y-auto pr-1">
          
          {/* Theme Settings */}
          <div className="space-y-2">
            <span className="font-bold text-slate-900 uppercase tracking-wider text-[11px] block">
              Appearance & Theme Mode
            </span>
            <div className="grid grid-cols-3 gap-2">
              {[
                { id: 'light', label: 'Light', icon: Sun },
                { id: 'dark', label: 'Dark', icon: Moon },
                { id: 'system', label: 'System', icon: Laptop }
              ].map((t) => {
                const Icon = t.icon;
                const isSel = theme === t.id;
                return (
                  <button
                    key={t.id}
                    onClick={() => setTheme(t.id)}
                    className={`p-3 rounded-xl border flex flex-col items-center gap-2 transition-colors ${
                      isSel
                        ? 'bg-emerald-500/15 text-emerald-600 border-emerald-500/40 font-bold'
                        : 'bg-slate-100 text-slate-600 border-slate-200 hover:bg-slate-200'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span>{t.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Database Connectivity */}
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold text-slate-900 flex items-center gap-2">
                <Database className="w-4 h-4 text-emerald-500" />
                MongoDB Atlas Cloud Connection
              </span>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/15 text-emerald-600 border border-emerald-500/30 flex items-center gap-1">
                <CheckCircle2 className="w-3 h-3" />
                Connected
              </span>
            </div>
            <p className="text-[11px] text-slate-500">
              Cluster: <code className="font-mono text-slate-700">cluster0.nq0foyh.mongodb.net</code> • Database: <code className="font-mono text-slate-700">food_quality_db</code>
            </p>
          </div>

          {/* Active Model Info */}
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold text-slate-900 flex items-center gap-2">
                <Cpu className="w-4 h-4 text-indigo-500" />
                Production Classifier
              </span>
              <span className="font-mono text-[11px] font-bold text-slate-900">
                Gradient Boosting (99.86% F1)
              </span>
            </div>
            <p className="text-[11px] text-slate-500">
              Evaluates 11 biochemical feature vectors with explainable score attribution.
            </p>
          </div>

        </div>

        {/* Footer */}
        <div className="pt-3 border-t border-slate-200 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold text-xs transition-colors shadow-xs"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
}
