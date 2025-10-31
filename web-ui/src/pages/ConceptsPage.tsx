import { useState, useEffect } from 'react';
import { apiClient } from '@/api/client';
import type { ConceptSummary } from '@/types/api';
import { FileText, Search } from 'lucide-react';

export function ConceptsPage() {
  const [concepts, setConcepts] = useState<ConceptSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    async function fetchConcepts() {
      try {
        const data = await apiClient.listConcepts();
        setConcepts(data.concepts);
      } catch (err) {
        console.error('Failed to load concepts:', err);
      } finally {
        setLoading(false);
      }
    }

    fetchConcepts();
  }, []);

  const filteredConcepts = concepts.filter(c =>
    c.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div className="text-center py-12">Loading...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Concepts</h1>
        <div className="text-gray-400">
          {concepts.length} concept{concepts.length !== 1 ? 's' : ''}
        </div>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
        <input
          type="text"
          placeholder="Search concepts..."
          className="
            w-full pl-10 pr-4 py-3
            bg-gray-800 border border-gray-700 rounded-lg
            text-white placeholder-gray-400
            focus:outline-none focus:border-panini-blue
          "
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {/* Concepts List */}
      <div className="grid gap-4">
        {filteredConcepts.length === 0 ? (
          <div className="bg-gray-800 rounded-lg p-12 border border-gray-700 text-center">
            <FileText className="w-16 h-16 text-gray-600 mx-auto mb-4" />
            <p className="text-gray-400 text-lg">No concepts found</p>
          </div>
        ) : (
          filteredConcepts.map((concept) => (
            <div
              key={concept.id}
              className="bg-gray-800 border border-gray-700 rounded-lg p-6 hover:border-panini-blue transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3">
                    <FileText className="w-5 h-5 text-panini-blue" />
                    <h3 className="text-xl font-semibold text-white">
                      {concept.name}
                    </h3>
                  </div>
                  <div className="mt-3 flex items-center space-x-4 text-sm text-gray-400">
                    <span>ID: {concept.id}</span>
                    <span>•</span>
                    <span>{concept.version_count} versions</span>
                    <span>•</span>
                    <span>Current: {concept.current_version}</span>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
