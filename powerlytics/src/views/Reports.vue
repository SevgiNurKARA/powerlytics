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
              20 {{ selectedFirm.dailyChange > 0 ? '+' : '' }}{{ selectedFirm.dailyChange }}%
            </span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Verimlilik</span>
            <span class="stat-value">{{ selectedFirm.efficiency }}85 %</span>
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

      <!-- Karbon Ayak İzi Raporu -->
      <div class="report-card carbon-footprint">
        <h3>Karbon Ayak İzi</h3>
        <p>{{ selectedFirm.name }} için aylık karbon ayak izi: {{ calculateCarbonFootprint(selectedFirm.currentUsage * 30).toFixed(2) }} kg CO₂</p>
        <div class="carbon-stats">
          <div class="carbon-meter">
            <div class="meter-label">Emisyon Seviyesi</div>
            <div class="meter-bar">
              <div class="meter-fill" :style="{ width: getCarbonImpactPercentage(selectedFirm.currentUsage * 30) + '%', backgroundColor: getCarbonImpactColor(selectedFirm.currentUsage * 30) }"></div>
            </div>
            <div class="meter-value">{{ getCarbonImpactStatus(selectedFirm.currentUsage * 30) }}</div>
          </div>
          <div class="carbon-comparison">
            <div class="comparison-item">
              <i class="fa-solid fa-tree"></i>
              <span color="#000000">{{ calculateTreeEquivalent(selectedFirm.currentUsage * 30).toFixed(1) }} ağaç</span>
            </div>
            <div class="comparison-item">
              <i class="fa-solid fa-car"></i>
              <span>{{ calculateCarEquivalent(selectedFirm.currentUsage * 30).toFixed(1) }} km</span>
            </div>
          </div>
        </div>
        <div class="report-actions">
          <button class="action-btn eco-btn">
            <i class="fa-solid fa-leaf"></i>
            Öneri Al
          </button>
          <button class="action-btn">
            <i class="fa-solid fa-download"></i>
            Rapor İndir
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

// Karbon ayak izi hesaplama metodu (kWh başına ortalama 0.5 kg CO₂ emisyonu)
const calculateCarbonFootprint = (kWh) => {
  return kWh * 0.5;
}

// Karbon ayak izi ağaç eşdeğeri hesaplama (1 ağaç yılda ortalama 22 kg CO₂ absorbe eder)
const calculateTreeEquivalent = (kWh) => {
  const carbonAmount = calculateCarbonFootprint(kWh);
  return carbonAmount / 22;
}

// Karbon ayak izi araba eşdeğeri hesaplama (ortalama 1 km'de 0.12 kg CO₂ emisyonu)
const calculateCarEquivalent = (kWh) => {
  const carbonAmount = calculateCarbonFootprint(kWh);
  return carbonAmount / 0.12;
}

// Karbon etkisi yüzdesini hesaplama (1000 kWh'ı %100 etki olarak kabul edelim)
const getCarbonImpactPercentage = (kWh) => {
  const percent = (calculateCarbonFootprint(kWh) / 500) * 100;
  return percent > 100 ? 100 : percent;
}

// Karbon etkisi rengi belirleme
const getCarbonImpactColor = (kWh) => {
  const percent = getCarbonImpactPercentage(kWh);
  if (percent < 30) return '#10b981'; // Yeşil - düşük etki
  if (percent < 70) return '#f59e0b'; // Sarı - orta etki
  return '#ef4444'; // Kırmızı - yüksek etki
}

// Karbon etkisi durumu belirleme
const getCarbonImpactStatus = (kWh) => {
  const percent = getCarbonImpactPercentage(kWh);
  if (percent < 30) return 'Düşük';
  if (percent < 70) return 'Orta';
  return 'Yüksek';
}
</script>

<style scoped>
.reports {
  height: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
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
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  color: #000000;
  border: 1px solid #d2d2d2;
  border-left: 4px solid #059669;
}

.report-card h3 {
  color: #000000;
  margin-bottom: 5px;
}

.report-card p {
  color: #000000;
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
  color: #000000;
  font-size: 0.875rem;
}

.stat-value {
  color: #000000;
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

/* Karbon ayak izi için ek stil özellikleri */
.carbon-footprint {
  border-left: 4px solid #059669;
}

.carbon-stats {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.carbon-meter {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.meter-label {
  color: #9ca3af;
  font-size: 0.875rem;
}

.meter-bar {
  height: 8px;
  width: 100%;
  background-color: #374151;
  border-radius: 4px;
  overflow: hidden;
}

.meter-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s ease, background-color 0.3s ease;
}

.meter-value {
  color: #fff;
  font-size: 0.875rem;
  font-weight: 500;
  align-self: flex-end;
}

.carbon-comparison {
  display: flex;
  gap: 15px;
  margin-top: 5px;
}

.comparison-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #000000;
  font-size: 0.875rem;
}

.comparison-item i {
  color: #10b981;
}

.eco-btn {
  background-color: #065f46;
}

.eco-btn:hover {
  background-color: #047857;
}
</style>