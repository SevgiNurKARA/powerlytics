<template>
  <div class="dashboard">
    <h2>Enerji Yönetim Gösterge Paneli</h2>
    <div class="dashboard-content">
      <!-- Özet Metrikler -->
      <div class="metrics-container">
        <div class="metric-item energy">
          <h3>Günlük Enerji Tüketimi</h3>
          <div class="value">{{ summary.dailyConsumption }} kWh</div>
          <div class="change" :class="{ 'positive': summary.consumptionChange < 0, 'negative': summary.consumptionChange > 0 }">
            {{ summary.consumptionChange > 0 ? '+' : '' }}{{ summary.consumptionChange }}% geçen güne göre
          </div>
        </div>

        <div class="metric-item cost">
          <h3>Günlük Maliyet</h3>
          <div class="value">{{ summary.dailyCost }} ₺</div>
          <div class="change" :class="{ 'positive': summary.costChange < 0, 'negative': summary.costChange > 0 }">
            {{ summary.costChange > 0 ? '+' : '' }}{{ summary.costChange }}% geçen güne göre
          </div>
        </div>

        <div class="metric-item carbon">
          <h3>Karbon Ayak İzi</h3>
          <div class="value">{{ summary.carbonFootprint }} kg CO₂</div>
          <div class="change" :class="{ 'positive': summary.carbonChange < 0, 'negative': summary.carbonChange > 0 }">
            {{ summary.carbonChange > 0 ? '+' : '' }}{{ summary.carbonChange }}% geçen güne göre
          </div>
        </div>

        <div class="metric-item efficiency">
          <h3>Ortalama Verimlilik</h3>
          <div class="value">{{ summary.avgEfficiency }}%</div>
          <div class="change" :class="{ 'positive': summary.efficiencyChange > 0, 'negative': summary.efficiencyChange < 0 }">
            {{ summary.efficiencyChange > 0 ? '+' : '' }}{{ summary.efficiencyChange }}% geçen güne göre
          </div>
        </div>
      </div>

      <!-- Makine Seçici -->
      <div class="info-panel">
        <h3>Makine Seçimi</h3>
        <div class="machine-selector">
          <label for="firmType">Tesis:</label>
          <select 
            id="firmType" 
            v-model="selectedFirm" 
            class="machine-select"
          >
            <option value="">Tesis Seçiniz</option>
            <option v-for="firm in firms" :key="firm" :value="firm">
              {{ firm }}
            </option>
          </select>
          
          <label for="machineType">Makine Türü:</label>
          <select 
            id="machineType" 
            v-model="selectedMachineType" 
            class="machine-select"
            @change="fetchMachineData"
          >
          <option value="">Makine Seçiniz</option>
            <option value="Pompa">Pompa</option>
            <option value="LPG Kompresörü">LPG Kompresörü</option>
            <option value="Hava Kompresörü">Hava Kompresörü</option>
          
          </select>
        </div>
      </div>

      <!-- Gauge Meters Grid -->
      <div class="gauge-container">
        <div class="gauge-item">
          <h3>Çekilen Enerji</h3>
          <CircularProgress 
            :value="energyData.cekilenEnerji || 0" 
            :max="100"
            unit="kWh"
            color="green"
          />
        </div>

        <div class="gauge-item">
          <h3>Kullanılan Enerji</h3>
          <CircularProgress 
            :value="energyData.kullanilanEnerji || 0" 
            :max="100"
            unit="kWh"
            color="green"
          />
        </div>

        <div class="gauge-item">
          <h3>Verimlilik</h3>
          <CircularProgress 
            :value="energyData.verimlilik || 0" 
            :max="100"
            unit="%"
            color="green"
          />
        </div>

        <div class="gauge-item">
          <h3>Günlük Maliyet</h3>
          <CircularProgress 
            :value="energyData.gunlukMaliyet || 0" 
            :max="50"
            unit="₺"
            color="orange"
          />
        </div>
      </div>

      <!-- Status Indicators -->
      <div class="status-container">
        <div class="status-item temperature">
          <h3>Saat Aralığı</h3>
          <div class="value">{{ energyData.saatAraligi || '00-06' }}</div>
        </div>

        <div class="status-item" :class="{'alert': energyData.isoPuant}">
          <h3>Puant Durumu</h3>
          <div class="value">{{ energyData.isoPuant ? 'Puant Saati' : 'Normal Saat' }}</div>
        </div>

        <div class="status-item" :class="{'alert': energyData.isoAssessment === 'Verimsiz'}">
          <h3>ISO 50001 Değerlendirme</h3>
          <div class="value">{{ energyData.isoAssessment || 'Değerlendirilmedi' }}</div>
        </div>

        <div class="status-item">
          <h3>Çalışma Durumu</h3>
          <div class="value">{{ energyData.calismaDurumu || 'Normal' }}</div>
        </div>
      </div>

      <!-- Enerji Analiz Paneli (API'den) -->
      <div class="energy-analysis-panel info-panel">
        <h3>Enerji Analizi</h3>
        <div class="analysis-content">
          <div class="analysis-metrics">
            <div class="analysis-metric">
              <span>Toplam Kullanım</span>
              <span>{{ energyData.kullanilanEnerji || 0 }} kWh</span>
            </div>
            <div class="analysis-metric">
              <span>Mevcut Saat Maliyeti</span>
              <span>{{ energyData.gunlukMaliyet || 0 }} ₺</span>
            </div>
            <div class="analysis-metric">
              <span>Önerilen Saat Aralığı</span>
              <span>{{ energyAnalysis.optimal_time_range || '00-06' }}</span>
            </div>
            <div class="analysis-metric">
              <span>Önerilen Maliyet</span>
              <span>{{ energyAnalysis.optimal_cost || 0 }} ₺</span>
            </div>
            <div class="analysis-metric">
              <span>Karbon Ayak İzi</span>
              <span>{{ energyAnalysis.carbon_footprint || 0 }} kg</span>
            </div>
            <div class="analysis-metric highlight">
              <span>Potansiyel Tasarruf</span>
              <span>{{ energyAnalysis.potential_savings || 0 }} ₺</span>
            </div>
          </div>
          
          <div class="optimization-suggestion">
            <h4>AI Optimizasyon Önerisi</h4>
            <p>{{ aiPrediction || 'Analiz için tahmin talep edin' }}</p>
            <div class="savings-percentage" v-if="energyAnalysis.savings_percentage">
              <span>Tasarruf Potansiyeli:</span>
              <span class="percentage">%{{ energyAnalysis.savings_percentage.toFixed(2) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Makine Detayları -->
      <div class="info-panel" v-if="selectedMachineType">
        <h3>{{ selectedMachineType || 'Makine' }} Enerji Tüketim Verileri</h3>
        <div class="machine-form">
          <div class="form-row">
            <div class="form-group">
              <label for="cekilenEnerji">Çekilen Enerji (kWh):</label>
              <input type="number" id="cekilenEnerji" v-model="energyData.cekilenEnerji" class="form-input" step="0.1" min="0">
            </div>
            <div class="form-group">
              <label for="kullanilanEnerji">Kullanılan Enerji (kWh):</label>
              <input type="number" id="kullanilanEnerji" v-model="energyData.kullanilanEnerji" class="form-input" step="0.1" min="0">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="saatDilimi">Saat Dilimi:</label>
              <input type="time" id="saatDilimi" v-model="energyData.saatDilimi" class="form-input">
            </div>
            <div class="form-group">
              <label for="calismaDurumu">Çalışma Durumu:</label>
              <select id="calismaDurumu" v-model="energyData.calismaDurumu" class="form-input">
                <option value="Normal">Normal</option>
                <option value="Yüksek Yük">Yüksek Yük</option>
                <option value="Düşük Yük">Düşük Yük</option>
                <option value="Beklemede">Beklemede</option>
              </select>
            </div>
          </div>
          <div class="form-btns">
            <button 
              @click="analyzeEnergy" 
              class="action-btn"
              :disabled="!selectedMachineType || !energyData.cekilenEnerji || !energyData.kullanilanEnerji"
            >
              Enerji Analizi
            </button>
            <button 
              @click="getAIPrediction" 
              class="action-btn predict-btn"
              :disabled="!selectedMachineType || !energyData.cekilenEnerji || !energyData.kullanilanEnerji"
            >
              AI Tahmin
            </button>
          </div>
        </div>
      </div>

      <!-- Charts Grid -->
      <div class="charts-container">
        <div class="chart-item">
          <h3>Günlük Maliyet Karşılaştırması</h3>
          <EnergyChart 
            :data="costChartData" 
            :compare-data="previousCostChartData"
            compare-label="Önceki Dönem"
          />
        </div>

        <div class="chart-item">
          <h3>Saat Dilimleri Maliyet Analizi</h3>
          <EnergyChart :data="timeRangeChartData" />
        </div>
      </div>

      <!-- Alarm Panel -->
      <div class="alarm-panel">
        <h3>Aktif Alarmlar ({{ alarms.length }})</h3>
        <div class="alarm-content">
          <div v-for="alarm in alarms" :key="alarm.id" class="alarm-item" :style="{ backgroundColor: alarm.severity === 'Orta' ? 'yellow' : 'green' }">
            <div class="alarm-header" style="color: #000000;">
              <span>{{ alarm.type }}</span>
              <span class="alarm-value" style="color: #000000;">{{ alarm.severity }}</span>
            </div>
            <div class="alarm-info" style="color: #000000;">
              {{ alarm.message }}
              <span class="alarm-time">{{ alarm.timestamp }}</span>
            </div>
          </div>
          <div v-if="alarms.length === 0" class="no-alarms">
            Aktif alarm bulunmamaktadır.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import CircularProgress from '../components/CircularProgress.vue'
import EnergyChart from '../components/EnergyChart.vue'

// API endpoint base URL
const API_URL = 'http://localhost:5000'  // Flask API port

// Durumlar ve referanslar
const selectedFirm = ref('')
const selectedMachineType = ref('')
const alarms = ref([])
const aiPrediction = ref(null)
const updateInterval = ref(null)

// Firma ve makine listeleri
const firms = ref([])
const machines = ref([])

// Enerji verileri
const energyData = ref({
  cekilenEnerji: 0,
  kullanilanEnerji: 0,
  saatDilimi: '08:00',
  calismaDurumu: 'Normal',
  saatAraligi: '06-12',
  isoPuant: false,
  isoAssessment: 'Orta',
  gunlukMaliyet: 0,
  verimlilik: 0
})

// Özet metrikleri
const summary = ref({
  dailyConsumption: 0,
  dailyCost: 0,
  carbonFootprint: 0,
  avgEfficiency: 0,
  consumptionChange: 0,
  costChange: 0,
  carbonChange: 0,
  efficiencyChange: 0
})

// Enerji analiz verileri
const energyAnalysis = ref({
  current_time_range: '',
  current_cost: 0,
  alternative_costs: {},
  optimal_time_range: '',
  optimal_cost: 0,
  potential_savings: 0,
  savings_percentage: 0,
  efficiency: 0,
  carbon_footprint: 0,
  iso_assessment: ''
})

// Grafik verileri
const costChartData = ref({
  labels: ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs'],
  datasets: [{
    label: 'Maliyet Karşılaştırması (₺)',
    data: [6, 4, 3, 4, 5],
    backgroundCololr: ['#3B82F6'],
    borderColor: ['#2563EB'],
    borderWidth: 1
  }]
})

const timeRangeChartData = ref({
  labels: ['00-06', '06-12', '12-18', '18-24'],
  datasets: [{
    label: 'Saat Dilimi Maliyeti (₺)',
    data: [2.54, 3.25, 3.25, 2.54],
    backgroundColor: ['#DBEAFE', '#BFDBFE', '#93C5FD', '#60A5FA'],
    borderColor: '#2563EB',
    borderWidth: 1
  }]
})

// Önceki dönem maliyet verileri
const previousCostChartData = ref({
  labels: ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs'],
  datasets: [{
    label: 'Önceki Dönem Maliyeti (₺)',
    data: [5, 1, 4, 3, 4],
    borderColor: '#2563EB',
    backgroundColor: 'rgba(16, 185, 129, 0.2)',
    borderWidth: 1
  }]
})

// Model bilgilerini getir
const fetchModelInfo = async () => {
  try {
    const response = await fetch(`${API_URL}/model-info`)
    if (!response.ok) throw new Error('Model bilgileri alınamadı')
    
    const data = await response.json()
    firms.value = data.firms || [r,b,c]
    machines.value = data.machines || []
    
    // Özet metriklerini doldur
    summary.value = data.summary || {
      dailyConsumption: 156.8,
      dailyCost: 78.4,
      carbonFootprint: 62.7,
      avgEfficiency: 84.5,
      consumptionChange: -3.2,
      costChange: -4.7,
      carbonChange: -5.1,
      efficiencyChange: 1.2
    }
    
    // Alarmları doldur
    alarms.value = data.alarms || []
  } catch (error) {
    console.error('Model bilgileri alınamadı:', error)
    // Demo için varsayılan veriler
    firms.value = ['Çankaya ', 'Bahriye', 'Nazilli']
    machines.value = ['CNC Tezgahı', 'Pres Makinesi', 'Kaynak Makinesi']
    
    // Demo alarmları
    alarms.value = [
      {
        id: 1,
        type: 'Verimlilik Uyarısı',
        severity: 'Orta',
        message: 'CNC tezgahının verimliliği %65\'in altına düştü.',
        timestamp: '13.03.2025 10:32'
      },
      {
        id: 2,
        type: 'Puant Bildirimi',
        severity: 'Düşük',
        message: 'Şu an puant saati içinde çalışan 3 makine var.',
        timestamp: '13.03.2025 09:15'
      }
    ]
    
    // Demo özet verileri
    summary.value = {
      dailyConsumption: 156.8,
      dailyCost: 78.4,
      carbonFootprint: 62.7,
      avgEfficiency: 84.5,
      consumptionChange: -3.2,
      costChange: -4.7,
      carbonChange: -5.1,
      efficiencyChange: 1.2
    }
  }
}

// Makine verilerini getir
const fetchMachineData = async () => {
  if (!selectedMachineType.value) return
  
  try {
    const response = await fetch(`${API_URL}/machine-data?machine=${selectedMachineType.value}`)
    if (!response.ok) throw new Error('Makine verileri alınamadı')
    
    const data = await response.json()
    energyData.value = { ...energyData.value, ...data }
    calculateMachineMetrics()
  } catch (error) {
    console.error('Makine verileri alınamadı:', error)
    // Demo verileri
    energyData.value = {
      cekilenEnerji: 42.6,
      kullanilanEnerji: 36.4,
      saatDilimi: '08:30',
      calismaDurumu: 'Normal',
      saatAraligi: '06-12',
      isoPuant: false,
      isoAssessment: 'Verimli',
      verimlilik: 85.4,
      gunlukMaliyet: 18.2
    }
    calculateMachineMetrics()
  }
}

// Makine metriklerini hesapla
const calculateMachineMetrics = () => {
  if (energyData.value.cekilenEnerji && energyData.value.kullanilanEnerji) {
    // Verimlilik hesapla
    energyData.value.verimlilik = parseFloat(((energyData.value.kullanilanEnerji / energyData.value.cekilenEnerji) * 100).toFixed(1))
    
    // Günlük maliyet hesapla (varsayılan kWh birim fiyatı: 0.5 TL)
    energyData.value.gunlukMaliyet = parseFloat((energyData.value.kullanilanEnerji * 0.5).toFixed(1))
    
    // Saat aralığını belirle
    const hour = parseInt(energyData.value.saatDilimi.split(':')[0], 10)
    if (hour >= 0 && hour < 6) {
      energyData.value.saatAraligi = '00-06'
    } else if (hour >= 6 && hour < 12) {
      energyData.value.saatAraligi = '06-12'
    } else if (hour >= 12 && hour < 18) {
      energyData.value.saatAraligi = '12-18'
    } else {
      energyData.value.saatAraligi = '18-24'
    }
    
    // Puant durumunu kontrol et (17:00-22:00 arası puant saati)
    if (hour >= 17 && hour < 22) {
      energyData.value.isoPuant = true
    } else {
      energyData.value.isoPuant = false
    }
    
    // ISO değerlendirmesini yap
    if (energyData.value.verimlilik >= 85) {
      energyData.value.isoAssessment = 'Verimli'
    } else if (energyData.value.verimlilik >= 70) {
      energyData.value.isoAssessment = 'Orta'
    } else {
      energyData.value.isoAssessment = 'Verimsiz'
    }
  }
}

// Enerji analizi yap
const analyzeEnergy = async () => {
  try {
    const response = await fetch(`${API_URL}/energy-analysis`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        machine: selectedMachineType.value,
        time: energyData.value.saatDilimi,
        power_drawn: energyData.value.cekilenEnerji,
        power_used: energyData.value.kullanilanEnerji
      })
    })
    
    if (!response.ok) throw new Error('Enerji analizi yapılamadı')
    
    const data = await response.json()
    energyAnalysis.value = data
    
    // Grafik verilerini güncelle
    updateChartData()
  } catch (error) {
    console.error('Enerji analizi yapılamadı:', error)
    // Demo analiz verileri
    const hourRate = determineHourlyRate(energyData.value.saatDilimi)
    
    energyAnalysis.value = {
      current_time_range: energyData.value.saatAraligi,
      current_cost: energyData.value.gunlukMaliyet,
      alternative_costs: {
        '00-06': (energyData.value.kullanilanEnerji * 0.3).toFixed(1),
        '06-12': (energyData.value.kullanilanEnerji * 0.5).toFixed(1),
        '12-18': (energyData.value.kullanilanEnerji * 0.6).toFixed(1),
        '18-24': (energyData.value.kullanilanEnerji * 0.7).toFixed(1)
      },
      optimal_time_range: '00-06',
      optimal_cost: (energyData.value.kullanilanEnerji * 0.3).toFixed(1),
      potential_savings: (energyData.value.gunlukMaliyet - (energyData.value.kullanilanEnerji * 0.3)).toFixed(1),
      savings_percentage: ((energyData.value.gunlukMaliyet - (energyData.value.kullanilanEnerji * 0.3)) / energyData.value.gunlukMaliyet * 100),
      efficiency: energyData.value.verimlilik,
      carbon_footprint: (energyData.value.kullanilanEnerji * 0.4).toFixed(1),
      iso_assessment: energyData.value.isoAssessment
    }
    
    // Grafik verilerini güncelle
    updateChartData()
  }
}

// Saat dilimine göre birim fiyat belirle
const determineHourlyRate = (timeStr) => {
  const hour = parseInt(timeStr.split(':')[0], 10)
  
  if (hour >= 0 && hour < 6) return 0.3 // En ucuz
  if (hour >= 6 && hour < 12) return 0.5 // Normal
  if (hour >= 12 && hour < 18) return 0.6 // Yüksek
  return 0.7 // En yüksek (18-24)
}

// AI tahmini al
const getAIPrediction = async () => {
  try {
    const response = await fetch(`${API_URL}/ai-prediction`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        machine: selectedMachineType.value,
        current_data: energyData.value,
        analysis: energyAnalysis.value
      })
    })
    
    if (!response.ok) throw new Error('AI tahmini alınamadı')
    
    const data = await response.json()
    aiPrediction.value = data.prediction
  } catch (error) {
    console.error('AI tahmini alınamadı:', error)
    // Demo tahmin
    aiPrediction.value = `${selectedMachineType.value || 'Bu makine'} için enerji verimliliğini artırmak ve maliyeti düşürmek için üretim planlamasını 00-06 saatleri arasına kaydırmanızı öneririm. Bu değişiklik ile günlük ${energyAnalysis.value.potential_savings || '6.5'} ₺ tasarruf sağlayabilir ve karbon ayak izinizi %22 azaltabilirsiniz.`
  }
}

// Grafik verilerini güncelle
const updateChartData = () => {
  // Maliyet karşılaştırma grafiği
  costChartData.value.datasets[0].data = [
    parseFloat(energyAnalysis.value.current_cost),
    parseFloat(energyAnalysis.value.optimal_cost)
  ]
  
  // Saat dilimleri grafiği
  const timeRanges = ['00-06', '06-12', '12-18', '18-24']
  const alternativeCosts = energyAnalysis.value.alternative_costs || {}
  
  timeRangeChartData.value.datasets[0].data = timeRanges.map(range => 
    parseFloat(alternativeCosts[range] || 0)
  )
}

// Firma değiştiğinde makineleri güncelle
watch(selectedFirm, async (newValue) => {
  if (newValue) {
    try {
      const response = await fetch(`${API_URL}/machines?firm=${newValue}`)
      if (!response.ok) throw new Error('Makine listesi alınamadı')
      
      const data = await response.json()
      machines.value = data.machines || []
    } catch (error) {
      console.error('Makine listesi alınamadı:', error)
      // Demo makineler
      machines.value = ['CNC Tezgahı', 'Pres Makinesi', 'Kaynak Makinesi']
    }
  } else {
    machines.value = []
  }
  
  // Makine seçimini sıfırla
  selectedMachineType.value = ''
})

// Enerji verileri değiştiğinde metrikleri güncelle
watch([() => energyData.value.cekilenEnerji, () => energyData.value.kullanilanEnerji, () => energyData.value.saatDilimi], 
  () => {
    calculateMachineMetrics()
  }
)

// Component yüklendiğinde
onMounted(() => {
  // Model ve makine bilgilerini getir
  fetchModelInfo()
  
  // Periyodik güncelleme başlat (5 dakikada bir)
  updateInterval.value = setInterval(() => {
    fetchModelInfo()
    if (selectedMachineType.value) {
      fetchMachineData()
    }
  }, 5 * 60 * 1000)
})

// Component kaldırıldığında
onUnmounted(() => {
  // Periyodik güncellemeyi durdur
  if (updateInterval.value) {
    clearInterval(updateInterval.value)
  }
})
</script>

<style scoped>
.dashboard {
  font-family: 'Roboto', sans-serif;
  max-width: 100%;
  margin: 0 auto;
  background-color: #ffffff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.dashboard h2 {
  background-color:#4b5563;
  color: white;
  margin: 0;
  padding: 20px;
  font-size: 1.5rem;
  text-align: center;
}

.dashboard-content {
  padding: 20px;
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 20px;
}

/* Özet Metrikler */
.metrics-container {
  grid-column: span 12;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}

.metric-item {
  background-color: #d2d2d2;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.metric-item h3 {
  font-size: 1rem;
  margin-top: 0;
  margin-bottom: 10px;
  color: #4b5563;
}

.metric-item .value {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 5px;
  color: #111827;
}

.metric-item .change {
  font-size: 0.85rem;
  color: #6b7280;
}

.metric-item .change.positive {
  color: #10b981;
}

.metric-item .change.negative {
  color: #ef4444;
}

.metric-item.energy .value {
  color: #3b82f6;
}

.metric-item.cost .value {
  color: #f59e0b;
}

.metric-item.carbon .value {
  color: #10b981;
}

.metric-item.efficiency .value {
  color: #8b5cf6;
}

/* Makine Seçici */
.info-panel {
 grid-column: span 12;
 background-color: white;
 border: 1px solid #d2d2d2;
 border-radius: 8px;
 padding: 20px;
 box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.info-panel h3 {
 margin-top: 0;
 margin-bottom: 15px;
 color: #1e40af;
 font-size: 1.2rem;
}

.machine-selector {
 display: flex;
 flex-wrap: wrap;
 align-items: center;
 gap: 15px;
}

.machine-selector label {
 font-weight: 500;
 color: #4b5563;
 margin-right: 5px;
}

.machine-select {
 padding: 8px 12px;
 border: 1px solid #d1d5db;
 border-radius: 6px;
 font-size: 0.95rem;
 min-width: 200px;
}

/* Gauge Meters Grid */
.gauge-container {
 grid-column: span 12;
 display: grid;
 grid-template-columns: repeat(4, 1fr);
 gap: 15px;
}

.gauge-item {
 background-color: #d2d2d2;
 border-radius: 8px;
 padding: 15px;
 box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
 display: flex;
 flex-direction: column;
 align-items: center;
}

.gauge-item h3 {
 margin-top: 0;
 margin-bottom: 15px;
 color: #f59e0b;
 font-size: 1rem;
 text-align: center;
}

/* Status Indicators */
.status-container {
 grid-column: span 12;
 display: grid;
 grid-template-columns: repeat(4, 1fr);
 gap: 15px;
}

.status-item {
 background-color:#d2d2d2;
 border-radius: 8px;
 padding: 15px;
 box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
 color: #000000;
}

.status-item h3 {
 font-size: 1rem;
 margin-top: 0;
 margin-bottom: 10px;
 color: #000000;
}

.status-item .value {
 font-size: 1.25rem;
 font-weight: bold;
 color: #000000;
}

.status-item.alert {
 background-color: #fee2e2;
}

.status-item.alert .value {
 color: #ef4444;
}

/* Energy Analysis Panel */
.energy-analysis-panel {
 grid-column: span 12;
}

.analysis-content {
 display: flex;
 flex-wrap: wrap;
 gap: 20px;
}

.analysis-metrics {
 flex: 1;
 min-width: 300px;
 display: grid;
 grid-template-columns: repeat(2, 1fr);
 gap: 10px;
}

.analysis-metric {
 padding: 10px;
 background-color: #d2d2d2;
 border-radius: 6px;
 color: #000000;
 display: flex;
 justify-content: space-between;
 font-size: 0.95rem;
}

.analysis-metric.highlight {
 background-color: #d2d2d2;
 font-weight: 500;
 color: #000000;
}

.optimization-suggestion {
 flex: 1;
 color: #000000;
 min-width: 300px;
 background-color: #d2d2d2;
 border-radius: 6px;
 padding: 15px;
}

.optimization-suggestion h4 {
 margin-top: 0;
 margin-bottom: 10px;
 color: #1e40af;
 font-size: 1rem;
}

.optimization-suggestion p {
 margin-bottom: 10px;
 line-height: 1.5;
}

.savings-percentage {
 display: flex;
 justify-content: space-between;
 font-weight: 500;
}

.savings-percentage .percentage {
 color: #10b981;
}

/* Machine Form */
.machine-form {
 margin-top: 10px;
}

.form-row {
 display: flex;
 flex-wrap: wrap;
 gap: 20px;
 margin-bottom: 15px;
}

.form-group {
 flex: 1;
 min-width: 200px;
 color: #000000;
 background-color: #f0f9ff;
}

.form-group label {
 display: block;
 margin-bottom: 5px;
 font-size: 0.9rem;
 color: #000000;
}

.form-input {
 width: 100%;
 padding: 8px 12px;
 border: 1px solid #d1d5db;
 border-radius: 6px;
 font-size: 0.95rem;
}

.form-btns {
 display: flex;
 gap: 15px;
 margin-top: 15px;
}

.action-btn {
 padding: 10px 20px;
 background-color: darkblue;
 color: white;
 border: none;
 border-radius: 6px;
 font-weight: 500;
 cursor: pointer;
 transition: background-color 0.2s;
}

.action-btn:hover {
 background-color: #3b82f6;
}

.action-btn:disabled {
 background-color: #93c5fd;
 cursor: not-allowed;
}

.predict-btn {
 background-color: #f59e0b;
}

.predict-btn:hover {
 background-color: #fdee00;
}

.predict-btn:disabled {
 background-color: #c4b5fd;
}

/* Charts Grid */
.charts-container {
 grid-column: span 12;
 display: grid;
 grid-template-columns: repeat(2, 1fr);
 gap: 20px;
 width: 100%;

}

.chart-item {
 background-color:#d2d2d2;
 border-radius: 8px;
 padding: 15px;
 box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.chart-item h3 {
 margin-top: 0;
 margin-bottom: 15px;
 color: #000000;
 font-size: 1rem;
 text-align: center;
}

/* Alarm Panel */
.alarm-panel {
 grid-column: span 12;
 background-color:#d2d2d2;
 border-radius: 8px;
 padding: 20px;
 box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}


.alarm-panel h3 {
 margin-top: 0;
 margin-bottom: 15px;
 color: red;
 font-size: 1.2rem;
}

.alarm-content {
 display: flex;
 flex-direction: column;
 gap: 12px;
}

.alarm-item {
 padding: 12px;
 border-radius: 6px;
 background-color: #fee2e2;
}

.alarm-header {
 display: flex;
 justify-content: space-between;
 font-weight: 500;
 margin-bottom: 5px;
}

.alarm-value {
 padding: 2px 8px;
 border-radius: 99px;
 font-size: 0.85rem;
 background-color: #fecaca;
}

.alarm-info {
 display: flex;
 justify-content: space-between;
 font-size: 0.95rem;
}

.alarm-time {
 font-size: 0.85rem;
 color: #6b7280;
}

.no-alarms {
 padding: 15px;
 text-align: center;
 color: #6b7280;
}

/* Responsive adjustments */
@media (max-width: 1200px) {
 .metrics-container {
   grid-template-columns: repeat(2, 1fr);
 }
 
 .gauge-container {
   grid-template-columns: repeat(2, 1fr);
 }
 
 .status-container {
   grid-template-columns: repeat(2, 1fr);
 }
 
 .charts-container {
   grid-template-columns: 1fr;
 }
}

@media (max-width: 768px) {
 .metrics-container {
   grid-template-columns: 1fr;
 }
 
 .gauge-container {
   grid-template-columns: 1fr;
 }
 
 .status-container {
   grid-template-columns: 1fr;
 }
 
 .analysis-metrics {
   grid-template-columns: 1fr;
 }
}
</style>