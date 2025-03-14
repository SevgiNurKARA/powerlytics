<template>
  <div class="container" style="background-color: #ffffff;">
    <!-- Header -->
    <div class="header">
      <h1>Powerlytics Enerji İzleme Sistemi</h1>
      <nav class="navigation">
        <a 
          v-for="item in navItems" 
          :key="item.path"
          :href="'#' + item.path"
          class="nav-item"
          :class="{ active: currentPath === item.path }"
          @click.prevent="navigateTo(item.path)"
        >
          <font-awesome-icon :icon="item.icon.split('fa-')[1]" />
          {{ item.name }}
        </a>
      </nav>
      <div class="user-info">
        <span>{{ selectedFirm && selectedFirm.name }}</span>
        <button @click="toggleDropdown" class="user-button">
          <font-awesome-icon icon="user" />
        </button>
        <div v-if="dropdownOpen" class="user-dropdown">
          <div class="dropdown-header">Firma Seçin</div>
          <div 
            v-for="firm in firms" 
            :key="firm.name"
            class="dropdown-item"
            @click="selectFirm(firm)"
          >
            {{ firm.name }}
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="main-content">
      <router-view :selectedFirm="selectedFirm" :energyData="energyData"></router-view>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import router from '@/router'

const route = useRouter()
 
const currentPath = computed(() => route.path)

const navItems = [
  { name: 'Gösterge Paneli', path: '/', icon: 'fa-gauge' },
  { name: 'Analiz', path: '/analysis', icon: 'fa-chart-line' },
  { name: 'Raporlar', path: '/reports', icon: 'fa-file-lines' },
  { name: 'Ayarlar', path: '/settings', icon: 'fa-gears' }
]

const dropdownOpen = ref(false)
const selectedFirm = ref(null)
const energyData = ref([])

// Firmaların verileri
const firms = ref([
  { name: "Firma A", id: 1 },
  { name: "Firma B", id: 2 },
  { name: "Firma C", id: 3 },
  { name: "Firma D", id: 4 }
])

// Başlangıçta ilk firmayı seç
selectedFirm.value = firms.value[0]

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const selectFirm = (firm) => {
  selectedFirm.value = firm
  dropdownOpen.value = false
  fetchEnergyData(firm.id)
}

const fetchEnergyData = async (firmId) => {
  try {
    const response = await axios.get(`/api/energy-data?firmId=${firmId}`)
    energyData.value = response.data
  } catch (error) {
    console.error("Enerji verileri alınırken hata oluştu:", error)
  }
}

const onMounted = () => {
  fetchEnergyData(selectedFirm.value.id)
}

const navigateTo = (path) => {
  route.push(path)
}
</script>

<style>
/* Reset default styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  margin: 0;
  padding: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background-color: #ffffff;
}

body {
  font-family: 'Inter', sans-serif;
  line-height: 1.5;
}

.container {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #111827;
  color: white;
  overflow: hidden;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #1F2937;
  border-bottom: 1px solid #374151;
}

.header h1 {
  font-size: 1.5rem;
  font-weight: bold;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
}

.user-button {
  padding: 0.5rem;
  border-radius: 0.375rem;
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  transition: background-color 0.2s;
}

.user-button:hover {
  background-color: #374151;
}

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  background-color: #1F2937;
  border: 1px solid #374151;
  border-radius: 0.5rem;
  width: 200px;
  z-index: 50;
}

.dropdown-header {
  padding: 0.75rem 1rem;
  color: #9CA3AF;
  font-size: 0.875rem;
  
}

.dropdown-item {
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.dropdown-item:hover {
  background-color: #374151;
}

.navigation {
  display: flex;
  padding: 1rem 2rem;
  background-color: #1F2937;
  
  gap: 1rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  color: #9CA3AF;
  text-decoration: none;
  transition: all 0.2s;
}

.nav-item:hover {
  background-color: #374151;
  color: white;
}

.nav-item.active {
  background-color: #374151;
  color: white;
}

.nav-item i {
  font-size: 1rem;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}

/* Transition animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>