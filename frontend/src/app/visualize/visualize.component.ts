import { Component, ElementRef, Input, OnChanges, ViewChild, viewChild } from '@angular/core';
import { Chart } from 'chart.js';

@Component({
  selector: 'app-visualize',
  imports: [],
  standalone: true,
  templateUrl: './visualize.component.html',
  styleUrl: './visualize.component.scss'
})
export class VisualizeComponent implements OnChanges  {
  @Input() chartData: any;
  @ViewChild('chartCanvas') chartCanvas!: ElementRef;
  chart!: Chart;

  ngOnChanges() {
    if (this.chartData) {
      this.createChart();
    }
  }

  createChart() {
    if (this.chart) {
      this.chart.destroy(); // Remove previous chart instance
    }

    const ctx = this.chartCanvas.nativeElement.getContext('2d');
    this.chart = new Chart(ctx, {
      type: this.chartData.chartType, // Dynamic chart type
      data: {
        labels: this.chartData.labels,
        datasets: [{
          label: this.chartData.chartLabel,
          data: this.chartData.values,
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false
      }
    });
  }
}
