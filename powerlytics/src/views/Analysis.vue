<template>
  <div class="analysis">
    <h2>Analiz</h2>
    <div class="analysis-content">
      <div class="chart-container">
        <h3>Enerji Tüketim Analizi</h3>
        <div class="chart">
          <!-- Burada chart komponenti kullanılacak -->
          <EnergyChart :data="energyChartData" />
        </div>
      </div>
      
      <div class="analysis-stats">
        <div class="stat-card">
          <h4>Günlük Ortalama</h4>
          <div class="stat-value">{{ dailyAverage }} kWh</div>
        </div>
        <div class="stat-card">
          <h4>Haftalık Trend</h4>
          <div class="stat-value" :class="weeklyTrend > 0 ? 'positive' : 'negative'">
            {{ weeklyTrend > 0 ? '+' : '' }}{{ weeklyTrend }}%
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import EnergyChart from '../components/EnergyChart.vue'

const dailyAverage = ref(245.8)
const weeklyTrend = ref(-2.5)

const energyChartData = computed(() => ({
  labels: ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar'],
  datasets: [{
    label: 'Enerji Tüketimi (kWh)',
    data: [240, 238, 245, 230, 248, 242, 235],
    borderColor: '#10B981',
    tension: 0.4
  }]
}))
</script>

<style scoped>
.analysis {
  height: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.analysis h2 {
  margin-bottom: 20px;
  color: #fff;
}

.analysis-content {
  flex: 1;
  display: grid;
  grid-template-rows: 1fr auto;
  gap: 20px;
}

.chart-container {
  background-color: #1f2937;
  padding: 20px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
}

.chart-container h3 {
  color: #9ca3af;
  margin-bottom: 15px;
}

.chart {
  flex: 1;
  min-height: 400px;
}

.analysis-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  background-color: #1f2937;
  padding: 20px;
  border-radius: 8px;
}

.stat-card h4 {
  color: #9ca3af;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #fff;
}

.positive {
  color: #10B981;
}

.negative {
  color: #EF4444;
}
</style> 