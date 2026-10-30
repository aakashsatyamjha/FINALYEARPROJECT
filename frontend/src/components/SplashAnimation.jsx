import React, { useEffect, useState } from 'react';
import { ShieldCheck } from 'lucide-react';

export default function SplashAnimation({ onComplete }) {
  const [stage, setStage] = useState(0); // 0: init, 1: glow+logo, 2: scan, 3: text, 4: exit

  useEffect(() => {
    const t1 = setTimeout(() => setStage(1), 60);
    const t2 = setTimeout(() => setStage(2), 400);
    const t3 = setTimeout(() => setStage(3), 700);
    const t4 = setTimeout(() => setStage(4), 1250);
    const t5 = setTimeout(() => {
      if (onComplete) onComplete();
    }, 1450);

    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
      clearTimeout(t3);
      clearTimeout(t4);
      clearTimeout(t5);
    };
  }, [onComplete]);

  return (
    <div className={`
      fixed inset-0 z-[99999] w-screen h-screen flex flex-col items-center justify-center bg-white text-slate-900
      transition-all duration-300 ease-out select-none
      ${stage === 4 ? 'opacity-0 pointer-events-none scale-105' : 'opacity-100 pointer-events-auto scale-100'}
    `}>
      
      {/* Background Radial Glow */}
      <div className={`
        absolute w-96 h-96 rounded-full bg-emerald-100 blur-3xl pointer-events-none transition-all duration-700
        ${stage >= 1 ? 'opacity-100 scale-100' : 'opacity-0 scale-75'}
      `} />
      
      <div className="relative z-10 flex flex-col items-center justify-center space-y-6">
        
        {/* Shield Logo */}
        <div className={`
          relative w-20 h-20 rounded-2xl bg-gradient-to-br from-emerald-100 to-teal-50 border border-emerald-200
          flex items-center justify-center shadow-lg shadow-emerald-100 overflow-hidden
          transition-all duration-500 transform
          ${stage >= 1 ? 'opacity-100 scale-100 translate-y-0' : 'opacity-0 scale-90 translate-y-4'}
        `}>
          <ShieldCheck className="w-11 h-11 text-emerald-600 stroke-[2.2] relative z-10" />

          {/* Laser Scanning Beam */}
          <div className={`
            absolute inset-x-0 h-1 bg-gradient-to-r from-transparent via-emerald-400 to-transparent
            shadow-[0_0_15px_rgba(16,185,129,0.4)] transition-all duration-700 ease-in-out
            ${stage >= 2 ? 'top-full opacity-100' : 'top-0 opacity-0'}
          `} />

          <div className="absolute inset-0 bg-emerald-100/30 animate-pulse pointer-events-none" />
        </div>

        {/* Brand Name */}
        <div className={`
          text-center space-y-1.5 transition-all duration-500 transform
          ${stage >= 3 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-3'}
        `}>
          <div className="flex items-center justify-center gap-2">
            <span className="text-3xl font-extrabold tracking-tight text-slate-900">
              FoodGuard
            </span>
            <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-700 border border-emerald-200">
              AI
            </span>
          </div>

          <p className="text-xs font-medium text-slate-500 tracking-widest uppercase">
            AI Food Safety Platform
          </p>
        </div>

        {/* Status bar */}
        <div className={`
          w-32 h-1 rounded-full bg-slate-200 overflow-hidden transition-opacity duration-300
          ${stage >= 2 ? 'opacity-100' : 'opacity-0'}
        `}>
          <div className="h-full bg-gradient-to-r from-emerald-500 via-teal-400 to-emerald-400 rounded-full animate-[shimmer_1s_infinite] w-full" />
        </div>

      </div>

    </div>
  );
}
