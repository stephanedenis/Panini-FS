// API Client for Panini-FS REST API

import axios, { AxiosInstance } from 'axios';
import type {
  ApiResponse,
  ConceptListResponse,
  ConceptDetail,
  VersionDetail,
  TimelineResponse,
  SnapshotListResponse,
  SnapshotDetail,
  TimeTravelResponse,
  DiffResponse,
  StatsResponse,
} from '@/types/api';

class PaniniApiClient {
  private client: AxiosInstance;

  constructor(baseURL: string = '/api') {
    this.client = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  private async request<T>(
    method: string,
    url: string,
    data?: unknown
  ): Promise<T> {
    const response = await this.client.request<ApiResponse<T>>({
      method,
      url,
      data,
    });

    if (!response.data.success) {
      throw new Error(response.data.error || 'API request failed');
    }

    return response.data.data as T;
  }

  // Health check
  async health(): Promise<string> {
    return this.request<string>('GET', '/health');
  }

  // Concepts
  async listConcepts(): Promise<ConceptListResponse> {
    return this.request<ConceptListResponse>('GET', '/concepts');
  }

  async getConcept(id: string): Promise<ConceptDetail> {
    return this.request<ConceptDetail>('GET', `/concepts/${id}`);
  }

  async getVersion(
    conceptId: string,
    versionId: string
  ): Promise<VersionDetail> {
    return this.request<VersionDetail>(
      'GET',
      `/concepts/${conceptId}/versions/${versionId}`
    );
  }

  async getDiff(
    conceptId: string,
    from: string,
    to: string
  ): Promise<DiffResponse> {
    return this.request<DiffResponse>(
      'GET',
      `/concepts/${conceptId}/diff?from=${from}&to=${to}`
    );
  }

  // Timeline
  async getTimeline(
    start?: string,
    end?: string
  ): Promise<TimelineResponse> {
    const params = new URLSearchParams();
    if (start) params.append('start', start);
    if (end) params.append('end', end);
    
    const query = params.toString();
    return this.request<TimelineResponse>(
      'GET',
      `/timeline${query ? '?' + query : ''}`
    );
  }

  // Snapshots
  async listSnapshots(): Promise<SnapshotListResponse> {
    return this.request<SnapshotListResponse>('GET', '/snapshots');
  }

  async getSnapshot(id: string): Promise<SnapshotDetail> {
    return this.request<SnapshotDetail>('GET', `/snapshots/${id}`);
  }

  // Time travel
  async timeTravelQuery(timestamp: string): Promise<TimeTravelResponse> {
    return this.request<TimeTravelResponse>(
      'GET',
      `/time-travel?timestamp=${timestamp}`
    );
  }

  // Stats
  async getStats(): Promise<StatsResponse> {
    return this.request<StatsResponse>('GET', '/stats');
  }
}

// Export singleton instance
export const apiClient = new PaniniApiClient();
