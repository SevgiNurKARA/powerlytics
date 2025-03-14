<template>
  <div class="circular-progress">
    <svg :width="size" :height="size" viewBox="0 0 100 100">
      <!-- Background circle -->
      <circle
        cx="50"
        cy="50"
        :r="radius"
        fill="none"
        :stroke="backgroundColor"
        :stroke-width="strokeWidth"
        class="background-circle"
      />
      
      <!-- Progress circle -->
      <circle
        cx="50"
        cy="50"
        :r="radius"
        fill="none"
        :stroke="color"
        :stroke-width="strokeWidth"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="strokeDashoffset"
        class="progress-circle"
      />
      
      <!-- Value text -->
      <text
        x="50"
        y="45"
        text-anchor="middle"
        :fill="textColor"
        class="progress-value"
      >
        {{ displayValue }}
      </text>
      
      <!-- Unit text -->
      <text
        x="50"
        y="65"
        text-anchor="middle"
        :fill="textColor"
        class="progress-unit"
      >
        {{ unit }}
      </text>
    </svg>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: {
    type: [Number, String],
    required: true
  },
  max: {
    type: Number,
    default: 100
  },
  size: {
    type: Number,
    default: 120
  },
  color: {
    type: String,
    default: '#3B82F6'
  },
  backgroundColor: {
    type: String,
    default: '#E5E7EB'
  },
  textColor: {
    type: String,
    default: '#f59e0b'
  },
  unit: {
    type: String,
    default: ''
  },
  strokeWidth: {
    type: Number,
    default: 8
  }
})

// Ensure value is treated as a number
const numericValue = computed(() => Number(props.value) || 0)

// Format display value
const displayValue = computed(() => {
  return numericValue.value.toLocaleString()
})

const radius = computed(() => 40 - props.strokeWidth / 2)
const circumference = computed(() => 2 * Math.PI * radius.value)
const progress = computed(() => {
  // Ensure progress is between 0 and 1
  const ratio = numericValue.value / props.max
  return Math.min(Math.max(ratio, 0), 1)
})
const strokeDashoffset = computed(() => 
  circumference.value * (1 - progress.value)
)
</script>

<style scoped>
.circular-progress {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  position: relative;
  width: 100%;
  height: 100%;
}

.progress-value {
  font-size: 24px;
  font-weight: bold;
}

.progress-unit {
  font-size: 14px;
  opacity: 0.8;
}

svg {
  overflow: visible;
  position: relative;
}

.background-circle {
  transform-origin: center;
}

.progress-circle {
  transform-origin: center;
  transform: rotate(-90deg);
  transition: stroke-dashoffset 0.35s;
}

circle {
  transition: stroke-dashoffset 0.35s;
}
</style>
