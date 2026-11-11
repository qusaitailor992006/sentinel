import React, { useState } from 'react';
import { AlertTriangle, Clock, ArrowUpRight, Search, Filter, ShieldCheck, CheckCircle2, UserCheck } from 'lucide-react';

export default function TriageQueue({ cases, onSelectCase, onQuickAction }) {
  const [filter, setFilter] = useState('ALL');
  const [search, setSearch] = useState('');

  const filteredCases = cases.filter(c => {
    const matchesFilter = filter === 'ALL' || c.status === filter;
    const matchesSearch = c.title.toLowerCase().includes(search.toLowerCase()) ||
                          c.account_id.toLowerCase().includes(search.toLowerCase()) ||
                          c.id.toLowerCase().includes(search.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const getRiskBadge = (score) => {
    if (score >= 85) return 'bg-red-500/10 border-red-500/40 text-red-400';
    if (score >= 65) return 'bg-amber-500/10 border-amber-500/40 text-amber-400';
    return 'bg-blue-500/10 border-blue-500/40 text-blue-400';
  };

  const getPriorityBadge = (priority) => {
    switch (priority) {
      case 'CRITICAL': return 'bg-red-950 text-red-300 border-red-800';
      case 'HIGH': return 'bg-amber-950 text-amber-300 border-amber-800';
      case 'MEDIUM': return 'bg-blue-950 text-blue-300 border-blue-800';
      default: return 'bg-gray-800 text-gray-300 border-gray-700';
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Header & Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Active Investigation Triage</h1>
          <p className="text-sm text-gray-400 mt-1">
            Real-time queue prioritized by Scikit-Learn Isolation Forest & deterministic velocity rules.
          </p>
        </div>

        {/* Filter Buttons */}
        <div className="flex items-center space-x-2">
          {['ALL', 'NEW', 'UNDER_REVIEW', 'RESOLVED_FRAUD'].map(tab => (
            <button
              key={tab}
              onClick={() => setFilter(tab)}
              className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                filter === tab
                  ? 'bg-blue-600 text-white font-semibold'
                  : 'bg-gray-800/80 text-gray-400 hover:text-white hover:bg-gray-700'
              }`}
            >
              {tab.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Search Input */}
      <div className="relative">
        <Search className="w-4 h-4 text-gray-500 absolute left-3.5 top-3" />
        <input
          type="text"
          placeholder="Filter by Case ID, Account ID, or Typology..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full bg-[#111827] border border-gray-800 rounded-lg pl-10 pr-4 py-2 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors"
        />
      </div>

      {/* Cases List */}
      <div className="grid gap-3">
        {filteredCases.length === 0 ? (
          <div className="text-center py-12 bg-[#111827] rounded-xl border border-gray-800">
            <CheckCircle2 className="w-10 h-10 text-emerald-500 mx-auto mb-2 opacity-80" />
            <h3 className="text-base font-medium text-white">Queue Cleared</h3>
            <p className="text-sm text-gray-400">No open risk incidents matching current filters.</p>
          </div>
        ) : (
          filteredCases.map(c => (
            <div
              key={c.id}
              onClick={() => onSelectCase(c)}
              className="bg-[#111827] hover:bg-[#151E32] transition-all cursor-pointer rounded-xl border border-gray-800/80 hover:border-blue-500/50 p-4 sm:p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-sm"
            >
              {/* Left Details */}
              <div className="space-y-2 flex-1">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="font-mono text-xs font-bold text-gray-400 bg-gray-900 px-2 py-0.5 rounded border border-gray-800">
                    {c.id}
                  </span>
                  <span className={`text-[11px] font-bold px-2 py-0.5 rounded border ${getPriorityBadge(c.priority)}`}>
                    {c.priority}
                  </span>
                  <span className="text-xs text-gray-400 font-mono">
                    Account: <strong className="text-gray-200">{c.account_id}</strong>
                  </span>
                  {c.fraud_typology && (
                    <span className="text-xs font-medium px-2 py-0.5 rounded bg-indigo-950/60 text-indigo-300 border border-indigo-800/60">
                      {c.fraud_typology}
                    </span>
                  )}
                </div>

                <h3 className="text-base font-semibold text-white group-hover:text-blue-400 transition-colors">
                  {c.title}
                </h3>

                {c.ai_summary && (
                  <p className="text-xs text-gray-400 line-clamp-1 italic bg-gray-900/40 p-1.5 rounded border-l-2 border-blue-500">
                    " {c.ai_summary} "
                  </p>
                )}
              </div>

              {/* Right Scores & Quick Action */}
              <div className="flex items-center space-x-4 self-end md:self-center">
                {/* Risk Score Circle */}
                <div className={`px-3 py-2 rounded-lg border text-center ${getRiskBadge(c.risk_score)}`}>
                  <div className="text-lg font-bold font-mono tracking-tight">{c.risk_score.toFixed(1)}</div>
                  <div className="text-[10px] uppercase font-semibold tracking-wider">RISK SCORE</div>
                </div>

                {/* Inspect Button */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onSelectCase(c);
                  }}
                  className="flex items-center space-x-1 px-3.5 py-2 bg-blue-600/20 hover:bg-blue-600 text-blue-300 hover:text-white rounded-lg text-xs font-semibold border border-blue-500/30 transition-all shadow-sm"
                >
                  <span>Investigate</span>
                  <ArrowUpRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>

    </div>
  );
}
