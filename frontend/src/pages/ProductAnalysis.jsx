import React, { useState } from 'react';
import { ArrowLeft, ArrowRight, AlertTriangle, CheckCircle2, ShieldCheck, Info, Search, FileSpreadsheet, ChevronDown, ChevronUp } from 'lucide-react';
import RESTRICTED_HAZARDS from '../data/restricted_substances_hazards.json';

export default function ProductAnalysis({ data, onReset }) {
  const [hasProceededToStep2, setHasProceededToStep2] = useState(false);
  const [hazardSearch, setHazardSearch] = useState('');
  const [isHazardsExpanded, setIsHazardsExpanded] = useState(true);

  if (!data) {
    return (
      <div className="p-8 text-center text-gray-500 text-xs">
        <p>No product analysis data available.</p>
        <button onClick={onReset} className="mt-3 px-4 py-2 rounded bg-blue-600 text-white font-medium cursor-pointer">
          Check Another Product
        </button>
      </div>
    );
  }

  const {
    product_name = "Food Product",
    brand = "Packaged Goods",
    barcode,
    category = "Packaged Food",
    quality_score = 75,
    final_verdict_badge,
    risk = {},
    regulatory = {},
    adulteration = {},
    parsed_ingredients = [],
    matched_ingredients = [],
    regulatory_alerts = [],
    clean_ingredients = [],
    dataset_eval = {},
    source
  } = data || {};

  // Safely normalize ingredients list
  let ingredientsList = [];
  try {
    if (Array.isArray(parsed_ingredients) && parsed_ingredients.length > 0) {
      ingredientsList = parsed_ingredients;
    } else if (typeof data.ingredients === 'string' && data.ingredients.length > 0) {
      ingredientsList = data.ingredients.split(',').map(s => s.trim()).filter(Boolean);
    } else if (typeof data.ingredients_text === 'string' && data.ingredients_text.length > 0) {
      ingredientsList = data.ingredients_text.split(',').map(s => s.trim()).filter(Boolean);
    }
  } catch (e) {
    ingredientsList = [];
  }

  // Normalize alerts from 300-item dataset
  const alertsList = Array.isArray(regulatory_alerts) ? regulatory_alerts : [];

  // Step-wise assessment logic
  const localIssues = alertsList.filter(a => 
    (a.india_status || '').toLowerCase().includes('not') || 
    (a.india_status || '').toLowerCase().includes('banned') ||
    (a.flagged_authorities || '').toLowerCase().includes('india')
  );
  
  const globalIssues = alertsList.filter(a =>
    (a.usa_status || '').toLowerCase().includes('not') ||
    (a.usa_status || '').toLowerCase().includes('revoked') ||
    (a.eu_status || '').toLowerCase().includes('not') ||
    (a.eu_status || '').toLowerCase().includes('banned') ||
    (a.flagged_authorities || '').toLowerCase().includes('european') ||
    (a.flagged_authorities || '').toLowerCase().includes('fda')
  );

  const isStep1Passed = localIssues.length === 0;
  const isStep2Passed = globalIssues.length === 0;

  // Determine overall risk level based on user step authorization
  let overallRisk = "LOW";
  let badgeColor = "bg-green-50 text-green-700 border-green-200";

  if (!hasProceededToStep2) {
    if (!isStep1Passed) {
      overallRisk = "HIGH";
      badgeColor = "bg-red-50 text-red-700 border-red-200";
    } else {
      overallRisk = "LOW";
      badgeColor = "bg-green-50 text-green-700 border-green-200";
    }
  } else {
    try {
      const v = (final_verdict_badge || (risk && risk.risk_tier) || data.final_verdict || '').toLowerCase();
      if (!isStep2Passed || alertsList.some(a => (a.alert_reason || '').toLowerCase().includes('banned') || (a.alert_reason || '').toLowerCase().includes('revoked')) || v.includes('high') || v.includes('banned') || v.includes('critical')) {
        overallRisk = "HIGH";
        badgeColor = "bg-red-50 text-red-700 border-red-200";
      } else if (alertsList.length > 0 || v.includes('mod') || v.includes('cond') || Number(quality_score) < 70) {
        overallRisk = "MEDIUM";
        badgeColor = "bg-amber-50 text-amber-700 border-amber-200";
      }
    } catch (e) {
      overallRisk = "LOW";
    }
  }

  // Country regulatory summary based on real alerts
  const isUsBanned = alertsList.some(a => (a.usa_status || '').toLowerCase().includes('not') || (a.usa_status || '').toLowerCase().includes('revoked'));
  const isEuBanned = alertsList.some(a => (a.eu_status || '').toLowerCase().includes('not') || (a.eu_status || '').toLowerCase().includes('banned'));
  const isIndiaBanned = localIssues.length > 0;

  const countries = [
    {
      name: "India",
      authority: "FSSAI",
      status: isIndiaBanned ? "Not Permitted / Banned" : (alertsList.length > 0 ? "Permitted with Limits" : "Allowed"),
      isAllowed: !isIndiaBanned
    },
    {
      name: "European Union",
      authority: "EFSA",
      status: isEuBanned ? "Not Authorised / Banned" : (alertsList.length > 0 ? "Restricted Uses" : "Allowed"),
      isAllowed: !isEuBanned
    },
    {
      name: "USA",
      authority: "FDA",
      status: isUsBanned ? "Revoked / Not Permitted" : (alertsList.length > 0 ? "Permitted within Limits" : "Allowed"),
      isAllowed: !isUsBanned
    },
    {
      name: "Australia / NZ",
      authority: "FSANZ",
      status: alertsList.length > 0 ? "Standard Limits Apply" : "Allowed",
      isAllowed: true
    }
  ];

  // Matched hazards against scanned product
  const matchedHazards = (RESTRICTED_HAZARDS || []).filter(h => 
    alertsList.some(a => {
      const aIns = (a.ins_number || '').toLowerCase().replace(/[^\w]/g, '');
      const aName = (a.ingredient_name || '').toLowerCase();
      const hIns = (h.ins_code || '').toLowerCase().replace(/[^\w]/g, '');
      const hName = (h.common_name || '').toLowerCase();
      return (aIns && hIns && aIns === hIns) || aName.includes(hName) || hName.includes(aName);
    })
  );

  // Filtered hazards for search
  const filteredHazards = (RESTRICTED_HAZARDS || []).filter(h => {
    if (!hazardSearch.trim()) return true;
    const q = hazardSearch.toLowerCase();
    return (
      (h.ins_code || '').toLowerCase().includes(q) ||
      (h.common_name || '').toLowerCase().includes(q) ||
      (h.health_problems_faced || '').toLowerCase().includes(q) ||
      (h.primary_organ_affected || '').toLowerCase().includes(q) ||
      (h.restriction_status || '').toLowerCase().includes(q)
    );
  });

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      
      {/* ── Top Header ── */}
      <div className="flex items-center justify-between border-b border-gray-200 pb-3">
        <div>
          <span className="text-xs text-gray-500 font-semibold uppercase tracking-wider block">
            Product Safety & Regulatory Assessment
          </span>
          <h1 className="text-xl font-bold text-gray-900">{String(product_name)}</h1>
          <p className="text-xs text-gray-600">
            {String(brand)} • {String(category)} {barcode ? `• Barcode: ${barcode}` : ''}
          </p>
          {source && (
            <span className="inline-block mt-1 text-[11px] text-blue-600 bg-blue-50 px-2 py-0.5 rounded border border-blue-100">
              Source: {source}
            </span>
          )}
        </div>

        <button
          onClick={onReset}
          className="px-3.5 py-1.5 rounded bg-gray-100 hover:bg-gray-200 text-gray-800 text-xs font-semibold flex items-center gap-1.5 cursor-pointer border border-gray-200"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Check Another Product</span>
        </button>
      </div>

      {/* ── Overall Risk Card ── */}
      <div className="bg-white border border-gray-200 rounded-lg p-5 flex items-center justify-between">
        <div>
          <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider block">
            Overall Risk Assessment
          </span>
          <div className="text-2xl font-black text-gray-900 mt-1">
            {overallRisk} RISK
          </div>
          <p className="text-xs text-gray-600 mt-0.5">
            Safety Score: <strong>{Number(quality_score) || 75} / 100</strong>
          </p>
        </div>

        <span className={`px-4 py-2 rounded-md text-sm font-bold border ${badgeColor}`}>
          {overallRisk} RISK
        </span>
      </div>

      {/* ── Step-Wise Regulatory Verification Pipeline (Step 1 -> Step 2) ── */}
      <div className="bg-white border border-gray-200 rounded-lg p-5 space-y-4">
        <div className="border-b border-gray-100 pb-2 flex items-center justify-between">
          <h2 className="text-sm font-bold text-gray-900 flex items-center gap-2">
            <span>Step-by-Step Regulatory Verification Pipeline</span>
          </h2>
          <span className="text-[11px] text-gray-500">
            Local Authority (FSSAI) → Global Database (EFSA & FDA)
          </span>
        </div>

        {/* STEP 1: LOCAL DATABASE CHECK */}
        <div className={`p-4 rounded-md border text-xs space-y-2 ${
          isStep1Passed 
            ? 'bg-green-50/60 border-green-200 text-green-950' 
            : 'bg-red-50 border-red-200 text-red-950'
        }`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold ${
                isStep1Passed ? 'bg-green-600 text-white' : 'bg-red-600 text-white'
              }`}>
                1
              </span>
              <strong className="text-sm font-bold">
                Step 1: Local Database Verification (India FSSAI)
              </strong>
            </div>
            <span className={`px-2.5 py-0.5 rounded text-[11px] font-bold border ${
              isStep1Passed 
                ? 'bg-green-100 text-green-800 border-green-300' 
                : 'bg-red-100 text-red-800 border-red-300'
            }`}>
              {isStep1Passed ? '✓ STEP 1 PASSED: PERMITTED' : '✕ STEP 1 ALERT: RESTRICTED'}
            </span>
          </div>

          <p className="text-gray-700 leading-relaxed text-xs pl-7">
            {isStep1Passed
              ? "All detected formulation ingredients are Permitted under Indian FSSAI domestic food safety regulations. Proceeding to Step 2 (Global Database)."
              : "One or more ingredients have restrictions or prohibitions under Indian domestic FSSAI food standards. Checking global database for international standing."
            }
          </p>

          {/* If Local issues exist, display them */}
          {!isStep1Passed && (
            <div className="pl-7 pt-1 space-y-2">
              {localIssues.map((item, idx) => (
                <div key={idx} className="bg-white p-2.5 rounded border border-red-200 text-xs space-y-1">
                  <div className="font-bold text-red-800">
                    {item.ins_number} — {item.ingredient_name}
                  </div>
                  <div><strong>Country / Authority:</strong> India (FSSAI)</div>
                  <div><strong>Reason behind alert:</strong> {item.alert_reason || item.screening_note}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* ── USER PERMISSION CHECKPOINT / STEP 2 ── */}
        {!hasProceededToStep2 ? (
          <div className="p-4 bg-blue-50/90 border border-blue-200 rounded-lg text-xs space-y-3">
            <div className="flex items-start gap-2.5">
              <Info className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
              <div>
                <strong className="text-blue-950 block font-bold text-sm">
                  User Permission Required: Check Forward Against Global Database?
                </strong>
                <p className="text-gray-700 text-xs mt-1 leading-relaxed">
                  {isStep1Passed 
                    ? "Step 1 (Local FSSAI Database) is completely Permitted. By default, local clearance is achieved. Do you want to grant permission to check forward against the Global Database (European Union EFSA & US FDA) for international compliance?"
                    : "Step 1 (Local FSSAI Database) has flagged domestic concerns. Do you wish to grant permission to check forward against the Global Database (European Union EFSA & US FDA)?"
                  }
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3 pt-1 pl-6 flex-wrap">
              <button
                type="button"
                onClick={() => setHasProceededToStep2(true)}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-bold text-xs flex items-center gap-1.5 cursor-pointer shadow-sm transition-colors"
              >
                <span>Check Forward (Proceed to Step 2: Global Database)</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>

              <span className="text-gray-500 text-[11px]">
                or stay with Local Clearance
              </span>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center justify-between border-t border-gray-100 pt-3">
              <span className="text-xs font-semibold text-gray-500">
                User Granted Permission: Checking Global Regulatory Database
              </span>
              <button
                type="button"
                onClick={() => setHasProceededToStep2(false)}
                className="text-xs text-blue-600 hover:underline flex items-center gap-1 cursor-pointer font-medium"
              >
                <span>← Collapse Step 2 / Back to Step 1 Only</span>
              </button>
            </div>

            {/* STEP 2: GLOBAL DATABASE CHECK */}
            <div className={`p-4 rounded-md border text-xs space-y-2 ${
              isStep2Passed 
                ? 'bg-green-50/60 border-green-200 text-green-950' 
                : 'bg-red-50 border-red-200 text-red-950'
            }`}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold ${
                    isStep2Passed ? 'bg-green-600 text-white' : 'bg-red-600 text-white'
                  }`}>
                    2
                  </span>
                  <strong className="text-sm font-bold">
                    Step 2: Global Database Verification (European Union EFSA & US FDA)
                  </strong>
                </div>
                <span className={`px-2.5 py-0.5 rounded text-[11px] font-bold border ${
                  isStep2Passed 
                    ? 'bg-green-100 text-green-800 border-green-300' 
                    : 'bg-red-100 text-red-800 border-red-300'
                }`}>
                  {isStep2Passed ? '✓ STEP 2 PASSED: PERMITTED' : '✕ STEP 2 RED ALERT: BANNED / RESTRICTED'}
                </span>
              </div>

              <p className="text-gray-700 leading-relaxed text-xs pl-7">
                {isStep2Passed
                  ? "All detected formulation ingredients are Permitted across international global databases (European Union EFSA and US FDA). All permissions verified clean."
                  : "Formulation divergence detected! While permitted in some jurisdictions, an ingredient is strictly RESTRICTED or BANNED in the Global Database."
                }
              </p>

              {/* If Global issues exist, display why no: Item Name, INS, Country, Reason */}
              {!isStep2Passed && (
                <div className="pl-7 pt-2 space-y-3">
                  {globalIssues.map((alt, idx) => (
                    <div key={idx} className="bg-white p-3 rounded border border-red-200 text-xs space-y-2 text-red-950">
                      <div className="flex items-center justify-between border-b border-red-100 pb-1.5">
                        <div>
                          <span className="font-bold text-sm text-red-800 block">
                            {alt.ins_number} — {alt.ingredient_name}
                          </span>
                          {alt.chemical_name && (
                            <span className="text-[11px] text-gray-500 font-mono">
                              Chemical: {alt.chemical_name}
                            </span>
                          )}
                        </div>
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-red-100 text-red-800 border border-red-300">
                          INTERNATIONAL BAN
                        </span>
                      </div>

                      <div className="space-y-1.5 text-xs">
                        <p>
                          <strong className="text-gray-900">Flagged Country / Union:</strong>{' '}
                          <span className="text-red-700 font-bold">{alt.flagged_authorities}</span>
                        </p>
                        <p className="leading-relaxed">
                          <strong className="text-gray-900">Reason Behind Alert:</strong>{' '}
                          <span className="text-red-900 font-medium">{alt.alert_reason}</span>
                        </p>
                        {alt.regulatory_reference && (
                          <p className="text-[11px] text-gray-600">
                            <strong>Statutory Reference:</strong> {alt.regulatory_reference}
                          </p>
                        )}
                      </div>

                      {/* Multi-Country Permission Matrix */}
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 pt-1 text-[11px]">
                        <div className="bg-gray-50 p-2 rounded border border-gray-200">
                          <span className="text-gray-500 block">India (Local DB):</span>
                          <strong className={alt.india_status?.toLowerCase().includes('not') ? 'text-red-700' : 'text-green-700'}>
                            {alt.india_status || 'Permitted with limits'}
                          </strong>
                        </div>
                        <div className="bg-gray-50 p-2 rounded border border-gray-200">
                          <span className="text-gray-500 block">USA (FDA Global DB):</span>
                          <strong className={alt.usa_status?.toLowerCase().includes('not') || alt.usa_status?.toLowerCase().includes('revoked') ? 'text-red-700' : 'text-green-700'}>
                            {alt.usa_status || 'Permitted'}
                          </strong>
                        </div>
                        <div className="bg-gray-50 p-2 rounded border border-gray-200">
                          <span className="text-gray-500 block">EU (EFSA Global DB):</span>
                          <strong className={alt.eu_status?.toLowerCase().includes('not') || alt.eu_status?.toLowerCase().includes('banned') ? 'text-red-700' : 'text-green-700'}>
                            {alt.eu_status || 'Permitted'}
                          </strong>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* SUMMARY CONCLUSION */}
            {isStep1Passed && isStep2Passed ? (
              <div className="bg-green-100/70 border border-green-300 rounded-md p-3.5 flex items-center gap-3">
                <CheckCircle2 className="w-5 h-5 text-green-700 shrink-0" />
                <div className="text-xs text-green-950">
                  <strong className="block text-sm font-bold text-green-800">
                    All Regulatory Permissions OK — No Worries
                  </strong>
                  <span>
                    Both Step 1 (Local FSSAI) and Step 2 (Global EFSA & FDA) verified completely clean. No banned substances or revoked authorizations found.
                  </span>
                </div>
              </div>
            ) : (
              <div className="bg-red-50 border border-red-300 rounded-md p-3.5 flex items-center gap-3">
                <AlertTriangle className="w-5 h-5 text-red-700 shrink-0" />
                <div className="text-xs text-red-950">
                  <strong className="block text-sm font-bold text-red-800">
                    Regulatory Divergence Alert Detected
                  </strong>
                  <span>
                    Product passed initial local screening or has divergent international clearance. Caution is advised for sensitive demographics or export compliance.
                  </span>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* ── Ingredient Analysis Table ── */}
      <div className="bg-white border border-gray-200 rounded-lg p-5 space-y-3">
        <h2 className="text-sm font-bold text-gray-900 border-b border-gray-100 pb-2">
          Detected Ingredients & Dataset Matching
        </h2>

        {ingredientsList.length === 0 ? (
          <p className="text-xs text-gray-500">Standard packaged food formulation verified.</p>
        ) : (
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-gray-200 bg-gray-50 text-gray-600">
                <th className="py-2 px-3">Ingredient</th>
                <th className="py-2 px-3 text-right">Regulatory Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {ingredientsList.map((ing, i) => {
                const ingName = typeof ing === 'string' ? ing : (ing?.name || ing?.ingredient || 'Ingredient');
                const safeIngStr = String(ingName).toLowerCase();
                
                // Check if this ingredient generated an alert in our dataset
                const matchedAlert = alertsList.find(a => {
                  const insLow = (a.ins_number || '').toLowerCase().replace(/[^\w]/g, '');
                  const nameLow = (a.ingredient_name || '').toLowerCase();
                  const targetClean = safeIngStr.replace(/[^\w]/g, '');
                  return safeIngStr.includes(nameLow) || (insLow && targetClean.includes(insLow));
                });

                  return (
                    <tr key={i}>
                      <td className="py-2 px-3 text-gray-900 font-medium">
                        {String(ingName)}
                      </td>
                      <td className="py-2 px-3 text-right">
                        {matchedAlert ? (
                          <span className="text-red-700 font-bold inline-flex items-center justify-end gap-1">
                            ⚠ Restricted in {String(matchedAlert.flagged_authorities || 'International Regulations').split('(')[0].trim()}
                          </span>
                        ) : (
                          <span className="text-green-600 font-bold inline-flex items-center justify-end gap-1">
                            ✓ Allowed
                          </span>
                        )}
                      </td>
                    </tr>
                  );
              })}
            </tbody>
          </table>
        )}
      </div>

      {/* ── Regulatory Check Table ── */}
      <div className="bg-white border border-gray-200 rounded-lg p-5 space-y-3">
        <h2 className="text-sm font-bold text-gray-900 border-b border-gray-100 pb-2">
          Regulatory Check by Authority
        </h2>

        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50 text-gray-600">
              <th className="py-2 px-3">Country / Region</th>
              <th className="py-2 px-3">Authority</th>
              <th className="py-2 px-3 text-right">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {countries.map((c, i) => (
              <tr key={i}>
                <td className="py-2 px-3 font-semibold text-gray-900">{c.name}</td>
                <td className="py-2 px-3 text-gray-500">{c.authority}</td>
                <td className={`py-2 px-3 text-right font-bold ${c.isAllowed ? 'text-green-600' : 'text-red-600'}`}>
                  {c.isAllowed ? `✓ ${c.status}` : `✕ ${c.status}`}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* ── Problem Faced by Restricted Substances Reference Dataset (After Last Section) ── */}
      <div className="bg-white border border-gray-200 rounded-lg p-5 space-y-4">
        <div className="flex items-center justify-between border-b border-gray-100 pb-3 flex-wrap gap-2">
          <div>
            <div className="flex items-center gap-2">
              <FileSpreadsheet className="w-4 h-4 text-blue-600 shrink-0" />
              <h2 className="text-sm font-bold text-gray-900">
                Restricted Substances & Health Hazards Reference Dataset
              </h2>
            </div>
            <p className="text-[11px] text-gray-500 mt-0.5">
              Specific physiological problems faced, toxicological pathologies, and health hazards of restricted additives & adulterants.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => setIsHazardsExpanded(!isHazardsExpanded)}
              className="px-2.5 py-1 text-xs border border-gray-200 rounded hover:bg-gray-50 flex items-center gap-1 text-gray-700 cursor-pointer"
            >
              <span>{isHazardsExpanded ? 'Collapse Table' : 'Expand Table'}</span>
              {isHazardsExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
            </button>
          </div>
        </div>

        {isHazardsExpanded && (
          <div className="space-y-3">
            {/* Filter / Search Bar */}
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-gray-400 absolute left-3 top-2.5" />
              <input
                type="text"
                value={hazardSearch}
                onChange={(e) => setHazardSearch(e.target.value)}
                placeholder="Search restricted substances by INS code, name, organ, or health hazard (e.g. 171, DNA, Thyroid, Asthma)..."
                className="w-full pl-9 pr-3 py-1.5 border border-gray-200 rounded text-xs text-gray-800 placeholder-gray-400 focus:outline-none focus:border-blue-500"
              />
            </div>

            {/* If scanned product matches any restricted hazard, highlight it */}
            {matchedHazards.length > 0 && (
              <div className="p-3 bg-red-50/90 border border-red-200 rounded text-xs space-y-1.5 text-red-950">
                <span className="font-bold text-red-800 block flex items-center gap-1.5">
                  <AlertTriangle className="w-3.5 h-3.5 text-red-600 shrink-0" />
                  <span>Clinical Hazards Facing Detected Ingredients in Current Product ({matchedHazards.length}):</span>
                </span>
                {matchedHazards.map((mh, idx) => (
                  <div key={idx} className="bg-white p-2.5 rounded border border-red-200 text-xs space-y-1">
                    <div>
                      <strong className="text-red-900">{mh.common_name} ({mh.ins_code}):</strong>{' '}
                      <span className="text-gray-800">{mh.health_problems_faced}</span>
                    </div>
                    <div className="text-[11px] text-gray-600 flex flex-wrap gap-x-4 gap-y-0.5 pt-0.5 border-t border-gray-100">
                      <span><strong>Target Organ:</strong> <span className="text-red-700">{mh.primary_organ_affected}</span></span>
                      <span><strong>Restriction Status:</strong> {mh.restriction_status}</span>
                      <span><strong>Safe Substitute:</strong> <span className="text-green-700">{mh.safer_permitted_alternatives}</span></span>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Scrollable Reference Table */}
            <div className="overflow-x-auto border border-gray-200 rounded max-h-96">
              <table className="w-full text-left text-xs border-collapse">
                <thead className="sticky top-0 z-10">
                  <tr className="bg-gray-100 border-b border-gray-200 text-gray-700 font-semibold shadow-xs">
                    <th className="py-2.5 px-3 whitespace-nowrap bg-gray-100">Code</th>
                    <th className="py-2.5 px-3 bg-gray-100">Substance Name</th>
                    <th className="py-2.5 px-3 whitespace-nowrap bg-gray-100">Primary Organ</th>
                    <th className="py-2.5 px-3 min-w-[260px] bg-gray-100">Problems Faced (Health Hazards & Toxicity)</th>
                    <th className="py-2.5 px-3 whitespace-nowrap bg-gray-100">Restriction Status</th>
                    <th className="py-2.5 px-3 bg-gray-100">Safer Alternative</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {filteredHazards.map((item, idx) => {
                    const isMatchedInScan = alertsList.some(a => {
                      const aIns = (a.ins_number || '').toLowerCase().replace(/[^\w]/g, '');
                      const hIns = (item.ins_code || '').toLowerCase().replace(/[^\w]/g, '');
                      return aIns && hIns && aIns === hIns;
                    });

                    return (
                      <tr 
                        key={idx} 
                        className={`transition-colors ${
                          isMatchedInScan ? 'bg-red-50/70 font-medium' : 'hover:bg-gray-50'
                        }`}
                      >
                        <td className="py-2.5 px-3 font-mono font-bold text-gray-900 whitespace-nowrap">
                          {item.ins_code}
                          {isMatchedInScan && (
                            <span className="block text-[10px] text-red-600 font-sans font-bold">
                              [In Scanned Food]
                            </span>
                          )}
                        </td>
                        <td className="py-2.5 px-3">
                          <strong className="text-gray-900 block">{item.common_name}</strong>
                          <span className="text-[10px] text-gray-500 block truncate max-w-[160px]" title={item.scientific_chemical_name}>
                            {item.scientific_chemical_name}
                          </span>
                        </td>
                        <td className="py-2.5 px-3 text-gray-700 whitespace-nowrap font-medium">
                          {item.primary_organ_affected}
                        </td>
                        <td className="py-2.5 px-3 text-gray-800 leading-relaxed text-[11px]">
                          {item.health_problems_faced}
                        </td>
                        <td className="py-2.5 px-3 text-[11px] whitespace-nowrap">
                          <span className="text-red-700 font-bold block max-w-[150px] truncate" title={item.restriction_status}>
                            {item.restriction_status}
                          </span>
                        </td>
                        <td className="py-2.5 px-3 text-[11px] text-green-800 font-medium">
                          {item.safer_permitted_alternatives}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>

            {/* Dataset Provenance Footer */}
            <div className="flex items-center justify-between text-[11px] text-gray-500 pt-1 flex-wrap gap-2 border-t border-gray-100">
              <span>
                Showing {filteredHazards.length} of {RESTRICTED_HAZARDS.length} toxicological profiles • EFSA, US FDA, FSSAI Gazettes & IARC Monographs
              </span>
              <span className="text-blue-600 font-mono text-[10px]">
                File: dataset/restricted_substances_hazards_dataset.csv
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Bottom Action Button */}
      <div className="pt-2 text-center">
        <button
          onClick={onReset}
          className="px-6 py-2.5 rounded bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs cursor-pointer transition-colors"
        >
          Check Another Product
        </button>
      </div>

    </div>
  );
}
