import React, { useState, useEffect } from 'react';
import { DollarSign, ShieldAlert, CheckCircle2, TrendingUp, AlertTriangle } from 'lucide-react';

export default function ExecutiveDashboard() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMetrics();
  }, []);

  const fetchMetrics = async () => {
    try {
      const res = await fetch('/api/analytics/dashboard');
      const data = await res.json();
      setMetrics(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !metrics) {
    return <div className="text-gray-400 font-mono text-sm py-12 text-center animate-pulse">Aggregating Executive BI Data...</div>;
  }

  return (
    <div className="space-y-6">
      
      {/* Title */}
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Executive Trust & Risk Intelligence</h1>
        <p className="text-sm text-gray-400 mt-1">
          Simulated marketplace metrics measuring fraud loss prevention, false positive impact, and rule performance.
        </p>
      </div>

      {/* Top 4 KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <div className="bg-[#111827] border border-gray-800 p-5 rounded-xl shadow-sm">
          <div className="flex items-center justify-between text-gray-400 text-xs font-medium">
            <span>PREVENTED FRAUD LOSS</span>
            <DollarSign className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-2">
            ${metrics.prevented_fraud_loss_usd.toLocaleString()}
          </div>
          <div className="text-xs text-gray-400 mt-1">Simulated intercepted value</div>
        </div>

        <div className="bg-[#111827] border border-gray-800 p-5 rounded-xl shadow-sm">
          <div className="flex items-center justify-between text-gray-400 text-xs font-medium">
            <span>TOTAL PROCESSED VOLUME</span>
            <TrendingUp className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-white mt-2">
            ${metrics.total_volume_usd.toLocaleString()}
          </div>
          <div className="text-xs text-gray-400 mt-1">{metrics.total_transactions} transactions scored</div>
        </div>

        <div className="bg-[#111827] border border-gray-800 p-5 rounded-xl shadow-sm">
          <div className="flex items-center justify-between text-gray-400 text-xs font-medium">
            <span>FALSE POSITIVE RATIO (FPR)</span>
            <CheckCircle2 className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-amber-400 mt-2">
            {metrics.false_positive_rate}%
          </div>
          <div className="text-xs text-gray-400 mt-1">Target benchmark &lt; 5.0%</div>
        </div>

        <div className="bg-[#111827] border border-gray-800 p-5 rounded-xl shadow-sm">
          <div className="flex items-center justify-between text-gray-400 text-xs font-medium">
            <span>AVG INVESTIGATION CYCLE</span>
            <AlertTriangle className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-purple-400 mt-2">
            {metrics.avg_investigation_time_mins} min
          </div>
          <div className="text-xs text-gray-400 mt-1">Accelerated via Groq LLaMA 3.3</div>
        </div>

      </div>

      {/* Middle Grid: Typology Exposure & Risk Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Fraud Typologies Table */}
        <div className="bg-[#111827] border border-gray-800 p-5 rounded-xl shadow-sm">
          <h3 className="text-base font-bold text-white mb-4">Fraud Typology Financial Exposure</h3>
          <div className="divide-y divide-gray-800">
            {metrics.top_fraud_typologies.map((t, idx) => (
              <div key={idx} className="py-3 flex items-center justify-between text-xs">
                <div>
                  <div className="font-semibold text-gray-200">{t.typology}</div>
                  <div className="text-gray-400 text-[11px] font-mono">{t.count} incidents intercepted</div>
                </div>
                <div className="text-right">
                  <div className="font-mono font-bold text-red-400">${t.loss_exposure.toLocaleString()}</div>
                  <div className="text-[10px] text-gray-500 uppercase">Exposure</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Risk Distribution Breakdown */}
        <div className="bg-[#111827] border border-gray-800 p-5 rounded-xl shadow-sm">
          <h3 className="text-base font-bold text-white mb-4">Transaction Risk Distribution</h3>
          <div className="space-y-4">
            {Object.entries(metrics.risk_distribution).map(([category, count]) => {
              const pct = Math.round((count / (metrics.total_transactions || 1)) * 100);
              return (
                <div key={category} className="space-y-1.5">
                  <div className="flex justify-between text-xs font-medium">
                    <span className="text-gray-300">{category}</span>
                    <span className="text-gray-400 font-mono">{count} txns ({pct}%)</span>
                  </div>
                  <div className="w-full bg-gray-800 h-2 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${
                        category.includes('High') ? 'bg-red-500' : (category.includes('Medium') ? 'bg-amber-500' : 'bg-blue-500')
                      }`}
                      style={{ width: `${Math.max(pct, 4)}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

      </div>

      {/* Weekly Trend Table */}
      <div className="bg-[#111827] border border-gray-800 p-5 rounded-xl shadow-sm">
        <h3 className="text-base font-bold text-white mb-3">7-Day Transaction vs Fraud Intercept Trends</h3>
        <div className="grid grid-cols-7 gap-2 text-center text-xs font-mono">
          {metrics.daily_volume_trend.map((d, i) => (
            <div key={i} className="bg-gray-900/60 p-3 rounded-lg border border-gray-800">
              <div className="font-bold text-gray-300">{d.day}</div>
              <div className="text-[11px] text-gray-400 mt-1">${(d.legit_volume / 1000).toFixed(0)}k vol</div>
              <div className="text-[11px] text-red-400 font-bold mt-0.5">${d.fraud_attempted} risk</div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
