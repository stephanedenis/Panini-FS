import { useState, useEffect } from 'react';
import { apiClient } from '@/api/client';
import type { StatsResponse, TimelineEvent } from '@/types/api';
import { 
  BarChart3, 
  Database, 
  FileText, 
  GitBranch,
  Layers,
  HardDrive
} from 'lucide-react';
import { TimelineViewer } from '@/components/TimelineViewer';

export function Dashboard() {
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [recentEvents, setRecentEvents] = useState<TimelineEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const [statsData, timelineData] = await Promise.all([
          apiClient.getStats(),
          apiClient.getTimeline(),
        ]);
        
        setStats(statsData);
        setRecentEvents(timelineData.events.slice(0, 10));
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load data');
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-panini-blue"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-900/20 border border-red-500 rounded-lg p-6">
        <h2 className="text-red-400 font-semibold mb-2">Error loading dashboard</h2>
        <p className="text-red-300">{error}</p>
        <p className="text-sm text-gray-400 mt-4">
          Make sure the API server is running on <code>http://localhost:3000</code>
        </p>
      </div>
    );
  }

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`;
  };

  const dedupRatio = stats
    ? (stats.dedup_savings / (stats.total_size + stats.dedup_savings)) * 100
    : 0;

  return (
    <div className="space-y-8">
      {/* Stats Grid */}
      <div>
        <h2 className="text-2xl font-bold mb-4">System Overview</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {/* Total Concepts */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Total Concepts</p>
                <p className="text-3xl font-bold text-white mt-1">
                  {stats?.total_concepts || 0}
                </p>
              </div>
              <FileText className="w-12 h-12 text-panini-blue opacity-50" />
            </div>
          </div>

          {/* Total Versions */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Total Versions</p>
                <p className="text-3xl font-bold text-white mt-1">
                  {stats?.total_versions || 0}
                </p>
              </div>
              <GitBranch className="w-12 h-12 text-panini-purple opacity-50" />
            </div>
          </div>

          {/* Total Snapshots */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Snapshots</p>
                <p className="text-3xl font-bold text-white mt-1">
                  {stats?.total_snapshots || 0}
                </p>
              </div>
              <Layers className="w-12 h-12 text-green-500 opacity-50" />
            </div>
          </div>

          {/* Total Atoms */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Total Atoms</p>
                <p className="text-3xl font-bold text-white mt-1">
                  {stats?.total_atoms || 0}
                </p>
              </div>
              <Database className="w-12 h-12 text-yellow-500 opacity-50" />
            </div>
          </div>

          {/* Storage Size */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Storage Size</p>
                <p className="text-3xl font-bold text-white mt-1">
                  {stats ? formatBytes(stats.total_size) : '0 B'}
                </p>
              </div>
              <HardDrive className="w-12 h-12 text-orange-500 opacity-50" />
            </div>
          </div>

          {/* Deduplication */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Dedup Savings</p>
                <p className="text-3xl font-bold text-white mt-1">
                  {dedupRatio.toFixed(1)}%
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  {stats ? formatBytes(stats.dedup_savings) : '0 B'} saved
                </p>
              </div>
              <BarChart3 className="w-12 h-12 text-cyan-500 opacity-50" />
            </div>
          </div>
        </div>
      </div>

      {/* Timeline Viewer */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Recent Activity</h2>
        <TimelineViewer events={recentEvents} />
      </div>
    </div>
  );
}
