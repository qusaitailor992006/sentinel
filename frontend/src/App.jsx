import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import TriageQueue from './components/TriageQueue';
import ExecutiveDashboard from './components/ExecutiveDashboard';
import LiveSimulator from './components/LiveSimulator';
import CaseDetailModal from './components/CaseDetailModal';
import { Shield, BookOpen, Layers, Terminal } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('triage');
  const [cases, setCases] = useState([]);
  const [selectedCase, setSelectedCase] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCases();
  }, []);

  const fetchCases = async () => {
    try {
      const res = await fetch('/api/cases');
      const data = await res.json();
      setCases(data);
    } catch (err) {
      console.error("Failed to load cases:", err);
    } finally {
      setLoading(false);
    }
  };

  const pendingCount = cases.filter(c => c.status === 'NEW' || c.status === 'UNDER_REVIEW').length;

  return (
    <div className="min-h-screen flex flex-col bg-[#0A0E17] text-gray-100">
      
      {/* Top Navigation */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        pendingCasesCount={pendingCount}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {activeTab === 'triage' && (
          <TriageQueue
            cases={cases}
            onSelectCase={(c) => setSelectedCase(c)}
            onQuickAction={fetchCases}
          />
        )}

        {activeTab === 'analytics' && (
          <ExecutiveDashboard />
        )}

        {activeTab === 'simulator' && (
          <LiveSimulator onTransactionCreated={fetchCases} />
        )}

        {activeTab === 'docs' && (
          <div className="max-w-4xl mx-auto space-y-6">
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight">Enterprise Architecture & Specifications</h1>
              <p className="text-sm text-gray-400 mt-1">Core specifications, data schemas, and role play guidelines for interviews.</p>
            </div>

            <div className="bg-[#111827] border border-gray-800 rounded-xl p-6 space-y-4">
              <h3 className="text-base font-bold text-white flex items-center space-x-2">
                <Layers className="w-5 h-5 text-blue-400" />
                <span>Three-Tier Intelligence Architecture</span>
              </h3>
              <p className="text-sm text-gray-300 leading-relaxed">
                SENTINEL operates on a hybrid decision engine combining deterministic velocity rules, Scikit-learn unsupervised anomaly detection (Isolation Forest), and NetworkX multi-hop entity resolution to detect fraud rings sharing device hardware and proxy IP subnets.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2 text-xs font-mono">
                <div className="p-3 bg-gray-900 rounded-lg border border-gray-800">
                  <div className="text-blue-400 font-bold mb-1">Tier 1: Rules Engine</div>
                  <div className="text-gray-400">Velocity checks, geo-mismatches, threshold triggers.</div>
                </div>
                <div className="p-3 bg-gray-900 rounded-lg border border-gray-800">
                  <div className="text-purple-400 font-bold mb-1">Tier 2: ML & Graph</div>
                  <div className="text-gray-400">Isolation Forest (0.08 contamination) + NetworkX ego-networks.</div>
                </div>
                <div className="p-3 bg-gray-900 rounded-lg border border-gray-800">
                  <div className="text-emerald-400 font-bold mb-1">Tier 3: Groq LLaMA 3.3</div>
                  <div className="text-gray-400">Natural language case synthesis & automated justification.</div>
                </div>
              </div>
            </div>

            <div className="bg-[#111827] border border-gray-800 rounded-xl p-6 space-y-4">
              <h3 className="text-base font-bold text-white flex items-center space-x-2">
                <Terminal className="w-5 h-5 text-emerald-400" />
                <span>Interviewer Demonstration Flow (5 Minutes)</span>
              </h3>
              <ol className="list-decimal list-inside space-y-2 text-sm text-gray-300 font-sans">
                <li><strong className="text-white">Executive BI</strong>: Walk through prevented fraud loss ($30k+) and the False Positive Ratio (FPR).</li>
                <li><strong className="text-white">Incident Triage</strong>: Filter by priority (Critical/High), explain the Isolation Forest anomaly score.</li>
                <li><strong className="text-white">Entity Graph</strong>: Open Case 2024-003 to reveal 4 distinct accounts colluding over a shared emulator device.</li>
                <li><strong className="text-white">Forensic LLM</strong>: Click "Run LLaMA 3.3 Analysis" to generate an executive-ready evidence summary via Groq.</li>
                <li><strong className="text-white">Live Simulator</strong>: Inject a custom transaction live to show instant rule triggering and case generation.</li>
              </ol>
            </div>
          </div>
        )}

      </main>

      {/* Case Dossier Modal */}
      {selectedCase && (
        <CaseDetailModal
          caseItem={selectedCase}
          onClose={() => setSelectedCase(null)}
          onRefreshData={fetchCases}
        />
      )}

      {/* Footer */}
      <footer className="border-t border-gray-800/80 py-4 text-center text-xs text-gray-500 font-mono">
        SENTINEL Intelligence Platform • Built for Enterprise Portfolio & Technical Interviews
      </footer>

    </div>
  );
}
