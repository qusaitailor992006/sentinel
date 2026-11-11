import React, { useState, useEffect } from 'react';
import { Network, AlertCircle, Shield, Smartphone } from 'lucide-react';

export default function GraphView({ accountId }) {
  const [graphData, setGraphData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchGraph();
  }, [accountId]);

  const fetchGraph = async () => {
    try {
      const res = await fetch(`/api/graph/account/${accountId}`);
      const data = await res.json();
      setGraphData(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-gray-400 text-sm font-mono animate-pulse py-8 text-center">Traversing NetworkX Entity Clusters...</div>;
  }

  const { nodes = [], edges = [], summary = {} } = graphData || {};

  return (
    <div className="space-y-4">
      {/* Summary Banner */}
      <div className="bg-[#111827] border border-gray-800 rounded-xl p-4 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h4 className="text-sm font-bold text-white flex items-center space-x-2">
            <Network className="w-4 h-4 text-blue-400" />
            <span>Multi-Hop Entity Resolution Graph</span>
          </h4>
          <p className="text-xs text-gray-400 mt-0.5">
            Ego-network linking device tokens, proxy IPs, and co-operating accounts.
          </p>
        </div>

        <div className="flex items-center space-x-3 text-xs font-mono">
          <span className="px-2 py-1 rounded bg-gray-800 text-gray-300">
            Nodes: <strong>{summary.total_nodes || 0}</strong>
          </span>
          <span className="px-2 py-1 rounded bg-gray-800 text-gray-300">
            Edges: <strong>{summary.total_edges || 0}</strong>
          </span>
          {summary.has_syndicate && (
            <span className="px-2.5 py-1 rounded bg-red-950 border border-red-700 text-red-300 font-bold animate-pulse">
              SYNDICATE DETECTED
            </span>
          )}
        </div>
      </div>

      {/* Visual Canvas Representation */}
      <div className="bg-[#0B0F19] border border-gray-800 rounded-xl p-6 relative min-h-[320px] flex flex-col justify-center items-center">
        
        {nodes.length === 0 ? (
          <div className="text-gray-500 text-xs">No graph entities linked to this profile.</div>
        ) : (
          <div className="w-full grid grid-cols-1 md:grid-cols-2 gap-4">
            
            {/* Accounts Column */}
            <div className="space-y-3">
              <div className="text-xs font-mono font-bold text-gray-400 uppercase tracking-wider">
                Accounts Linked ({nodes.filter(n => n.data.type === 'account').length})
              </div>
              {nodes.filter(n => n.data.type === 'account').map(node => (
                <div
                  key={node.data.id}
                  className={`p-3 rounded-lg border text-xs flex items-center justify-between ${
                    node.data.is_target
                      ? 'bg-blue-950/40 border-blue-500 text-white shadow-md'
                      : 'bg-gray-900 border-gray-800 text-gray-300'
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <Shield className={`w-4 h-4 ${node.data.is_target ? 'text-blue-400' : 'text-gray-500'}`} />
                    <div>
                      <div className="font-bold">{node.data.label}</div>
                      <div className="text-[10px] text-gray-400 font-mono">{node.data.id}</div>
                    </div>
                  </div>
                  {node.data.risk_score && (
                    <span className="font-mono text-red-400 font-bold">
                      {node.data.risk_score.toFixed(1)}
                    </span>
                  )}
                </div>
              ))}
            </div>

            {/* Devices & Tokens Column */}
            <div className="space-y-3">
              <div className="text-xs font-mono font-bold text-gray-400 uppercase tracking-wider">
                Shared Hardware & IP Tokens ({nodes.filter(n => n.data.type === 'device').length})
              </div>
              {nodes.filter(n => n.data.type === 'device').map(node => (
                <div
                  key={node.data.id}
                  className="p-3 rounded-lg bg-gray-900 border border-gray-800 text-xs space-y-1 text-gray-300"
                >
                  <div className="flex items-center space-x-2">
                    <Smartphone className="w-4 h-4 text-purple-400" />
                    <span className="font-bold text-white">{node.data.label}</span>
                  </div>
                  <div className="font-mono text-[11px] text-gray-400">
                    IP Address: {node.data.ip || 'Unknown'} {node.data.is_vpn ? '(VPN/Proxy Flagged)' : ''}
                  </div>
                </div>
              ))}
            </div>

          </div>
        )}

      </div>
    </div>
  );
}
