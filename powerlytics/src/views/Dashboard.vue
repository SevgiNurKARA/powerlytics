<template>
  <div class="dashboard">
    <h2>Gösterge Paneli</h2>
    <div class="dashboard-content">
      <!-- Gauge Meters Grid -->
      <div class="gauge-container">
        <div class="gauge-item">
          <h3>Frekans</h3>
          <CircularProgress 
            :value="selectedFirm?.frequency || 51" 
            :max="100"
            unit="Hz"
            color="green"
          />
        </div>

        <div class="gauge-item">
          <h3>Voltaj</h3>
          <CircularProgress 
            :value="selectedFirm?.voltage || 224" 
            :max="400"
            unit="V"
            color="blue"
          />
        </div>

        <div class="gauge-item">
          <h3>Güç</h3>
          <CircularProgress 
            :value="selectedFirm?.power || 19" 
            :max="50"
            unit="kW"
            color="green"
          />
        </div>

        <div class="gauge-item">
          <h3>Akım</h3>
          <CircularProgress 
            :value="selectedFirm?.current || 14" 
            :max="30"
            unit="A"
            color="yellow"
          />
        </div>
      </div>

      <!-- Status Indicators -->
      <div class="status-container">
        <div class="status-item temperature">
          <h3>A1_Sıcaklık</h3>
          <div class="value">20 °C</div>
        </div>

        <div class="status-item humidity">
          <h3>A1_Nem</h3>
          <div class="value">53 %</div>
        </div>

        <div class="status-item smoke">
          <h3>Duman Sensörü</h3>
          <div class="value">0 digital</div>
        </div>

        <div class="status-item door">
          <h3>Kapı Sensörü</h3>
          <div class="value">0 digital</div>
        </div>
      </div>

      <!-- Info Panels -->
      <div class="info-panel">
        <h3>Koridor Sıcaklıkları</h3>
        <div class="corridor-temps">
          <div class="temp-item">
            <span>A1</span>
            <span>20 °C</span>
          </div>
          <div class="temp-item">
            <span>A2</span>
            <span>30 °C</span>
          </div>
          <div class="temp-item">
            <span>A3</span>
            <span>32 °C</span>
          </div>
          <div class="temp-item">
            <span>A4</span>
            <span>32 °C</span>
          </div>
        </div>
      </div>

      <div class="info-panel">
        <h3>UPS1 Enerji Tüketim Verileri</h3>
        <div class="machine-selector">
          <label for="machineType">Makine Türü:</label>
          <select 
            id="machineType" 
            v-model="selectedMachineType" 
            class="machine-select"
            @change="updatePrediction"
          >
            <option value="">Makine Seçiniz</option>
            <option value="Pompa">Pompa</option>
            <option value="LPG Kompresörü">LPG Kompresörü</option>
            <option value="Hava Kompresörü">Hava Kompresörü</option>
          </select>
        </div>
        <div class="ups-data">
          <div class="data-item">
            <span>Güç</span>
            <span>{{ selectedFirm.power }} kW</span>
          </div>
          <div class="data-item">
            <span>Akım</span>
            <span>{{ selectedFirm.current }} A</span>
          </div>
          <div class="data-item">
            <span>Voltaj</span>
            <span>{{ selectedFirm.voltage }} V</span>
          </div>
          <div class="data-item">
            <span>Frekans</span>
            <span>{{ selectedFirm.frequency }} Hz</span>
          </div>
          <div class="data-item prediction">
            <span>Verimlilik</span>
            <span>{{ calculateEfficiency }}%</span>
          </div>
          <div class="data-item prediction">
            <span>AI Önerisi</span>
            <span :class="{ 'warning': prediction }">
              {{ selectedMachineType ? (prediction || 'Yükleniyor...') : 'Lütfen makine türü seçiniz' }}
            </span>
          </div>
        </div>
        <button 
          @click="updatePrediction" 
          class="update-btn"
          :disabled="!selectedMachineType"
        >
          Tahmin Güncelle
        </button>
      </div>

      <!-- Charts Grid -->
      <div class="charts-container">
        <div class="chart-item">
          <h3>Akım Grafiği</h3>
          <EnergyChart :data="currentChartData" />
        </div>

        <div class="chart-item">
          <h3>Sıcaklık Grafiği</h3>
          <EnergyChart :data="tempChartData" />
        </div>
      </div>

      <!-- Alarm Panel -->
      <div class="alarm-panel">
        <h3>Aktif Alarmlar ({{ alarms.length }})</h3>
        <div class="alarm-content">
          <div v-for="alarm in alarms" :key="alarm.id" class="alarm-item">
            <div class="alarm-header">
              <span>{{ alarm.type }}</span>
              <span class="alarm-value">{{ alarm.value }}</span>
            </div>
            <div class="alarm-info">
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import CircularProgress from '../components/CircularProgress.vue'
import EnergyChart from '../components/EnergyChart.vue'

// Örnek veri seti (15 dakikalık aralıklarla)
const sampleData = [
  { time: '00:00', power: 19, current: 14, voltage: 224, frequency: 51, efficiency: 75 },
  { time: '00:15', power: 21, current: 15, voltage: 223, frequency: 50, efficiency: 70 },
  { time: '00:30', power: 23, current: 16, voltage: 225, frequency: 51, efficiency: 65 },
  { time: '00:45', power: 25, current: 17, voltage: 222, frequency: 50, efficiency: 60 },
  { time: '01:00', power: 22, current: 15, voltage: 224, frequency: 51, efficiency: 68 },
  { time: '01:15', power: 20, current: 14, voltage: 225, frequency: 50, efficiency: 72 },
  { time: '01:30', power: 18, current: 13, voltage: 223, frequency: 51, efficiency: 78 },
  { time: '01:45', power: 24, current: 16, voltage: 224, frequency: 50, efficiency: 63 }
]

const currentDataIndex = ref(0)
const updateInterval = ref(null)
const alarms = ref([])

// Seçili firma verisi - şimdi dinamik olarak güncellenecek
const selectedFirm = ref({
  name: "Firma A",
  frequency: sampleData[0].frequency,
  voltage: sampleData[0].voltage,
  power: sampleData[0].power,
  current: sampleData[0].current,
  efficiency: sampleData[0].efficiency,
  dailyChange: -5.2,
  currentUsage: 42.5,
  activePower: 3.2,
  reactivePower: 0.8
})

// Veri güncelleme fonksiyonu
const updateData = () => {
  currentDataIndex.value = (currentDataIndex.value + 1) % sampleData.length
  const newData = sampleData[currentDataIndex.value]
  
  selectedFirm.value = {
    ...selectedFirm.value,
    frequency: newData.frequency,
    voltage: newData.voltage,
    power: newData.power,
    current: newData.current,
    efficiency: newData.efficiency
  }

  // Verimlilik kontrolü ve alarm oluşturma
  if (newData.efficiency < 65) {
    const alarm = {
      id: Date.now(),
      type: 'Verimlilik Alarmı',
      message: `Kritik verimlilik seviyesi: ${newData.efficiency}%`,
      value: `${newData.efficiency}%`,
      timestamp: new Date().toLocaleTimeString()
    }
    alarms.value = [alarm, ...alarms.value]
  }

  // Tahmin güncelleme
  if (selectedMachineType.value) {
    updatePrediction()
  }

  // Grafik verilerini güncelle
  updateChartData(newData)
}

// Grafik verilerini güncelleme
const updateChartData = (newData) => {
  const currentTime = newData.time
  
  // Akım grafiği güncelleme
  currentChartData.value.datasets[0].data.shift()
  currentChartData.value.datasets[0].data.push(newData.current)
  currentChartData.value.labels.shift()
  currentChartData.value.labels.push(currentTime)
}

// Grafik verileri
const currentChartData = ref({
  labels: ['00:00', '00:05', '00:10', '00:15', '00:20', '00:25', '00:30'],
  datasets: [{
    label: 'Akım (A)',
    data: [14, 13.8, 14.2, 13.9, 14.1, 13.7, 14],
    borderColor: '#10B981',
    tension: 0.4
  }]
})

const tempChartData = computed(() => ({
  labels: ['00:00', '00:05', '00:10', '00:15', '00:20', '00:25', '00:30'],
  datasets: [{
    label: 'Sıcaklık (°C)',
    data: [20, 20.5, 20.2, 20.8, 20.4, 20.6, 20.3],
    borderColor: '#3B82F6',
    tension: 0.4
  }]
}))

const selectedMachineType = ref('')
const prediction = ref(null)
const energyData = ref({
  cekilen_enerji: 0,
  kullanilan_enerji: 0
})

// Verimlilik hesaplama - artık gerçek veriye dayalı
const calculateEfficiency = computed(() => {
  return selectedFirm.value.efficiency
})

// AI tahmin fonksiyonu - mevcut implementasyon
const updatePrediction = async () => {
  if (!selectedMachineType.value) {
    prediction.value = null
    return
  }

  try {
    const requestData = {
      firma_adi: selectedFirm.value.name,
      makine_turu: selectedMachineType.value,
      cekilen_enerji: selectedFirm.value.power * 1.2, // Örnek çekilen enerji hesabı
      kullanilan_enerji: selectedFirm.value.power,
      calisma_durumu: 1,
      verimlilik: calculateEfficiency.value,
      saat_dilimi: new Date().getHours().toString().padStart(2, '0') + ':' + 
                   new Date().getMinutes().toString().padStart(2, '0')
    }

    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestData)
    })

    const data = await response.json()
    prediction.value = data.oneri
  } catch (error) {
    console.error('Tahmin alınırken hata oluştu:', error)
    prediction.value = 'Hata: ' + error.message
  }
}

// Component lifecycle hooks
onMounted(() => {
  // 15 dakikada bir veri güncelleme (demo için 15 saniye yapalım)
  updateInterval.value = setInterval(updateData, 15000)
})

onUnmounted(() => {
  if (updateInterval.value) {
    clearInterval(updateInterval.value)
  }
})
</script>

<style scoped>
.dashboard {
  width: 100%;
  height: 100%;
  padding: 1.5rem 2rem;
  display: flex;
  flex-direction: column;
  background-color: #111827;
  overflow: hidden;
  margin: 0 auto;
  max-width: 100%;
}

.dashboard h2 {
  margin-bottom: 20px;
  color: #fff;
  padding: 0;
}

.dashboard-content {
  flex: 1;
  width: 100%;
  display: grid;
  grid-template-rows: auto auto auto 1fr auto;
  gap: 20px;
  overflow-y: auto;
  background-color: #111827;
  padding-right: 10px;
  margin: 0 auto;
  max-width: 100%;
}

.gauge-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  width: 100%;
  margin: 0 auto;
}

.gauge-item {
  background-color: #1f2937;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

.gauge-item h3 {
  color: #9ca3af;
  margin-bottom: 15px;
}

.status-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.status-item {
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

.status-item h3 {
  color: #9ca3af;
  margin-bottom: 10px;
}

.status-item .value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #fff;
}

.temperature { background-color: #1f2937; }
.humidity { background-color: #7f1d1d; }
.smoke { background-color: #5b21b6; }
.door { background-color: #9a3412; }

.info-panel {
  background-color: #1f2937;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.info-panel h3 {
  color: #9ca3af;
  margin-bottom: 15px;
}

.corridor-temps, .ups-data {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.temp-item, .data-item {
  display: flex;
  justify-content: space-between;
  color: #fff;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
  min-height: 300px;
}

.chart-item {
  background-color: #1f2937;
  padding: 20px;
  border-radius: 8px;
  min-height: 300px;
  display: flex;
  flex-direction: column;
}

.chart-item h3 {
  color: #9ca3af;
  margin-bottom: 15px;
}

.alarm-panel {
  background-color: rgba(185, 28, 28, 0.2);
  border: 1px solid #ef4444;
  padding: 20px;
  border-radius: 8px;
}

.alarm-panel h3 {
  color: #f87171;
  margin-bottom: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.alarm-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.alarm-item {
  background-color: rgba(239, 68, 68, 0.1);
  padding: 15px;
  border-radius: 6px;
  border-left: 4px solid #ef4444;
}

.alarm-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  color: #fff;
  font-weight: 600;
}

.alarm-value {
  color: #f87171;
  font-weight: bold;
}

.alarm-info {
  color: #9ca3af;
  font-size: 0.9rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.alarm-time {
  color: #6b7280;
  font-size: 0.8rem;
}

.no-alarms {
  color: #9ca3af;
  text-align: center;
  padding: 20px;
  font-style: italic;
}

.ups-data {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.data-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  background-color: #1F2937;
  border-radius: 0.5rem;
}

.data-item span:first-child {
  color: #9CA3AF;
  font-size: 0.875rem;
}

.data-item span:last-child {
  color: #fff;
  font-size: 1.25rem;
  font-weight: 600;
}

.data-item.prediction {
  background-color: #374151;
}

.warning {
  color: #F59E0B !important;
}

.machine-selector {
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.machine-selector label {
  color: #9CA3AF;
  font-size: 0.875rem;
}

.machine-select {
  padding: 0.5rem;
  border-radius: 0.375rem;
  background-color: #374151;
  color: white;
  border: 1px solid #4B5563;
  outline: none;
  cursor: pointer;
  min-width: 200px;
}

.machine-select:focus {
  border-color: #3B82F6;
}

.update-btn:disabled {
  background-color: #4B5563;
  cursor: not-allowed;
}

.update-btn {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #3B82F6;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.update-btn:hover {
  background-color: #2563EB;
}
</style> 