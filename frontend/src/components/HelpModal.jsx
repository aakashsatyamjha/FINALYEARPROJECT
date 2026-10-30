import React from 'react';
import { 
  X, 
  HelpCircle, 
  BookOpen, 
  Barcode, 
  FileText, 
  ShieldAlert, 
  ExternalLink,
  Scale
} from 'lucide-react';

export default function HelpModal({ isOpen, onClose }) {
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
            <div className="w-9 h-9 rounded-xl bg-cyan-500/15 border border-cyan-500/30 flex items-center justify-center text-cyan-500">
              <HelpCircle className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-900">Help & User Guide</h2>
              <p className="text-xs text-slate-500">Learn how to scan barcodes, extract OCR text, and interpret risk ratings.</p>
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
        <div className="space-y-4 text-xs text-slate-700 max-h-[70vh] overflow-y-auto pr-1">
          
          <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200 space-y-1.5">
            <h3 className="font-bold text-slate-900 flex items-center gap-2">
              <Barcode className="w-4 h-4 text-emerald-500" />
              1. Barcode Scanning
            </h3>
            <p className="text-[11px] text-slate-500 leading-relaxed">
              Use your device camera to scan the EAN-13 or UPC-A barcode on any packaged food item. The system connects to the Open Food Facts API with an offline fallback catalog.
            </p>
          </div>

          <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200 space-y-1.5">
            <h3 className="font-bold text-slate-900 flex items-center gap-2">
              <FileText className="w-4 h-4 text-cyan-500" />
              2. Ingredient OCR
            </h3>
            <p className="text-[11px] text-slate-500 leading-relaxed">
              Take a snapshot of the printed ingredients list or upload a photo. Tesseract.js optical character recognition extracts the text so you can inspect, edit, and analyze it.
            </p>
          </div>

          <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200 space-y-1.5">
            <h3 className="font-bold text-slate-900 flex items-center gap-2">
              <Scale className="w-4 h-4 text-indigo-500" />
              3. FSSAI Compliance & Regulatory Insights
            </h3>
            <p className="text-[11px] text-slate-500 leading-relaxed">
              Explains why the Government of India granted an FSSAI license under the Food Safety and Standards Act (2006) and flags any prohibited dyes, trans-fat violations, or toxic additives.
            </p>
          </div>

        </div>

        {/* Footer */}
        <div className="pt-3 border-t border-slate-200 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-slate-900 text-white font-bold text-xs transition-colors shadow-xs"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
