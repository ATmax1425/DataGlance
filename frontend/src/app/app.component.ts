import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent } from './header/header.component';
import { ChartSelectComponent } from './chart-select/chart-select.component';
import { VisualizeComponent } from './visualize/visualize.component';
import { ParameterSelectComponent } from "./chart-select/parameter-select/parameter-select.component";

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [RouterOutlet, HeaderComponent, ChartSelectComponent, VisualizeComponent, ParameterSelectComponent],
    templateUrl: './app.component.html',
    styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'frontend';
  chartOptions: any;

  onChartSelectionChange(event: { database: string; chart: string }) {
    console.log('Selected Database:', event.database);
    console.log('Selected Chart Type:', event.chart);
  }

  onChartDataReceived(event: any) {
    this.chartOptions = event; // Store received chart data
  }
}
