import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { DatasetService } from '../services/dataset.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-chart-select',
  imports: [CommonModule, FormsModule],
  standalone: true,
  templateUrl: './chart-select.component.html',
  styleUrl: './chart-select.component.scss'
})
export class ChartSelectComponent implements OnInit{
  databases : string[] = [];
  // chartTypes = ['Scatter', 'Line', 'Histogram', 'KDE', 'ECD', 'Bar', 'Countplot'];
  chartTypes : string[] = [];

  selectedDatabase: string = '';
  selectedChart: string = '';
  formData: any = {};

  columns: { numerical: string[], categorical: string[] } = { numerical: [], categorical: [] };
  requiredFields: string[] = [];

  @Output() chartDataEvent = new EventEmitter<any>();

  constructor(private datasetService: DatasetService) {}

  ngOnInit() {
    // Fetch dataset names from FastAPI
    this.datasetService.getAvailableDatasets().subscribe(response => {
      console.log("API Response:", response);
      this.databases = response.available_datasets;
      this.chartTypes = response.available_charts;
      this.selectedDatabase = this.databases.length > 0 ? this.databases[0] : '';
      this.selectedChart = this.chartTypes.length > 0? this.chartTypes[0] : '';
    });
  }

  onDatabaseChange(): void {
    this.columns = { numerical: [], categorical: [] };
    this.requiredFields = [];
  }

  onChartChange(): void {
    if (this.selectedDatabase && this.selectedChart) {
      this.datasetService.getChartRequirements({
        dataset: this.selectedDatabase,
        chart: this.selectedChart
      }).subscribe((data) => {
        this.requiredFields = data.required_keys;
        this.columns.numerical = data.numerical_columns;
        this.columns.categorical = data.categorical_columns;
        this.formData = {};
      });
    }
  }

  generateChart(): void {
    const requestData = {
      dataset: this.selectedDatabase,
      chart: this.selectedChart,
      ...this.formData
    };

    this.datasetService.getChartRequirements(requestData).subscribe((chartData) => {
      this.chartDataEvent.emit(chartData); // Send data to parent (App Component)
    });
  }
}
