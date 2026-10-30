import React, { useState, useEffect } from 'react';
import { 
  Globe, 
  Search, 
  Filter, 
  Scale, 
  AlertTriangle, 
  CheckCircle2, 
  XCircle, 
  HelpCircle, 
  ChevronRight, 
  ExternalLink,
  BookOpen,
  Info,
  Shield,
  Layers,
  Sparkles
} from 'lucide-react';

export default function RegulatoryIntelligence({ onSelectProductForAnalysis }) {
  const [ingredients, setIngredients] = useState([]);
  const [countries, setCountries] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedIngredient, setSelectedIngredient] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedCountryFilter, setSelectedCountryFilter] = useState('ALL');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [ingRes, countRes] = await Promise.all([
        fetch('/api/regulatory/ingredients'),
        fetch('/api/countries')
      ]);
      if (ingRes.ok) {
        const ingData = await ingRes.json();
        setIngredients(ingData);
        if (ingData.length > 0) {
          setSelectedIngredient(ingData[0]);
        }
      }
      if (countRes.ok) {
        const countData = await countRes.json();
        setCountries(countData);
      }
    } catch (err) {
      console.error("Failed to load regulatory data:", err);
    } finally {
      setLoading(false);
    }
  };

  const categories = ['All', ...new Set(ingredients.map(i => i.category))];

  const filteredIngredients = ingredients.filter(ing => {
    const matchesSearch = 
      ing.common_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ing.ins_e_number.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ing.function.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (ing.aliases && ing.aliases.some(a => a.toLowerCase().includes(searchQuery.toLowerCase())));

    const matchesCategory = selectedCategory === 'All' || ing.category === selectedCategory;

    return matchesSearch && matchesCategory;
  });

  const getStatusBadge = (statusCode, statusText) => {
    switch (statusCode) {
      case 'PERMITTED':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-emerald-500/15 text-emerald-600 border border-emerald-500/30 text-xs font-semibold">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Permitted</span>
          </span>
        );
      case 'PERMITTED_WITH_LIMITS':
      case 'PERMITTED_WITH_CONDITIONS':
      case 'RESTRICTED':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-amber-500/15 text-amber-600 border border-amber-500/30 text-xs font-semibold">
            <AlertTriangle className="w-3.5 h-3.5" />
            <span>{statusText.includes('restriction') ? 'Restricted' : 'Conditional / Limits'}</span>
          </span>
        );
      case 'NOT_PERMITTED':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-rose-500/15 text-rose-600 border border-rose-500/30 text-xs font-semibold">
            <XCircle className="w-3.5 h-3.5" />
            <span>Not Permitted / Banned</span>
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-slate-500/15 text-slate-400 border border-slate-500/30 text-xs font-semibold">
            <HelpCircle className="w-3.5 h-3.5" />
            <span>Verification Required</span>
          </span>
        );
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6 pb-12 animate-fade-in">
      
      {/* ── Page Header ── */}
      <div className="space-y-2">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 text-xs font-bold uppercase tracking-wider">
          <Globe className="w-3.5 h-3.5" />
          <span>Global Regulatory Intelligence</span>
        </div>
        <h1 className="text-2xl lg:text-3xl font-extrabold text-slate-900 tracking-tight">
          Food Additive & Substance Regulatory Knowledge Base
        </h1>
        <p className="text-sm text-slate-600 max-w-3xl">
          Search and compare verified food safety regulations, maximum permissible limits, and scientific rationale across India (FSSAI), USA (FDA), European Union (EFSA), Germany (BVL), and the UK (FSA).
        </p>
      </div>

      {/* ── Search & Filter Controls ── */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        
        {/* Search Bar */}
        <div className="md:col-span-2 relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by ingredient name, INS/E number (e.g. E171, Tartrazine, TBHQ, MSG)..."
            className="w-full pl-10 pr-4 py-2.5 rounded-xl glass-card text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 transition-all"
          />
        </div>

        {/* Category Dropdown */}
        <div className="relative">
          <Filter className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 rounded-xl glass-card text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 transition-all cursor-pointer appearance-none"
          >
            {categories.map((cat) => (
              <option key={cat} value={cat} className="bg-slate-900 text-white">
                Category: {cat}
              </option>
            ))}
          </select>
        </div>

      </div>

      {/* ── Main Explorer Grid (Split View) ── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column: Ingredient Catalog List */}
        <div className="lg:col-span-5 space-y-3">
          <div className="flex items-center justify-between px-1">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              Ingredients ({filteredIngredients.length})
            </span>
            <span className="text-[11px] text-slate-400">Click to view global profile</span>
          </div>

          <div className="space-y-2 max-h-[680px] overflow-y-auto pr-1">
            {loading ? (
              <div className="p-8 text-center text-sm text-slate-400 glass-card rounded-2xl">
                Loading regulatory database...
              </div>
            ) : filteredIngredients.length === 0 ? (
              <div className="p-8 text-center text-sm text-slate-400 glass-card rounded-2xl">
                No ingredients found matching "{searchQuery}".
              </div>
            ) : (
              filteredIngredients.map((ing) => {
                const isSelected = selectedIngredient?.id === ing.id;
                return (
                  <div
                    key={ing.id}
                    onClick={() => setSelectedIngredient(ing)}
                    className={`
                      p-3.5 rounded-xl transition-all cursor-pointer border text-left
                      ${isSelected 
                        ? 'bg-emerald-500/15 border-emerald-500/40 shadow-sm' 
                        : 'glass-card hover:bg-slate-100 border-slate-200/60'
                      }
                    `}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-bold text-slate-900">
                            {ing.common_name}
                          </span>
                          <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-200 text-slate-700">
                            {ing.ins_e_number}
                          </span>
                        </div>
                        <p className="text-[11px] text-slate-500 line-clamp-1">
                          {ing.function} • {ing.category}
                        </p>
                      </div>

                      <div className="flex items-center gap-1.5 shrink-0">
                        {ing.cross_country_reason && (
                          <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-500 border border-amber-500/30" title="Cross-country divergence exists">
                            Divergent
                          </span>
                        )}
                        <ChevronRight className={`w-4 h-4 transition-transform ${isSelected ? 'text-emerald-500 translate-x-0.5' : 'text-slate-400'}`} />
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Right Column: Detailed Regulatory & Toxicological Profile */}
        <div className="lg:col-span-7">
          {selectedIngredient ? (
            <div className="glass-card rounded-2xl p-6 border space-y-6 sticky top-24">
              
              {/* Header Profile */}
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-4 border-b border-slate-200">
                <div className="space-y-1">
                  <div className="flex items-center gap-2 flex-wrap">
                    <h2 className="text-xl font-bold text-slate-900">
                      {selectedIngredient.common_name}
                    </h2>
                    <span className="text-xs font-mono font-bold px-2 py-0.5 rounded-lg bg-emerald-500/20 text-emerald-500 border border-emerald-500/30">
                      {selectedIngredient.ins_e_number}
                    </span>
                  </div>
                  <p className="text-xs text-slate-500 font-mono">
                    {selectedIngredient.scientific_name}
                  </p>
                  <p className="text-xs font-semibold text-slate-700">
                    Category: <span className="text-emerald-600">{selectedIngredient.category}</span> ({selectedIngredient.function})
                  </p>
                </div>

                <div className="shrink-0 flex items-center gap-2">
                  <span className={`px-2.5 py-1 rounded-xl text-xs font-bold ${
                    selectedIngredient.risk_classification === 'Critical' ? 'bg-rose-500/20 text-rose-500 border border-rose-500/30' :
                    selectedIngredient.risk_classification === 'High' ? 'bg-orange-500/20 text-orange-500 border border-orange-500/30' :
                    selectedIngredient.risk_classification === 'Moderate' ? 'bg-amber-500/20 text-amber-500 border border-amber-500/30' :
                    'bg-emerald-500/20 text-emerald-500 border border-emerald-500/30'
                  }`}>
                    Risk: {selectedIngredient.risk_classification}
                  </span>
                </div>
              </div>

              {/* Cross-Country Rationale Highlight Box */}
              {selectedIngredient.cross_country_reason && (
                <div className="p-4 rounded-xl bg-gradient-to-r from-amber-500/15 via-orange-500/10 to-amber-500/5 border border-amber-500/30 space-y-2">
                  <div className="flex items-center gap-2 text-xs font-bold text-amber-600">
                    <Scale className="w-4 h-4" />
                    <span>Why Regulatory Status Differs Across Countries</span>
                  </div>
                  <p className="text-xs text-slate-700 leading-relaxed">
                    {selectedIngredient.cross_country_reason}
                  </p>
                  <div className="flex items-center gap-1.5 text-[11px] text-slate-500 pt-1">
                    <BookOpen className="w-3.5 h-3.5 text-slate-400" />
                    <span>Source: {selectedIngredient.evidence_source}</span>
                  </div>
                </div>
              )}

              {/* Country Comparison Cards */}
              <div className="space-y-3">
                <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider flex items-center gap-2">
                  <Globe className="w-3.5 h-3.5 text-emerald-500" />
                  <span>Country-by-Country Regulatory Status</span>
                </h3>

                <div className="grid grid-cols-1 gap-3">
                  
                  {/* India (FSSAI) */}
                  <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-1.5">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="text-base">🇮🇳</span>
                        <span className="text-xs font-bold text-slate-900">India (FSSAI)</span>
                      </div>
                      {getStatusBadge(selectedIngredient.india_status.code, selectedIngredient.india_status.status)}
                    </div>
                    <p className="text-xs text-slate-600">
                      <span className="font-semibold text-slate-500">Limit:</span> {selectedIngredient.india_status.max_limit}
                    </p>
                    <p className="text-[11px] text-slate-500">
                      {selectedIngredient.india_status.condition}
                    </p>
                  </div>

                  {/* USA (FDA) */}
                  <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-1.5">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="text-base">🇺🇸</span>
                        <span className="text-xs font-bold text-slate-900">USA (FDA)</span>
                      </div>
                      {getStatusBadge(selectedIngredient.usa_status.code, selectedIngredient.usa_status.status)}
                    </div>
                    <p className="text-xs text-slate-600">
                      <span className="font-semibold text-slate-500">Limit:</span> {selectedIngredient.usa_status.max_limit}
                    </p>
                    <p className="text-[11px] text-slate-500">
                      {selectedIngredient.usa_status.condition}
                    </p>
                  </div>

                  {/* European Union (EFSA) */}
                  <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-1.5">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="text-base">🇪🇺</span>
                        <span className="text-xs font-bold text-slate-900">European Union (EFSA)</span>
                      </div>
                      {getStatusBadge(selectedIngredient.eu_status.code, selectedIngredient.eu_status.status)}
                    </div>
                    <p className="text-xs text-slate-600">
                      <span className="font-semibold text-slate-500">Limit:</span> {selectedIngredient.eu_status.max_limit}
                    </p>
                    <p className="text-[11px] text-slate-500">
                      {selectedIngredient.eu_status.condition}
                    </p>
                  </div>

                  {/* Germany (BVL) */}
                  <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-1.5">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="text-base">🇩🇪</span>
                        <span className="text-xs font-bold text-slate-900">Germany (BVL / EU Baseline)</span>
                      </div>
                      {getStatusBadge(selectedIngredient.germany_status.code, selectedIngredient.germany_status.status)}
                    </div>
                    <p className="text-xs text-slate-600">
                      <span className="font-semibold text-slate-500">National Decree:</span> {selectedIngredient.germany_status.condition}
                    </p>
                  </div>

                </div>
              </div>

              {/* Consumer Concerns Tags */}
              {selectedIngredient.consumer_concerns && selectedIngredient.consumer_concerns.length > 0 && (
                <div className="space-y-2 pt-2 border-t border-slate-200">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                    Consumer & Health Concerns
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {selectedIngredient.consumer_concerns.map((c, i) => (
                      <span key={i} className="text-xs px-2.5 py-1 rounded-lg bg-slate-200 text-slate-700 border border-slate-300">
                        ⚠️ {c}
                      </span>
                    ))}
                  </div>
                </div>
              )}

            </div>
          ) : (
            <div className="glass-card rounded-2xl p-12 text-center text-slate-400">
              Select an ingredient from the catalog to inspect its global regulatory profile.
            </div>
          )}
        </div>

      </div>

    </div>
  );
}
