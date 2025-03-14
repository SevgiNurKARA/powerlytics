<template>
  <div class="chart-wrapper">
    <div class="chart-area">
      <!-- Y ekseni -->
      <div class="y-axis">
        <div class="y-label" v-for="(value, index) in yAxisLabels" :key="'y-'+index" :style="{ bottom: `${index * 20}%` }">
          {{ value }}
        </div>
      </div>
      
      <!-- Scatter plot alanı -->
      <div class="plot-area">
        <!-- Izgara çizgileri -->
        <div class="grid-lines y-grid">
          <div class="grid-line" v-for="i in 5" :key="'grid-y-'+i" :style="{ bottom: `${i * 20}%` }"></div>
        </div>
        <div class="grid-lines x-grid">
          <div class="grid-line" v-for="i in 5" :key="'grid-x-'+i" :style="{ left: `${i * 20}%` }"></div>
        </div>
        
        <!-- Regresyon çizgisi -->
        <div class="regression-line" :style="getRegressionLineStyle()"></div>
        
        <!-- Veri noktaları -->
        <div 
          v-for="(point, index) in data.basePoints" 
          :key="'base-'+index" 
          class="data-point base-point"
          :style="getPointStyle(point)"
          :title="`x: ${point.x.toFixed(1)}, y: ${point.y.toFixed(1)}`"
        ></div>
        
        <div 
          v-for="(point, index) in data.efficiencyPoints" 
          :key="'eff-'+index" 
          class="data-point efficiency-point"
          :style="getPointStyle(point)"
          :title="`x: ${point.x.toFixed(1)}, y: ${point.y.toFixed(1)}`"
        ></div>
      </div>
      
      <!-- X ekseni -->
      <div class="x-axis">
        <div class="x-label" v-for="(value, index) in xAxisLabels" :key="'x-'+index" :style="{ left: `${index * 20}%` }">
          {{ value }}
        </div>
      </div>
    </div>
    
    <!-- Açıklama -->
    <div class="legend">
      <div class="legend-item">
        <div class="legend-color base-point"></div>
        <div>Standart Tüketim</div>
      </div>
      <div class="legend-item">
        <div class="legend-color efficiency-point"></div>
        <div>Verimli Tüketim</div>
      </div>
      <div class="legend-item">
        <div class="legend-color regression-line-sample"></div>
        <div>Regresyon Doğrusu</div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';

export default {
 // ScatterChart.vue içinde
props: {
  data: {
    type: Object,
    default: () => ({
      basePoints: [],
      efficiencyPoints: [],
      regressionLine: {
        start: { x: 0, y: 0 },
        end: { x: 100, y: 100 }
      }
    })
  }
},
  setup(props) {
    const xAxisLabels = computed(() => {
      return [70, 80, 90, 100].map(value => `${value}%`);
    });
    
    const yAxisLabels = computed(() => {
      return [0, 25, 50, 75, 100].map(value => `${value} kWh`);
    });
    
    const getPointStyle = (point) => {
      // Nokta pozisyonunu hesapla
      const x = (point.x - 70) / 30 * 100; // 70-100 aralığını 0-100% aralığına dönüştür
      const y = point.y / 100 * 100; // 0-100 aralığını 0-100% aralığına dönüştür
      
      return {
        left: `${x}%`,
        bottom: `${y}%`
      };
    };
    
    const getRegressionLineStyle = () => {
      const start = props.data.regressionLine.start;
      const end = props.data.regressionLine.end;
      
      const x1 = (start.x - 70) / 30 * 100;
      const y1 = start.y / 100 * 100;
      const x2 = (end.x - 70) / 30 * 100;
      const y2 = end.y / 100 * 100;
      
      // SVG çizgi yerine CSS transform kullanıyoruz
      const length = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
      const angle = Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI;
      
      return {
        width: `${length}%`,
        left: `${x1}%`,
        bottom: `${y1}%`,
        transform: `rotate(${angle}deg)`,
        transformOrigin: 'left bottom'
      };
    };
    
    return {
      xAxisLabels,
      yAxisLabels,
      getPointStyle,
      getRegressionLineStyle
    };
  }
}
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chart-area {
  flex: 1;
  position: relative;
  padding: 20px 40px;
  height: 250px;
}

.plot-area {
  position: absolute;
  top: 20px;
  right: 40px;
  bottom: 40px;
  left: 60px;
  border-left: 1px solid #4B5563;
  border-bottom: 1px solid #4B5563;
}

.y-axis {
  position: absolute;
  left: 0;
  top: 20px;
  bottom: 40px;
  width: 60px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.y-label {
  position: absolute;
  right: 10px;
  transform: translateY(50%);
  font-size: 0.7rem;
  color: #9CA3AF;
}

.x-axis {
  position: absolute;
  left: 60px;
  right: 40px;
  bottom: 0;
  height: 40px;
}

.x-label {
  position: absolute;
  top: 10px;
  transform: translateX(-50%);
  font-size: 0.7rem;
  color: #9CA3AF;
}

.grid-lines {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}

.grid-line {
  position: absolute;
  background-color: #374151;
}

.y-grid .grid-line {
  left: 0;
  right: 0;
  height: 1px;
}

.x-grid .grid-line {
  top: 0;
  bottom: 0;
  width: 1px;
}

.data-point {
  position: absolute;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  transform: translate(-50%, 50%);
}

.base-point {
  background-color: #F87171;
}

.efficiency-point {
  background-color: #10B981;
}

.regression-line {
  position: absolute;
  height: 2px;
  background-color: #60A5FA;
}

.legend {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
  gap: 2rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
}

.regression-line-sample {
  background-color: #60A5FA;
}
</style>