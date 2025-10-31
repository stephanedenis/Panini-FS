// API Types for Panini-FS

export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error: string | null;
}

export interface ConceptSummary {
  id: string;
  name: string;
  current_version: string;
  version_count: number;
  created_at: string;
  updated_at: string;
}

export interface ConceptListResponse {
  concepts: ConceptSummary[];
  total: number;
}

export interface VersionSummary {
  version_id: string;
  parent: string | null;
  timestamp: string;
  author: string;
  message: string;
  size: number;
  atom_count: number;
}

export interface ConceptDetail {
  id: string;
  name: string;
  current_version: string;
  versions: VersionSummary[];
  created_at: string;
  updated_at: string;
  metadata: Record<string, string>;
}

export interface VersionDetail {
  version_id: string;
  parent: string | null;
  atoms: string[];
  size: number;
  content_hash: string;
  timestamp: string;
  author: string;
  message: string;
  metadata: Record<string, string>;
}

export type TimelineEventType = 
  | 'ConceptCreated'
  | 'ConceptModified'
  | 'SnapshotCreated';

export interface TimelineEvent {
  type: TimelineEventType;
  timestamp: string;
  concept_id?: string;
  concept_name?: string;
  version_id?: string;
  previous_version?: string;
  snapshot_id?: string;
  snapshot_name?: string;
}

export interface TimelineResponse {
  events: TimelineEvent[];
  total: number;
}

export interface SnapshotSummary {
  id: string;
  name: string;
  timestamp: string;
  concept_count: number;
}

export interface SnapshotListResponse {
  snapshots: SnapshotSummary[];
  total: number;
}

export interface SnapshotDetail {
  id: string;
  name: string;
  timestamp: string;
  concepts: Record<string, string>;
  metadata: Record<string, string>;
}

export interface DiffResponse {
  from: string;
  to: string;
  added_atoms: string[];
  removed_atoms: string[];
  size_change: number;
}

export interface TimeTravelResponse {
  timestamp: string;
  concepts: Record<string, string>;
}

export interface StatsResponse {
  total_concepts: number;
  total_versions: number;
  total_snapshots: number;
  total_atoms: number;
  total_size: number;
  dedup_savings: number;
}
