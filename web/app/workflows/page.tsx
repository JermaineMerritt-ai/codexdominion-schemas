'use client';

import React, { useEffect, useState } from 'react';
import { fetchWorkflowTypes, fetchWorkflowMetrics, WorkflowType, WorkflowMetrics } from '@/lib/api/workflows';

export default function WorkflowDashboard() {
  const [workflowTypes, setWorkflowTypes] = useState<Record<string, WorkflowType>>({});
  const [metrics, setMetrics] = useState<WorkflowMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const [types, metricsData] = await Promise.all([
          fetchWorkflowTypes(),
          fetchWorkflowMetrics()
        ]);
        setWorkflowTypes(types);
        setMetrics(metricsData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load data');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-100 p-8">
        <div className="max-w-7xl mx-auto">
          <p className="text-slate-400">Loading workflow data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-100 p-8">
        <div className="max-w-7xl mx-auto">
          <p className="text-red-400">Error: {error}</p>
        </div>
      </div>
    );
  }

  const typeCount = Object.keys(workflowTypes).length;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="border-b border-slate-800 pb-6">
          <h1 className="text-4xl font-bold text-emerald-400">Workflow Dashboard</h1>
          <p className="text-slate-400 mt-2">Automation workflows and performance metrics</p>
        </div>

        {/* Metrics Grid */}
        {metrics && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Total Actions */}
            <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
              <div className="text-slate-400 text-sm font-medium mb-2">Total Actions</div>
              <div className="text-3xl font-bold text-emerald-400">{metrics.total_actions}</div>
            </div>

            {/* Completed */}
            <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
              <div className="text-slate-400 text-sm font-medium mb-2">Completed</div>
              <div className="text-3xl font-bold text-green-400">{metrics.status_counts.completed}</div>
              <div className="text-xs text-slate-500 mt-1">
                Running: {metrics.status_counts.running}
              </div>
            </div>

            {/* Weekly Savings */}
            <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
              <div className="text-slate-400 text-sm font-medium mb-2">Weekly Savings</div>
              <div className="text-3xl font-bold text-emerald-400">
                ${metrics.total_savings.weekly.toLocaleString(undefined, { maximumFractionDigits: 0 })}
              </div>
            </div>

            {/* Yearly Savings */}
            <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
              <div className="text-slate-400 text-sm font-medium mb-2">Yearly Savings</div>
              <div className="text-3xl font-bold text-emerald-400">
                ${metrics.total_savings.yearly.toLocaleString(undefined, { maximumFractionDigits: 0 })}
              </div>
            </div>
          </div>
        )}

        {/* Workflow Types */}
        <div>
          <h2 className="text-2xl font-bold text-slate-100 mb-4">
            Available Workflow Types ({typeCount})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Object.entries(workflowTypes).map(([id, type]) => (
              <div
                key={id}
                className="bg-slate-900 border border-slate-800 rounded-lg p-6 hover:border-emerald-500 transition-colors"
              >
                <div className="flex items-start justify-between mb-3">
                  <h3 className="text-lg font-semibold text-slate-100">{type.name}</h3>
                  <span className="text-xs px-2 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    {type.domain}
                  </span>
                </div>
                <p className="text-slate-400 text-sm mb-4">{type.description}</p>
                <div className="space-y-2">
                  <div className="text-xs text-slate-500">
                    <span className="font-medium">Category:</span> {type.category}
                  </div>
                  <div className="text-xs text-slate-500">
                    <span className="font-medium">Required Inputs:</span> {type.required_inputs.length}
                  </div>
                  {metrics && metrics.actions_by_type[`create_workflow_${id}`] && (
                    <div className="text-xs text-emerald-400 font-medium pt-2 border-t border-slate-800">
                      {metrics.actions_by_type[`create_workflow_${id}`]} active workflows
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Actions by Type */}
        {metrics && Object.keys(metrics.actions_by_type).length > 0 && (
          <div>
            <h2 className="text-2xl font-bold text-slate-100 mb-4">Actions by Type</h2>
            <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
              <div className="space-y-3">
                {Object.entries(metrics.actions_by_type).map(([type, count]) => (
                  <div key={type} className="flex items-center justify-between">
                    <span className="text-slate-300 font-mono text-sm">{type}</span>
                    <span className="text-emerald-400 font-bold">{count}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Status Distribution */}
        {metrics && (
          <div>
            <h2 className="text-2xl font-bold text-slate-100 mb-4">Status Distribution</h2>
            <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-yellow-400">{metrics.status_counts.pending}</div>
                  <div className="text-sm text-slate-400">Pending</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-400">{metrics.status_counts.running}</div>
                  <div className="text-sm text-slate-400">Running</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-400">{metrics.status_counts.completed}</div>
                  <div className="text-sm text-slate-400">Completed</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-400">{metrics.status_counts.failed}</div>
                  <div className="text-sm text-slate-400">Failed</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
