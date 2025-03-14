<!-- src/components/EnergyChart.vue -->
<template>
  <div class="chart-wrapper">
    <Line
      :data="chartData"
      :options="chartOptions"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

const props = defineProps({
  data: {
    type: Object,
    required: true,
    default: () => ({
      labels: [],
      datasets: []
    })
  },
  compareData: {
    type: Object,
    required: false,
    default: null
  },
  compareLabel: {
    type: String,
    default: 'Karşılaştırma Verisi'
  }
})

const chartData = computed(() => {
  const result = {
    labels: props.data.labels,
    datasets: [...props.data.datasets]
  }
  
  if (props.compareData && props.compareData.datasets && props.compareData.datasets.length > 0) {
    const compareDataset = { ...props.compareData.datasets[0] }
    compareDataset.label = props.compareLabel
    compareDataset.borderColor = '#10B981'
    compareDataset.backgroundColor = 'rgba(16, 185, 129, 0.2)'
    
    result.datasets.push(compareDataset)
  }
  
  return result
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: ' #e5e4d7'
      },
      ticks: {
        color: '#000000'
      }
    },
    x: {
      grid: {
        color: '#e5e4d7'
      },
      ticks: {
        color: '#000000'
      }
    }
  },
  plugins: {
    legend: {
      labels: {
        color: '#000000'
      }
    }
  }
}
</script>

<style scoped>
.chart-wrapper {
  position: relative;
  height: 250px;
  width: 100%;
}
</style>
  