import React, { useState } from 'react';
import { UserCheck, Save, CheckCircle2 } from 'lucide-react';

export default function ConsumerIntelligence({ userPreferences, onSavePreferences }) {
  const [preferences, setPreferences] = useState({
    vegetarian: true,
    vegan: false,
    low_sugar: true,
    low_sodium: false,
    gluten_free: false,
    allergen_safe: true,
    low_additives: true,
    ...(userPreferences || {})
  });

  const [savedSuccess, setSavedSuccess] = useState(false);

  const handleToggle = (key) => {
    setPreferences(prev => ({ ...prev, [key]: !prev[key] }));
    setSavedSuccess(false);
  };

  const handleSave = () => {
    if (onSavePreferences) {
      onSavePreferences(preferences);
    }
    try {
      localStorage.setItem('foodguard_user_preferences', JSON.stringify(preferences));
    } catch (_) {}
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 3000);
  };

  const options = [
    { key: 'vegetarian', label: 'Vegetarian', desc: 'Flag non-vegetarian ingredients like gelatin or animal fats.' },
    { key: 'vegan', label: 'Vegan', desc: 'Flag all animal-derived ingredients including milk solids & honey.' },
    { key: 'low_sugar', label: 'Low Sugar Preference', desc: 'Warn if sugar content exceeds 5g per 100g serving.' },
    { key: 'low_sodium', label: 'Low Sodium Preference', desc: 'Warn if sodium exceeds 140mg per 100g serving.' },
    { key: 'gluten_free', label: 'Gluten-Free', desc: 'Flag wheat, barley, rye, and malt derivatives.' },
    { key: 'allergen_safe', label: 'Allergen Alerting', desc: 'Check for soy, peanuts, tree nuts, and dairy allergens.' },
    { key: 'low_additives', label: 'Minimize Artificial Additives', desc: 'Warn when synthetic food dyes or artificial preservatives are found.' },
  ];

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      
      {/* ── Page Header ── */}
      <div className="space-y-1 border-b border-gray-200 pb-3">
        <h1 className="text-xl font-bold text-gray-900 flex items-center gap-2">
          <UserCheck className="w-5 h-5 text-blue-600" />
          <span>Profile & Dietary Preferences</span>
        </h1>
        <p className="text-xs text-gray-600">
          Configure your personal safety parameters. Products will be evaluated against these rules.
        </p>
      </div>

      {savedSuccess && (
        <div className="p-3 rounded bg-green-50 border border-green-200 text-xs text-green-700 flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-green-600" />
          <span>Dietary preferences saved successfully.</span>
        </div>
      )}

      {/* ── Preferences Checklist ── */}
      <div className="bg-white border border-gray-200 rounded-lg p-5 space-y-4">
        <h2 className="text-sm font-bold text-gray-900 border-b border-gray-100 pb-2">
          Personal Health & Dietary Rules
        </h2>

        <div className="space-y-3">
          {options.map((opt) => (
            <label
              key={opt.key}
              className="flex items-start gap-3 p-3 rounded border border-gray-200 hover:bg-gray-50 cursor-pointer transition-colors"
            >
              <input
                type="checkbox"
                checked={Boolean(preferences[opt.key])}
                onChange={() => handleToggle(opt.key)}
                className="w-4 h-4 text-blue-600 rounded border-gray-300 mt-0.5 cursor-pointer"
              />
              <div className="space-y-0.5 text-xs">
                <strong className="text-gray-900 block font-semibold">{opt.label}</strong>
                <span className="text-gray-500 block">{opt.desc}</span>
              </div>
            </label>
          ))}
        </div>

        <div className="pt-3">
          <button
            onClick={handleSave}
            className="w-full sm:w-auto px-6 py-2 rounded bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs transition-colors flex items-center justify-center gap-2 cursor-pointer"
          >
            <Save className="w-4 h-4" />
            <span>Save Preferences</span>
          </button>
        </div>
      </div>

    </div>
  );
}
