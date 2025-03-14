<template style="background-color: #ffffff;">
  <div class="analysis-container">
    <h2>Enerji Analizi</h2>
    
    <div v-if="loading" class="loading">Veriler yükleniyor...</div>
    
    <div v-else>
      <!-- Saat dilimi maliyet karşılaştırması grafiği -->
      <div class="chart-container">
        <h3>Saatlik Maliyet Karşılaştırması</h3>
        <div class="chart">
          <EnergyChart 
            :data="costChartData"
            :compare-data="previousCostChartData"
            compare-label="Önceki Dönem"
          />
        </div>
      </div>

      <!-- ISO 50001 Regresyon Grafiği -->
      <div class="chart-container">
        <h3>ISO 50001 Regresyon Analizi</h3>
        <div class="chart">
          <scatter-chart :data="regressionData" />
        </div>
      </div>

      <!-- Verimlilik ve Tasarruf Analizleri -->
      <div class="efficiency-analysis">
        <h3>Verimlilik Analizi</h3>
        <div class="analysis-grid">
          <div class="analysis-card">
            <h4>Mevcut Durum</h4>
            <p>Kullanılan Enerji: {{ formatNumber(currentData.kullanilan_enerji) }} kWh</p>
            <p>Çekilen Enerji: {{ formatNumber(currentData.cekilen_enerji) }} kWh</p>
            <p>Saat Dilimi: {{ currentData.saat_aralik }}</p>
            <p>Maliyet: {{ formatNumber(currentData.current_cost) }} TL</p>
            <p>Verimlilik: {{ formatNumber(currentData.efficiency) }}%</p>
          </div>
          
          <div class="analysis-card">
            <h4>Optimize Edilmiş</h4>
            <p>Önerilen Saat Dilimi: {{ currentData.optimal_time_range }}</p>
            <p>Optimize Maliyet: {{ formatNumber(currentData.optimal_cost) }} TL</p>
            <p>Potansiyel Tasarruf: {{ formatNumber(currentData.potential_savings) }} TL</p>
            <p>Tasarruf Yüzdesi: {{ formatNumber(currentData.savings_percentage) }}%</p>
          </div>
          
          <div class="analysis-card">
            <h4>ISO 50001 Değerlendirmesi</h4>
            <p>Değerlendirme: <span :class="getAssessmentClass()">{{ currentData.iso_assessment }}</span></p>
            <p>Karbon Ayak İzi: {{ formatNumber(currentData.carbon_footprint) }} kg CO₂</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import EnergyChart from '@/components/EnergyChart.vue';
import ScatterChart from '@/components/ScatterChart.vue';

const loading = ref(true);
const currentData = ref({
  kullanilan_enerji: 0,
  cekilen_enerji: 0,
  saat_aralik: '',
  current_cost: 0,
  optimal_time_range: '',
  optimal_cost: 0,
  potential_savings: 0,
  savings_percentage: 0,
  efficiency: 0,
  carbon_footprint: 0,
  iso_assessment: ''
});

// Maliyet karşılaştırma grafiği için veri
const costChartData = ref({
  labels: ['00-06', '06-12', '12-18', '18-24'],
  datasets: [{
    label: 'Mevcut Dönem Maliyeti (₺)',
    data: [3, 2, 4, 2],
    backgroundColor: '#3B82F6',
    borderColor: '#2563EB',
    borderWidth: 1
  }]
});

// Önceki dönem verileri için karşılaştırma
const previousCostChartData = ref({
  labels: ['00-06', '06-12', '12-18', '18-24'],
  datasets: [{
    label: 'Önceki Dönem Maliyeti (₺)',
    data: [5, 4, 3, 7],
    backgroundColor: '#10B981',
    borderColor: '#059669',
    borderWidth: 1
  }]
});

const regressionData = ref([]);

const fetchAnalysisData = async () => {
  try {
    // Örnek veri. Gerçek uygulamada kullanıcı girdilerini almalısınız
    const requestData = {
      cekilen_enerji: 100,
      kullanilan_enerji: 85,
      saat_dilimi: '14:00'
    };
    
    // API çağrısı yapılıyor
    try {
      // API URL'ini doğru şekilde ayarlayalım
      const API_URL = 'http://localhost:5000'; // Flask API port
      
      const response = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData),
        mode: 'cors', // CORS modunu açıkça belirt
        credentials: 'same-origin' // Çerezleri gönderme (gerekirse 'include' yapın)
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Ana veriyi ayarla
      currentData.value = {
        ...requestData,
        ...data,
        saat_aralik: data.current_time_range // Saat aralığını doğru şekilde ayarla
      };
      
      // Maliyet karşılaştırması için veriyi dönüştür
      updateChartData(data);
      
      console.log("API yanıtı başarılı:", data);
      
    } catch (apiError) {
      console.error("API çağrısı başarısız, demo veriler kullanılıyor", apiError);
      // Demo veriler
      const demoData = {
        current_time_range: '12-18',
        current_cost: 42.5,
        alternative_costs: {
          '00-06': 25.5,
          '06-12': 34.2,
          '12-18': 42.5,
          '18-24': 48.7
        },
        optimal_time_range: '00-06',
        optimal_cost: 25.5,
        potential_savings: 17.0,
        savings_percentage: 40.0,
        efficiency: 85.0,
        carbon_footprint: 34.0,
        iso_assessment: 'Verimli'
      };
      
      currentData.value = {
        ...requestData,
        ...demoData,
        saat_aralik: demoData.current_time_range
      };
      
      // Demo verilerle grafikleri güncelle
      updateChartData(demoData);
    }
    
    // Regresyon verisi için örnek veri
    regressionData.value = generateRegressionData(currentData.value.efficiency);
    
  } catch (error) {
    console.error("Veri işlenirken hata oluştu", error);
  } finally {
    loading.value = false;
  }
};

// Grafik verilerini güncelle
const updateChartData = (data) => {
  // Mevcut dönem verileri
  const timeRanges = ['00-06', '06-12', '12-18', '18-24'];
  
  costChartData.value.datasets[0].data = timeRanges.map(range => {
    // Eğer API'den gelen veri varsa onu kullan
    if (data.alternative_costs && data.alternative_costs[range]) {
      return data.alternative_costs[range];
    }
    
    switch (range) {
      case '00-06':
        return 2.5; // Gece aralığı için varsayılan değer
      case '06-12':
        return 3.75; // Sabah aralığı için varsayılan değer
      case '12-18':
        return 3.75; // Öğleden sonra aralığı için varsayılan değer
      case '18-24':
        return 2.5; // Akşam aralığı için varsayılan değer
      default:
        return 0;
    }
  });
  
  // Önceki dönem için örnek veriler (gerçek uygulamada API'den alınabilir)
  previousCostChartData.value.datasets[0].data = timeRanges.map(range => {
    // Her aralık için farklı değerler
    switch (range) {
      case '00-06':
        return 4.3; // Önceki dönem gece aralığı
      case '06-12':
        return 5; // Önceki dönem sabah aralığı
      case '12-18':
        return 5.2; // Önceki dönem öğleden sonra aralığı
      case '18-24':
        return 4.2; // Önceki dönem akşam aralığı
      default:
        return 0;
    }
  });
};

// Verimlilik değerine dayalı örnek regresyon verisi oluştur
const generateRegressionData = (efficiency) => {
  const basePoints = [];
  const efficiency_points = [];
  
  // Son 10 veri noktası için üret
  for (let i = 0; i < 10; i++) {
    const x = 70 + Math.random() * 30; // Random activity level
    const y_base = x * 0.8 + Math.random() * 10; // Baz tüketim
    const y_efficient = x * (efficiency / 100) + Math.random() * 5; // Verimli tüketim
    
    basePoints.push({ x, y: y_base });
    efficiency_points.push({ x, y: y_efficient });
  }
  
  return {
    basePoints,
    efficiencyPoints: efficiency_points,
    regressionLine: { 
      start: { x: 70, y: 70 * 0.8 },
      end: { x: 100, y: 60 * 0.8 }
    }
  };
};

const formatNumber = (value) => {
  return Number(value).toFixed(2);
};

const getAssessmentClass = () => {
  const assessment = currentData.value.iso_assessment;
  if (assessment === 'Verimli') return 'assessment-good';
  if (assessment === 'Orta') return 'assessment-medium';
  return 'assessment-poor';
};

onMounted(fetchAnalysisData);
</script>

<style scoped>
.analysis-container {
  padding: 2rem;
  color: white;
  background-color: #ffffff;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  padding: 2rem;
}

.chart-container {
  background: #ffffff;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 2rem;
  border: 1px solid #d2d2d2;
  color: #000000;
}

.chart {
  height: 300px;
  width: 100%;
}

.efficiency-analysis {
  background: #ffffff;
  padding: 1rem;
  border-radius: 0.5rem;
  border: 1px solid #d2d2d2;
}

.analysis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.analysis-card {
  background: #d2d2d2;
  padding: 1rem;
  border-radius: 0.5rem;
  color: #000000;
}

h2 {
  font-size: 1.8rem;
  color: #000000;
  margin-bottom: 1.5rem;
}

h3 {
  font-size: 1.4rem;
  margin-bottom: 1rem;
  color: #000000;
}

h4 {
  font-size: 1.2rem;
  margin-bottom: 0.8rem;
  color: #000000;
}

.assessment-good {
  color: #10B981;
  font-weight: bold;
}

.assessment-medium {
  color: #F59E0B;
  font-weight: bold;
}

.assessment-poor {
  color: #EF4444;
  font-weight: bold;
}
</style>