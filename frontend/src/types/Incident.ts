export interface Incident {
  id: string;
  device_id: string;
  anomaly_type: string;
  latitude: number;
  longitude: number;
  timestamp: string;
}
