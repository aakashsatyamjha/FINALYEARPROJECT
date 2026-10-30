import React, { useState, useEffect } from 'react';
import { Barcode, FileText, ArrowRight } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const DEFAULT_RECENT_SCANS = [
  {
    barcode: "8901058921090",
    name: "Parle Coloured Candy (INS 127 Erythrosine)",
    brand: "Parle",
    date: "29/10/2026",
    risk: "High (US FDA Revoked, India OK)",
    riskBadge: "bg-red-50 text-red-700 border-red-200"
  },
  {
    barcode: "7622210817014",
    name: "Oreo Original Cookies (INS 171 Titanium Dioxide)",
    brand: "Mondelez",
    date: "29/10/2026",
    risk: "Alert (EU EFSA Banned, India/USA OK)",
    riskBadge: "bg-red-50 text-red-700 border-red-200"
  },
  {
    barcode: "8906127550010",
    name: "Natural Peanut Butter Crunch",
    brand: "Alpino",
    date: "29/10/2026",
    risk: "Low (All Countries OK)",
    riskBadge: "bg-green-50 text-green-700 border-green-200"
  },
  {
    barcode: "8901262010047",
    name: "Amul Pure Cow Ghee 1L",
    brand: "Amul",
    date: "28/10/2026",
    risk: "Low (All Countries OK)",
    riskBadge: "bg-green-50 text-green-700 border-green-200"
  }
];

export default function Home({ setActiveTab, onSelectSample }) {
  const { user } = useAuth();
  const [historyRecords, setHistoryRecords] = useState([]);

  useEffect(() => {
    fetchRecentScans();
  }, []);

  const fetchRecentScans = async () => {
    try {
      const res = await fetch('/api/history?limit=5');
      if (res.ok) {
        const data = await res.json();
        if (data && data.length > 0) {
          const formatted = data.map(item => {
            let risk = item.risk_level || 'Low';
            if (risk.toLowerCase().includes('high') || risk.toLowerCase().includes('banned')) risk = 'High';
            else if (risk.toLowerCase().includes('mod') || risk.toLowerCase().includes('cond')) risk = 'Medium';
            else risk = 'Low';

            let badge = "bg-green-50 text-green-700 border-green-200";
            if (risk === 'High') badge = "bg-red-50 text-red-700 border-red-200";
            if (risk === 'Medium') badge = "bg-amber-50 text-amber-700 border-amber-200";

            return {
              barcode: item.barcode || item.id,
              name: item.product_name || 'Packaged Product',
              brand: item.brand || 'Brand',
              date: item.created_at ? new Date(item.created_at).toLocaleDateString() : 'Recent',
              risk,
              riskBadge: badge
            };
          });
          setHistoryRecords(formatted);
          return;
        }
      }
    } catch (e) {
      console.log("Recent scans fetch:", e);
    }
    setHistoryRecords(DEFAULT_RECENT_SCANS);
  };

  const recordsToDisplay = historyRecords.length > 0 ? historyRecords : DEFAULT_RECENT_SCANS;

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      
      {/* ── Welcome Header ── */}
      <div className="space-y-1 border-b border-gray-200 pb-4">
        <h1 className="text-2xl font-bold text-gray-900">
          Welcome back, {user?.name || 'Aakash'}
        </h1>
        <p className="text-sm text-gray-600">
          What would you like to do?
        </p>
      </div>

      {/* ── Two Primary Action Buttons ── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        
        {/* Action 1: Scan Barcode */}
        <button
          onClick={() => setActiveTab('barcode')}
          className="p-6 rounded-lg bg-white border border-gray-200 hover:border-blue-500 hover:shadow-xs transition-all text-left group cursor-pointer space-y-3"
        >
          <div className="w-10 h-10 rounded bg-blue-50 text-blue-600 flex items-center justify-center">
            <Barcode className="w-5 h-5" />
          </div>
          <div>
            <h2 className="font-bold text-gray-900 text-base group-hover:text-blue-600 transition-colors">
              Scan Barcode
            </h2>
            <p className="text-xs text-gray-500 mt-1">
              Look up a product barcode to fetch nutritional and ingredient safety details.
            </p>
          </div>
          <div className="text-xs font-semibold text-blue-600 flex items-center gap-1 pt-1">
            <span>Start Barcode Scan</span>
            <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
          </div>
        </button>

        {/* Action 2: Upload Ingredient Image */}
        <button
          onClick={() => setActiveTab('ingredient')}
          className="p-6 rounded-lg bg-white border border-gray-200 hover:border-blue-500 hover:shadow-xs transition-all text-left group cursor-pointer space-y-3"
        >
          <div className="w-10 h-10 rounded bg-green-50 text-green-600 flex items-center justify-center">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <h2 className="font-bold text-gray-900 text-base group-hover:text-blue-600 transition-colors">
              Upload Ingredient Image
            </h2>
            <p className="text-xs text-gray-500 mt-1">
              Upload an image of the ingredient list to run OCR extraction & regulatory rules.
            </p>
          </div>
          <div className="text-xs font-semibold text-blue-600 flex items-center gap-1 pt-1">
            <span>Upload Label Image</span>
            <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
          </div>
        </button>

      </div>

      {/* ── Recent Assessments Table ── */}
      <div className="bg-white rounded-lg border border-gray-200 p-5 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-bold text-gray-900">
            Recent Assessments
          </h2>
          <button 
            onClick={() => setActiveTab('history')}
            className="text-xs text-blue-600 hover:underline font-medium"
          >
            View All History →
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-gray-200 text-gray-500 font-semibold bg-gray-50">
                <th className="py-2.5 px-3">Product</th>
                <th className="py-2.5 px-3">Risk Level</th>
                <th className="py-2.5 px-3">Date</th>
                <th className="py-2.5 px-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {recordsToDisplay.map((rec, i) => (
                <tr key={i} className="hover:bg-gray-50 transition-colors">
                  <td className="py-3 px-3">
                    <span className="font-semibold text-gray-900 block">{rec.name}</span>
                    <span className="text-[11px] text-gray-500 font-mono">{rec.barcode}</span>
                  </td>
                  <td className="py-3 px-3">
                    <span className={`inline-block px-2 py-0.5 rounded text-[11px] font-bold border ${rec.riskBadge}`}>
                      {rec.risk}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-gray-600">
                    {rec.date}
                  </td>
                  <td className="py-3 px-3 text-right">
                    <button
                      onClick={() => onSelectSample(rec.barcode)}
                      className="px-2.5 py-1 rounded bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium text-xs transition-colors"
                    >
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
