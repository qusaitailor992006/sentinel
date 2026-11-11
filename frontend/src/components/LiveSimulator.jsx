import React, { useState } from 'react';
import { Radio, Send, CheckCircle, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function LiveSimulator({ onTransactionCreated }) {
  const [amount, setAmount] = useState(1250);
  const [merchant, setMerchant] = useState('Apple Store Online');
  const [category, setCategory] = useState('electronics');
  const [accountId, setAccountId] = useState('ACC-1010');
  const [isForeign, setIsForeign] = useState(true);
  const [isVpn, setIsVpn] = useState(true);
  const [deviceAnomaly, setDeviceAnomaly] = useState(true);
  const [velocity, setVelocity] = useState(4);
  const [submitting, setSubmitting] = useState(false);
  const [lastResult, setLastResult] = useState(null);

  const handleSimulate = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setLastResult(null);

    try {
      const res = await fetch('/api/transactions/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          account_id: accountId,
          amount: parseFloat(amount),
          merchant,
          merchant_category: category,
          payment_method: 'credit_card',
          is_foreign_ip: isForeign,
          is_vpn: isVpn,
          device_anomaly: deviceAnomaly,
          velocity_1h: parseInt(velocity)
        })
      });
      const data = await res.json();
      setLastResult(data);
      if (onTransactionCreated) onTransactionCreated();
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight flex items-center space-x-2">
          <Radio className="w-6 h-6 text-blue-500 animate-pulse" />
          <span>Real-Time Fraud Ingestion Simulator</span>
        </h1>
        <p className="text-sm text-gray-400 mt-1">
          Inject synthetic transactions live during interviews to demonstrate real-time scoring and auto-triage case generation.
        </p>
      </div>

      <div className="bg-[#111827] border border-gray-800 rounded-2xl p-6 shadow-xl">
        <form onSubmit={handleSimulate} className="space-y-5">
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-gray-300 uppercase mb-1">Target Account ID</label>
              <input
                type="text"
                value={accountId}
                onChange={(e) => setAccountId(e.target.value)}
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500 font-mono"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-300 uppercase mb-1">Transaction Amount ($ USD)</label>
              <input
                type="number"
                step="0.01"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500 font-mono"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-gray-300 uppercase mb-1">Merchant Name</label>
              <input
                type="text"
                value={merchant}
                onChange={(e) => setMerchant(e.target.value)}
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-300 uppercase mb-1">1-Hour Velocity Spike</label>
              <input
                type="number"
                min="1"
                max="20"
                value={velocity}
                onChange={(e) => setVelocity(e.target.value)}
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500 font-mono"
                required
              />
            </div>
          </div>

          {/* Anomaly Checkboxes */}
          <div className="bg-gray-900/60 p-4 rounded-xl border border-gray-800 space-y-3">
            <span className="text-xs font-bold text-gray-300 uppercase tracking-wider block">Risk Signal Overrides</span>
            
            <div className="flex flex-wrap gap-4 text-xs text-gray-200">
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={isForeign}
                  onChange={(e) => setIsForeign(e.target.checked)}
                  className="rounded bg-gray-800 border-gray-700 text-blue-600 focus:ring-0"
                />
                <span>Foreign Geolocation</span>
              </label>

              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={isVpn}
                  onChange={(e) => setIsVpn(e.target.checked)}
                  className="rounded bg-gray-800 border-gray-700 text-blue-600 focus:ring-0"
                />
                <span>Anonymous Proxy / VPN</span>
              </label>

              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={deviceAnomaly}
                  onChange={(e) => setDeviceAnomaly(e.target.checked)}
                  className="rounded bg-gray-800 border-gray-700 text-blue-600 focus:ring-0"
                />
                <span>Device Fingerprint Drift</span>
              </label>
            </div>
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-xl shadow-lg shadow-blue-600/30 transition-all flex items-center justify-center space-x-2 disabled:opacity-50 text-sm"
          >
            <Send className="w-4 h-4" />
            <span>{submitting ? 'Scoring via ML Engine...' : 'Inject & Score Transaction Live'}</span>
          </button>
        </form>

        {/* Live Evaluation Result Card */}
        {lastResult && (
          <div className="mt-6 p-4 rounded-xl border border-gray-800 bg-[#0B0F19] space-y-3 animate-fade-in">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono font-bold text-gray-400">RESULT: {lastResult.id}</span>
              <span className={`text-xs font-bold px-2.5 py-0.5 rounded ${
                lastResult.ml_risk_score > 65 ? 'bg-red-500/20 text-red-300 border border-red-500/40' : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
              }`}>
                {lastResult.ml_risk_score > 65 ? 'CASE CREATED' : 'PASSED'}
              </span>
            </div>

            <div className="flex items-center space-x-4">
              <div>
                <div className="text-xs text-gray-400">Calculated Risk Score</div>
                <div className="text-2xl font-bold font-mono text-white">{lastResult.ml_risk_score.toFixed(1)} / 100</div>
              </div>
              <div>
                <div className="text-xs text-gray-400">Isolation Anomaly</div>
                <div className="text-2xl font-bold font-mono text-purple-400">{lastResult.anomaly_score.toFixed(3)}</div>
              </div>
            </div>

            {lastResult.rule_flags.length > 0 && (
              <div className="flex flex-wrap gap-1.5 pt-1">
                {lastResult.rule_flags.map((f, i) => (
                  <span key={i} className="px-2 py-0.5 rounded bg-red-950 text-red-300 text-[11px] font-mono border border-red-800">
                    {f}
                  </span>
                ))}
              </div>
            )}
          </div>
        )}

      </div>
    </div>
  );
}
