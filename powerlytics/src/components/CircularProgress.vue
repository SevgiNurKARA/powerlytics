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
        transform="rotate(-90 50 50)"
      />
      
      <!-- Value text -->
      <text
        x="50"
        y="45"
        text-anchor="middle"
        :fill="textColor"
        class="progress-value"
      >
        {{ value }}
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
    type: Number,
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
    default: '#10B981'
  },
  backgroundColor: {
    type: String,
    default: '#374151'
  },
  textColor: {
    type: String,
    default: '#ffffff'
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

const radius = computed(() => 45 - props.strokeWidth / 2)
const circumference = computed(() => 2 * Math.PI * radius.value)
const progress = computed(() => props.value / props.max)
const strokeDashoffset = computed(() => 
  circumference.value * (1 - progress.value)
)
</script>

<style scoped>
.circular-progress {
  display: inline-flex;
  justify-content: center;
  align-items: center;
}

.progress-value {
  font-size: 24px;
  font-weight: bold;
}

.progress-unit {
  font-size: 14px;
  opacity: 0.8;
}

circle {
  transition: stroke-dashoffset 0.35s;
  transform-origin: 50% 50%;
}
</style>
