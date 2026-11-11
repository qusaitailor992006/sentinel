import React from 'react';
import { Shield, Activity, BarChart3, Radio, FileText } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, pendingCasesCount = 3 }) {
  return (
    <header className="border-b border-gray-800 bg-[#0D131F]/90 backdrop-blur sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand */}
        <div className="flex items-center space-x-3">
          <div className="h-9 w-9 rounded-lg bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Shield className="w-5 h-5 text-white" />
          </div>
          <div>
            <span className="text-lg font-bold tracking-tight bg-gradient-to-r from-white via-gray-200 to-gray-400 bg-clip-text text-transparent">
              SENTINEL
            </span>
            <span className="text-[10px] uppercase font-mono px-2 py-0.5 ml-2 rounded bg-blue-500/10 border border-blue-500/30 text-blue-400 font-semibold tracking-wider">
              TRUST & SAFETY L4
            </span>
          </div>
        </div>

        {/* Tab Navigation */}
        <nav className="flex items-center space-x-1 sm:space-x-2">
          <button
            onClick={() => setActiveTab('triage')}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
              activeTab === 'triage'
                ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                : 'text-gray-400 hover:text-white hover:bg-gray-800/60'
            }`}
          >
            <Activity className="w-4 h-4" />
            <span>Incident Triage</span>
            {pendingCasesCount > 0 && (
              <span className="ml-1 px-1.5 py-0.2 rounded-full text-xs font-mono bg-red-500/30 text-red-300 border border-red-500/50">
                {pendingCasesCount}
              </span>
            )}
          </button>

          <button
            onClick={() => setActiveTab('analytics')}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
              activeTab === 'analytics'
                ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                : 'text-gray-400 hover:text-white hover:bg-gray-800/60'
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            <span>Executive BI</span>
          </button>

          <button
            onClick={() => setActiveTab('simulator')}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
              activeTab === 'simulator'
                ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                : 'text-gray-400 hover:text-white hover:bg-gray-800/60'
            }`}
          >
            <Radio className="w-4 h-4" />
            <span>Live Fraud Simulator</span>
          </button>

          <button
            onClick={() => setActiveTab('docs')}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
              activeTab === 'docs'
                ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                : 'text-gray-400 hover:text-white hover:bg-gray-800/60'
            }`}
          >
            <FileText className="w-4 h-4" />
            <span>BRD & Architecture</span>
          </button>
        </nav>

        {/* Analyst Status Badge */}
        <div className="hidden lg:flex items-center space-x-3 text-xs text-gray-400 font-mono">
          <div className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></div>
          <span>GROQ LLaMA 3.3 ACTIVE</span>
        </div>

      </div>
    </header>
  );
}
