<template>
    <div>
      <h2 class="chart-title">Saatlik Maliyet Karşılaştırması</h2>
      <LineChart :chart-data="chartData" :chart-options="chartOptions" />
    </div>
  </template>
  
  <script>
  import { Line } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale)
  
  export default {
    components: {
      LineChart: Line
    },
    props: {
      data: {
        type: Array,
        required: true
      }
    },
    computed: {
      chartData() {
        return {
          labels: this.data.map(item => item.hour),
          datasets: [
            {
              label: 'Maliyet (TL)',
              data: this.data.map(item => item.cost),
              borderColor: '#4CAF50',
              backgroundColor: 'rgba(76, 175, 80, 0.2)',
              fill: true
            }
          ]
        }
      },
      chartOptions() {
        return {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: true }
          }
        }
      }
    }
  }
  </script>
  
  <style>
  .chart-title {
    text-align: center;
    color: white;
    margin-bottom: 10px;
  }
  </style>
  