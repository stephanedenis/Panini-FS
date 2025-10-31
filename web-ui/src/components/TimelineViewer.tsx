import { format } from 'date-fns';
import type { TimelineEvent } from '@/types/api';
import {
  FileText,
  Edit,
  Camera,
  Clock,
} from 'lucide-react';

interface TimelineViewerProps {
  events: TimelineEvent[];
}

export function TimelineViewer({ events }: TimelineViewerProps) {
  if (events.length === 0) {
    return (
      <div className="bg-gray-800 rounded-lg p-12 border border-gray-700 text-center">
        <Clock className="w-16 h-16 text-gray-600 mx-auto mb-4" />
        <p className="text-gray-400 text-lg">No timeline events yet</p>
        <p className="text-gray-500 text-sm mt-2">
          Create concepts to see activity here
        </p>
      </div>
    );
  }

  const getEventIcon = (type: string) => {
    switch (type) {
      case 'ConceptCreated':
        return <FileText className="w-5 h-5" />;
      case 'ConceptModified':
        return <Edit className="w-5 h-5" />;
      case 'SnapshotCreated':
        return <Camera className="w-5 h-5" />;
      default:
        return <Clock className="w-5 h-5" />;
    }
  };

  const getEventColor = (type: string) => {
    switch (type) {
      case 'ConceptCreated':
        return 'bg-green-500';
      case 'ConceptModified':
        return 'bg-blue-500';
      case 'SnapshotCreated':
        return 'bg-purple-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getEventText = (event: TimelineEvent) => {
    switch (event.type) {
      case 'ConceptCreated':
        return (
          <>
            Created concept <span className="font-semibold">{event.concept_name}</span>
          </>
        );
      case 'ConceptModified':
        return (
          <>
            Modified <span className="font-semibold">{event.concept_name}</span>
            {event.previous_version && (
              <span className="text-gray-500 text-sm ml-2">
                (v{event.previous_version} → v{event.version_id})
              </span>
            )}
          </>
        );
      case 'SnapshotCreated':
        return (
          <>
            Created snapshot <span className="font-semibold">{event.snapshot_name}</span>
          </>
        );
      default:
        return 'Unknown event';
    }
  };

  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700">
      <div className="p-6">
        <div className="space-y-6">
          {events.map((event, index) => (
            <div key={index} className="flex items-start space-x-4">
              {/* Timeline line */}
              <div className="flex flex-col items-center">
                <div
                  className={`
                    ${getEventColor(event.type)}
                    rounded-full p-2 text-white
                  `}
                >
                  {getEventIcon(event.type)}
                </div>
                {index < events.length - 1 && (
                  <div className="w-0.5 h-full bg-gray-700 mt-2 flex-1 min-h-[40px]" />
                )}
              </div>

              {/* Event content */}
              <div className="flex-1 pb-8">
                <div className="bg-gray-750 rounded-lg p-4 border border-gray-600">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <p className="text-gray-200">
                        {getEventText(event)}
                      </p>
                      <p className="text-sm text-gray-400 mt-1">
                        {format(new Date(event.timestamp), 'PPpp')}
                      </p>
                    </div>
                    {event.concept_id && (
                      <button
                        className="
                          px-3 py-1 text-sm
                          bg-gray-700 hover:bg-gray-600
                          border border-gray-600
                          rounded
                          text-gray-300
                          transition-colors
                        "
                        onClick={() => {
                          // Navigate to concept detail
                          window.location.href = `/concepts/${event.concept_id}`;
                        }}
                      >
                        View
                      </button>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
