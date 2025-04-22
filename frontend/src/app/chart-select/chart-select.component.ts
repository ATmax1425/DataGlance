import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { DatasetService } from '../services/dataset.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChartTypeSelectComponent } from "./chart-type-select/chart-type-select.component";
import { ParameterSelectComponent } from "./parameter-select/parameter-select.component";

@Component({
  selector: 'app-chart-select',
  imports: [CommonModule, FormsModule, ChartTypeSelectComponent, ParameterSelectComponent],
  standalone: true,
  templateUrl: './chart-select.component.html',
  styleUrl: './chart-select.component.scss'
})
export class ChartSelectComponent implements OnInit{
  databases : any[] = [];
  // chartTypes = ['Scatter', 'Line', 'Histogram', 'KDE', 'ECD', 'Bar', 'Countplot'];
  chartTypes : any[] = [];

  selectedDatabase: string = '';
  selectedDatabaseIndex: number = 0;
  selectedChart: string = '';
  selectedChartIndex: number = 0;
  formData: any = {};

  columns: string[] = [];
  numericalColumns: string[] = [];
  categoricalColumns: string[] = [];
  fieldsMap: any = {};
  requiredFields: string[] = [];
  optionalFields: string[] = [];

  @Output() chartDataEvent = new EventEmitter<any>();

  constructor(private datasetService: DatasetService) {}

  ngOnInit() {
    this.datasetService.getAvailableDatasets().subscribe((response) => {
      console.log("getAvailableDatasets Response:", response);
      this.databases = response.available_datasets;
      this.chartTypes = response.available_charts;
      this.selectedDatabaseIndex = this.databases.length > 0 ? this.databases[0]["index"] : 0;
      this.selectedChartIndex = this.chartTypes.length > 0? this.chartTypes[0]["index"] : 0;
      if (this.selectedDatabase && this.selectedChartIndex){
        this.fetchChartRequirements();
      }
    });
  }

  fetchChartRequirements(){
    this.datasetService.getChartRequirements(
      this.selectedDatabase,
      this.selectedChart
    ).subscribe((data) => {
      this.fieldsMap = data.required_keys
      this.requiredFields = data.required_keys.required
      this.optionalFields = data.required_keys.optional || []
      this.columns = data.columns
      this.numericalColumns = data.numerical_columns
      this.categoricalColumns = data.categorical_columns
    });
  }

  getFilteredColumns(field: string): string[] {
    let data_types_options = this.fieldsMap.data_types
    let custom_options = this.fieldsMap.custom_options || {}
    let field_options: string[] = []
    if (field in data_types_options){
      if (data_types_options[field].includes('numerical')){
        field_options = field_options.concat(this.numericalColumns)
      }
      if (data_types_options[field].includes('categorical')){
        field_options = field_options.concat(this.categoricalColumns)
      }
      return field_options
    }
    else if (field in custom_options){
      field_options.concat(custom_options.get(field).get("options"))
      return field_options
    }
    return [];
  }

  onChange(): void {
    if (this.selectedDatabase && this.selectedChart) {
      this.fetchChartRequirements();
      this.formData = {};
    }
  }

  generateChart(): void {
    const requestData = {
      dataset: this.selectedDatabase,
      chart: this.selectedChart,
      fields : this.formData
    };
    this.chartDataEvent.emit(requestData);
  }
}
