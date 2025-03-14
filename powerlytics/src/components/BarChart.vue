<template>
    <div class="chart-wrapper">
      <div class="chart-bars">
        <div 
          v-for="(item, index) in data" 
          :key="index" 
          class="bar-container"
        >
          <div 
            class="bar" 
            :style="{ height: getBarHeight(item.value) }"
            :class="{
              'bar-optimal': item.isOptimal,
              'bar-current': item.isCurrent && !item.isOptimal,
              'bar-default': !item.isOptimal && !item.isCurrent
            }"
          ></div>
          <div class="bar-value">{{ formatValue(item.value) }}</div>
          <div class="bar-label">{{ item.label }}</div>
        </div>
      </div>
      <div class="legend">
        <div class="legend-item">
          <div class="legend-color bar-current"></div>
          <div>Mevcut Saat Dilimi</div>
        </div>
        <div class="legend-item">
          <div class="legend-color bar-optimal"></div>
          <div>Optimal Saat Dilimi</div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      data: {
        type: Array,
        required: true
      }
    },
    setup(props) {
      const getMaxValue = () => {
        return Math.max(...props.data.map(item => item.value)) * 1.1; // %10 padding
      };
      
      const getBarHeight = (value) => {
        const maxHeight = 200; // px
        const maxValue = getMaxValue();
        return `${(value / maxValue) * maxHeight}px`;
      };
      
      const formatValue = (value) => {
        return Number(value).toFixed(2) + ' TL';
      };
      
      return {
        getBarHeight,
        formatValue
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
  
  .chart-bars {
    display: flex;
    justify-content: space-around;
    align-items: flex-end;
    height: 250px;
    padding: 1rem;
  }
  
  .bar-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 60px;
  }
  
  .bar {
    width: 30px;
    background-color: #64748B;
    border-radius: 4px 4px 0 0;
    transition: height 0.5s ease;
  }
  
  .bar-default {
    background-color: #64748B;
  }
  
  .bar-current {
    background-color: #3B82F6;
  }
  
  .bar-optimal {
    background-color: #10B981;
  }
  
  .bar-value {
    margin-top: 8px;
    font-size: 0.8rem;
    color: #D1D5DB;
  }
  
  .bar-label {
    margin-top: 4px;
    font-size: 0.8rem;
    color: #D1D5DB;
    text-align: center;
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
  </style>