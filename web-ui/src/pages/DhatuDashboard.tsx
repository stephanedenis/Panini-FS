import React, { useState, useEffect } from 'react';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, Legend, Tooltip } from 'recharts';

interface EmotionInfo {
  name: string;
  sanskrit: string;
  devanagari: string;
  description: string;
  neurotransmitter: string;
  color: string;
}

interface EmotionalIntensity {
  seeking: number;
  fear: number;
  rage: number;
  lust: number;
  care: number;
  panic_grief: number;
  play: number;
}

interface ClassifyResult {
  intensity: EmotionalIntensity;
  dominant: string | null;
  arousal: number;
}

interface EmotionStats {
  total_profiles: number;
  emotion_distribution: Record<string, number>;
  average_arousal: number;
  top_emotions: [string, number][];
}

const DhatuDashboard: React.FC = () => {
  const [emotions, setEmotions] = useState<EmotionInfo[]>([]);
  const [stats, setStats] = useState<EmotionStats | null>(null);
  const [classifyText, setClassifyText] = useState('');
  const [classifyResult, setClassifyResult] = useState<ClassifyResult | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadEmotions();
    loadStats();
  }, []);

  const loadEmotions = async () => {
    try {
      const response = await fetch('http://localhost:3000/api/dhatu/emotions');
      const data = await response.json();
      setEmotions(data.emotions);
    } catch (error) {
      console.error('Failed to load emotions:', error);
    }
  };

  const loadStats = async () => {
    try {
      const response = await fetch('http://localhost:3000/api/dhatu/stats');
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  };

  const handleClassify = async () => {
    if (!classifyText.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch('http://localhost:3000/api/dhatu/classify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: classifyText }),
      });
      const data = await response.json();
      setClassifyResult(data);
      await loadStats();
    } catch (error) {
      console.error('Failed to classify:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRadarData = (intensity?: EmotionalIntensity) => {
    if (!intensity) return [];
    
    return [
      { emotion: 'SEEKING', value: intensity.seeking * 100, fullMark: 100 },
      { emotion: 'FEAR', value: intensity.fear * 100, fullMark: 100 },
      { emotion: 'RAGE', value: intensity.rage * 100, fullMark: 100 },
      { emotion: 'LUST', value: intensity.lust * 100, fullMark: 100 },
      { emotion: 'CARE', value: intensity.care * 100, fullMark: 100 },
      { emotion: 'PANIC/GRIEF', value: intensity.panic_grief * 100, fullMark: 100 },
      { emotion: 'PLAY', value: intensity.play * 100, fullMark: 100 },
    ];
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-4xl font-bold mb-2">Dhātu 🪷 Emotional Classification</h1>
      <p className="text-gray-600 mb-8">
        Based on Panksepp's seven primary emotional systems
      </p>

      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Total Profiles</h3>
            <p className="text-4xl font-bold text-blue-600">{stats.total_profiles}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Avg Arousal</h3>
            <p className="text-4xl font-bold text-green-600">{stats.average_arousal.toFixed(2)}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Top Emotion</h3>
            <p className="text-2xl font-bold text-purple-600">
              {stats.top_emotions[0] ? stats.top_emotions[0][0] : 'N/A'}
            </p>
            <p className="text-sm text-gray-500">
              {stats.top_emotions[0] ? `${stats.top_emotions[0][1]} files` : ''}
            </p>
          </div>
        </div>
      )}

      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h2 className="text-2xl font-bold mb-4">Seven Primary Emotions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {emotions.map((emotion) => (
            <div 
              key={emotion.name}
              className="border rounded-lg p-4 hover:shadow-md transition-shadow"
              style={{ borderLeft: \`4px solid \${emotion.color}\` }}
            >
              <h3 className="font-bold text-lg mb-1">{emotion.name}</h3>
              <p className="text-2xl mb-2">{emotion.devanagari}</p>
              <p className="text-sm text-gray-600 mb-1">{emotion.sanskrit}</p>
              <p className="text-xs text-gray-500 mb-2">{emotion.description}</p>
              <p className="text-xs text-gray-400">
                <strong>NT:</strong> {emotion.neurotransmitter}
              </p>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h2 className="text-2xl font-bold mb-4">Classify Text</h2>
        <textarea
          className="w-full border rounded p-3 mb-4 h-32"
          placeholder="Enter text to classify emotional content..."
          value={classifyText}
          onChange={(e) => setClassifyText(e.target.value)}
        />
        <button
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
          onClick={handleClassify}
          disabled={loading || !classifyText.trim()}
        >
          {loading ? 'Classifying...' : 'Classify Emotion'}
        </button>

        {classifyResult && (
          <div className="mt-6">
            <div className="flex items-center gap-4 mb-4">
              <div className="bg-purple-100 px-4 py-2 rounded">
                <span className="text-sm text-gray-600">Dominant: </span>
                <span className="font-bold text-purple-700">
                  {classifyResult.dominant || 'None'}
                </span>
              </div>
              <div className="bg-green-100 px-4 py-2 rounded">
                <span className="text-sm text-gray-600">Arousal: </span>
                <span className="font-bold text-green-700">
                  {classifyResult.arousal.toFixed(2)}
                </span>
              </div>
            </div>

            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="text-lg font-semibold mb-4 text-center">Emotional Profile</h3>
              <ResponsiveContainer width="100%" height={400}>
                <RadarChart data={getRadarData(classifyResult.intensity)}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="emotion" />
                  <PolarRadiusAxis angle={90} domain={[0, 100]} />
                  <Radar
                    name="Intensity"
                    dataKey="value"
                    stroke="#8b5cf6"
                    fill="#8b5cf6"
                    fillOpacity={0.6}
                  />
                  <Legend />
                  <Tooltip />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </div>

      {stats && stats.total_profiles > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold mb-4">Emotion Distribution</h2>
          <div className="space-y-3">
            {stats.top_emotions.map(([emotion, count]) => {
              const percentage = (count / stats.total_profiles) * 100;
              return (
                <div key={emotion}>
                  <div className="flex justify-between mb-1">
                    <span className="font-medium">{emotion}</span>
                    <span className="text-gray-600">{count} files ({percentage.toFixed(1)}%)</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all"
                      style={{ width: \`\${percentage}%\` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

export default DhatuDashboard;
