export interface PatientSummary {
  id: string;
  anonymized_code: string;
  preferred_language: string;
  age?: number;
}

export interface ActivityTrend {
  date: string;
  engagementScore: number;
  activityName: string;
}

export interface AlertNotification {
  id: string;
  patientCode: string;
  label: string;
  timestamp: string;
  severity: 'low' | 'medium' | 'high';
}
