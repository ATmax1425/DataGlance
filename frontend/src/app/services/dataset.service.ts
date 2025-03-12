import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DatasetService {
  private apiUrl = 'http://0.0.0.0:8000/dataset'; // FastAPI URL

  constructor(private http: HttpClient) {}

  // Fetch available datasets
  getAvailableDatasets(): Observable<{ available_datasets: string[], available_charts: string[]}> {
    return this.http.get<{ available_datasets: string[], available_charts: string[]}>(this.apiUrl);
  }

  // Fetch selected dataset columns by name
  getDatasetColumns(datasetName: string): Observable<{ columns: string[] }> {
    return this.http.get<{ columns: string[] }>(`${this.apiUrl}/${datasetName}/columns`);
  }

  // Fetch selected dataset by name
  getDataset(datasetName: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/${datasetName}`);
  }

  getChartRequirements(requestBody: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/get-chart-requirements`, requestBody);
  }
  
}