import { Component, output } from '@angular/core';

@Component({
  selector: 'app-chart-type-select',
  imports: [],
  standalone: true,
  templateUrl: './chart-type-select.component.html',
  styleUrl: './chart-type-select.component.scss'
})
export class ChartTypeSelectComponent {
  selected = output<string>();
  
  get_selected_chart_type(selectedChartType:string): void{
    this.selected.emit(selectedChartType);
  }
}
