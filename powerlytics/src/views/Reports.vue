<template>
  <div class="reports">
    <h2>Raporlar</h2>
    <div class="reports-content">
      <div class="report-card">
        <h3>Günlük Rapor</h3>
        <p>{{ selectedFirm.name }} için günlük enerji tüketimi: {{ selectedFirm.currentUsage }} kWh</p>
        <div class="report-stats">
          <div class="stat-item">
            <span class="stat-label">Değişim</span>
            <span class="stat-value" :class="selectedFirm.dailyChange > 0 ? 'positive' : 'negative'">
              {{ selectedFirm.dailyChange > 0 ? '+' : '' }}{{ selectedFirm.dailyChange }}%
            </span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Verimlilik</span>
            <span class="stat-value">{{ selectedFirm.efficiency }}%</span>
          </div>
        </div>
      </div>

      <div class="report-card">
        <h3>Haftalık Rapor</h3>
        <p>{{ selectedFirm.name }} için haftalık ortalama tüketim: {{ (selectedFirm.currentUsage * 7).toFixed(1) }} kWh</p>
        <div class="report-chart">
          <div class="chart-placeholder">
            <i class="fa-solid fa-chart-line"></i>
            <span>Haftalık tüketim grafiği</span>
          </div>
        </div>
      </div>

      <div class="report-card">
        <h3>Aylık Rapor</h3>
        <p>{{ selectedFirm.name }} için aylık toplam tüketim: {{ (selectedFirm.currentUsage * 30).toFixed(1) }} kWh</p>
        <div class="report-actions">
          <button class="action-btn">
            <i class="fa-solid fa-download"></i>
            PDF İndir
          </button>
          <button class="action-btn">
            <i class="fa-solid fa-envelope"></i>
            E-posta Gönder
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  selectedFirm: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.reports {
  height: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.reports h2 {
  margin-bottom: 20px;
  color: #fff;
}

.reports-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.report-card {
  background-color: #1f2937;
  padding: 20px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.report-card h3 {
  color: #9ca3af;
  margin-bottom: 5px;
}

.report-card p {
  color: #fff;
  font-size: 1rem;
}

.report-stats {
  display: flex;
  gap: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.stat-label {
  color: #9ca3af;
  font-size: 0.875rem;
}

.stat-value {
  color: #fff;
  font-size: 1.25rem;
  font-weight: 600;
}

.positive {
  color: #10b981;
}

.negative {
  color: #ef4444;
}

.report-chart {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: #4b5563;
}

.chart-placeholder i {
  font-size: 3rem;
}

.report-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  padding: 10px 15px;
  background-color: #374151;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.2s;
}

.action-btn:hover {
  background-color: #4b5563;
}
</style> 