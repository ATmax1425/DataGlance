import { Component, ElementRef, Input, OnChanges, ViewChild } from '@angular/core';
import { Chart, ScatterController, LineController, BarController, BubbleController, PieController, DoughnutController,
  Title, PointElement, LineElement, BarElement, ArcElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js';
import { DatasetService } from '../services/dataset.service';

Chart.register(ScatterController, LineController, BarController, BubbleController, PieController, DoughnutController, 
  Title, PointElement, LineElement, BarElement, ArcElement, CategoryScale, LinearScale, Tooltip, Legend)

@Component({
  selector: 'app-visualize',
  imports: [],
  standalone: true,
  templateUrl: './visualize.component.html',
  styleUrl: './visualize.component.scss'
})
export class VisualizeComponent implements OnChanges  {
  @Input() chartOptions: any;
  @ViewChild('chartCanvas') chartCanvas!: ElementRef;
  chart!: Chart;

  constructor(private datasetService: DatasetService) {}

  ngOnChanges() {
    console.log("chartOptions", this.chartOptions);
    if (this.chartOptions) {
      this.datasetService.getChartData(
        this.chartOptions.dataset, 
        this.chartOptions.chart, 
        this.chartOptions.fields
      ).subscribe((chartData) => {
        this.createChart(chartData);
      })
    }
  }

  createChart(chartData: any) {
    if (this.chart) {
      this.chart.destroy(); // Remove previous chart instance
    }

    const ctx = this.chartCanvas.nativeElement.getContext('2d');
    if (!ctx) {
      console.error("Canvas context not found!");
      return;
    }
    try {
      this.chart = new Chart(ctx, {
        type: chartData.chartType,
        data: chartData.chartData,
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      });
    } catch (error) {
      console.error("Error creating chart:", error);
    }
    console.log("Chart created successfully!");
  }
}
