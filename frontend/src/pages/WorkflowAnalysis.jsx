import React from 'react';
import ProductAnalysis from './ProductAnalysis';

export default function WorkflowAnalysis({ data, onReset, loading }) {
  if (loading) {
    return (
      <div className="p-12 text-center text-gray-500 text-xs space-y-2">
        <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="font-semibold text-gray-700">Analyzing product & regulatory rules...</p>
      </div>
    );
  }

  if (!data) return null;

  return <ProductAnalysis data={data} onReset={onReset} />;
}
