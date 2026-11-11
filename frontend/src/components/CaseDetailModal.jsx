import React, { useState, useEffect } from 'react';
import { X, Sparkles, ShieldAlert, Ban, CheckCircle, AlertOctagon, Share2, Network, History } from 'lucide-react';
import GraphView from './GraphView';

export default function CaseDetailModal({ caseItem, onClose, onRefreshData }) {
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [aiLoading, setAiLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('dossier'); // 'dossier', 'graph', 'audit'

  useEffect(() => {
    fetchCaseDetail();
  }, [caseItem.id]);

  const fetchCaseDetail = async () => {
    try {
      const res = await fetch(`/api/cases/${caseItem.id}`);
      const data = await res.json();
      setDetail(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateAI = async () => {
    setAiLoading(true);
    try {
      const res = await fetch(`/api/cases/${caseItem.id}/ai-summarize`, { method: 'POST' });
      await res.json();
      await fetchCaseDetail();
      onRefreshData();
    } catch (err) {
      console.error(err);
    } finally {
      setAiLoading(false);
    }
  };

  const handleAction = async (actionType) => {
    const note = prompt(`Enter investigator justification for ${actionType}:`, "Verified anomalous behavior violating Trust & Safety Policy 4.1.");
    if (!note) return;

    try {
      await fetch(`/api/cases/${caseItem.id}/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: actionType, notes: note })
      });
      await fetchCaseDetail();
      onRefreshData();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading || !detail) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">
        <div className="text-white font-mono text-sm animate-pulse">Loading Sentinel Forensic Dossier...</div>
      </div>
    );
  }

  const { case: c, account, transaction, audit_logs } = detail;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 overflow-y-auto">
      <div className="bg-[#0F172A] border border-gray-800 rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
        
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-800 flex items-center justify-between bg-[#131D33]">
          <div className="flex items-center space-x-3">
            <span className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/40">
              {c.id}
            </span>
            <h2 className="text-lg font-bold text-white">{c.title}</h2>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation Tabs Inside Modal */}
        <div className="px-6 border-b border-gray-800 bg-[#0F172A] flex space-x-6">
          <button
            onClick={() => setActiveTab('dossier')}
            className={`py-3 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'dossier' ? 'border-blue-500 text-blue-400' : 'border-transparent text-gray-400 hover:text-gray-200'
            }`}
          >
            Forensic Dossier
          </button>
          <button
            onClick={() => setActiveTab('graph')}
            className={`py-3 text-sm font-medium border-b-2 transition-colors flex items-center space-x-1.5 ${
              activeTab === 'graph' ? 'border-blue-500 text-blue-400' : 'border-transparent text-gray-400 hover:text-gray-200'
            }`}
          >
            <Network className="w-4 h-4" />
            <span>Fraud Network Graph</span>
          </button>
          <button
            onClick={() => setActiveTab('audit')}
            className={`py-3 text-sm font-medium border-b-2 transition-colors flex items-center space-x-1.5 ${
              activeTab === 'audit' ? 'border-blue-500 text-blue-400' : 'border-transparent text-gray-400 hover:text-gray-200'
            }`}
          >
            <History className="w-4 h-4" />
            <span>Audit Trail ({audit_logs.length})</span>
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1">
          
          {activeTab === 'dossier' && (
            <>
              {/* Account & Risk Metric Overview */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-[#17223B] p-4 rounded-xl border border-gray-800">
                  <div className="text-xs text-gray-400 font-medium">ACCOUNT PROFILE</div>
                  <div className="text-base font-bold text-white mt-1">{account.full_name}</div>
                  <div className="text-xs text-gray-400 font-mono mt-0.5">{account.id} • {account.country}</div>
                  <div className="mt-2 text-xs">
                    Status: <span className="uppercase font-bold text-amber-400">{account.status}</span>
                  </div>
                </div>

                <div className="bg-[#17223B] p-4 rounded-xl border border-gray-800">
                  <div className="text-xs text-gray-400 font-medium">ML RISK EVALUATION</div>
                  <div className="text-2xl font-bold font-mono text-red-400 mt-1">{c.risk_score.toFixed(1)} / 100</div>
                  <div className="text-xs text-gray-400 mt-1">Priority: <strong className="text-white">{c.priority}</strong></div>
                  <div className="text-xs text-gray-400">Typology: <strong className="text-indigo-400">{c.fraud_typology || 'Anomalous Activity'}</strong></div>
                </div>

                <div className="bg-[#17223B] p-4 rounded-xl border border-gray-800">
                  <div className="text-xs text-gray-400 font-medium">INTERCEPTED TRANSACTION</div>
                  {transaction ? (
                    <>
                      <div className="text-xl font-bold font-mono text-white mt-1">
                        ${transaction.amount.toFixed(2)} {transaction.currency}
                      </div>
                      <div className="text-xs text-gray-300 mt-1">{transaction.merchant} ({transaction.merchant_category})</div>
                      <div className="text-xs text-gray-400 font-mono">IP: {transaction.ip_address}</div>
                    </>
                  ) : (
                    <div className="text-xs text-gray-400 mt-2">Aggregated account-level alert</div>
                  )}
                </div>
              </div>

              {/* AI Forensic Synthesizer */}
              <div className="bg-gradient-to-r from-blue-950/40 via-indigo-950/30 to-purple-950/20 border border-blue-500/30 rounded-xl p-5 relative">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    <Sparkles className="w-5 h-5 text-blue-400" />
                    <h3 className="text-sm font-bold text-white tracking-wide uppercase">
                      Groq LLaMA 3.3 Forensic Case Synthesis
                    </h3>
                  </div>
                  <button
                    onClick={handleGenerateAI}
                    disabled={aiLoading}
                    className="flex items-center space-x-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-semibold shadow-md shadow-blue-600/30 transition-all disabled:opacity-50"
                  >
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>{aiLoading ? 'Synthesizing Signals...' : 'Run LLaMA 3.3 Analysis'}</span>
                  </button>
                </div>

                {c.ai_summary ? (
                  <div className="space-y-3">
                    <p className="text-sm text-gray-200 leading-relaxed font-sans bg-gray-900/60 p-3 rounded-lg border border-gray-800">
                      {c.ai_summary}
                    </p>
                    <div className="flex flex-wrap items-center gap-3 pt-1 text-xs">
                      <span className="font-semibold text-gray-300">
                        Recommended Action: <span className="font-mono text-amber-400 font-bold">{c.ai_recommendation || 'REQUEST_IDV'}</span>
                      </span>
                      <span className="text-gray-400 font-mono">
                        Confidence: <strong className="text-emerald-400">{c.ai_confidence || 85}%</strong>
                      </span>
                    </div>
                  </div>
                ) : (
                  <p className="text-xs text-gray-400 italic">
                    Click "Run LLaMA 3.3 Analysis" to generate real-time AI case summaries and evidence-backed recommendations via Groq.
                  </p>
                )}
              </div>

              {/* Triggered Rule Flags */}
              {transaction && transaction.rule_flags && (
                <div>
                  <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Deterministic Flags Triggered</h4>
                  <div className="flex flex-wrap gap-2">
                    {transaction.rule_flags.map((flag, idx) => (
                      <span key={idx} className="px-2.5 py-1 rounded bg-red-950/60 border border-red-800 text-red-300 text-xs font-mono font-medium">
                        {flag}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}

          {activeTab === 'graph' && (
            <GraphView accountId={c.account_id} />
          )}

          {activeTab === 'audit' && (
            <div className="space-y-3">
              <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider">Immutable Chain of Custody</h4>
              <div className="border border-gray-800 rounded-xl divide-y divide-gray-800 bg-[#111827]">
                {audit_logs.map(log => (
                  <div key={log.id} className="p-3 text-xs flex justify-between items-start">
                    <div>
                      <span className="font-mono font-bold text-blue-400">{log.action}</span>
                      <p className="text-gray-300 mt-0.5">{log.notes}</p>
                    </div>
                    <span className="text-gray-500 font-mono text-[11px]">
                      {new Date(log.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

        </div>

        {/* Footer Enforcement Actions */}
        <div className="px-6 py-4 border-t border-gray-800 bg-[#131D33] flex flex-wrap items-center justify-between gap-3">
          <div className="text-xs text-gray-400 font-mono">
            Current Case State: <strong className="text-white uppercase">{c.status}</strong>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => handleAction('FLAG_FALSE_POSITIVE')}
              className="flex items-center space-x-1.5 px-3 py-2 bg-emerald-600/20 hover:bg-emerald-600 text-emerald-300 hover:text-white rounded-lg text-xs font-semibold border border-emerald-500/40 transition-colors"
            >
              <CheckCircle className="w-3.5 h-3.5" />
              <span>Dismiss (False Positive)</span>
            </button>

            <button
              onClick={() => handleAction('RESTRICT_CARD')}
              className="flex items-center space-x-1.5 px-3 py-2 bg-amber-600/20 hover:bg-amber-600 text-amber-300 hover:text-white rounded-lg text-xs font-semibold border border-amber-500/40 transition-colors"
            >
              <AlertOctagon className="w-3.5 h-3.5" />
              <span>Restrict Payments</span>
            </button>

            <button
              onClick={() => handleAction('BAN_ACCOUNT')}
              className="flex items-center space-x-1.5 px-3.5 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg text-xs font-semibold shadow-md shadow-red-600/30 transition-colors"
            >
              <Ban className="w-3.5 h-3.5" />
              <span>Ban Account & Entities</span>
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
