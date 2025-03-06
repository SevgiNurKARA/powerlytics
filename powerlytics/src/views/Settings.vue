<template>
  <div class="settings">
    <h2>Ayarlar</h2>
    <div class="settings-content">
      <div class="settings-section">
        <h3>Firma Bilgileri</h3>
        <div class="form-group">
          <label for="firmName">Firma Adı</label>
          <input type="text" id="firmName" v-model="firmName" placeholder="Firma adı giriniz">
        </div>
        <div class="form-group">
          <label for="contactEmail">İletişim E-posta</label>
          <input type="email" id="contactEmail" v-model="contactEmail" placeholder="E-posta adresi giriniz">
        </div>
        <div class="form-group">
          <label for="contactPhone">İletişim Telefon</label>
          <input type="tel" id="contactPhone" v-model="contactPhone" placeholder="Telefon numarası giriniz">
        </div>
      </div>

      <div class="settings-section">
        <h3>Bildirim Ayarları</h3>
        <div class="toggle-group">
          <label for="emailNotifications">E-posta Bildirimleri</label>
          <div class="toggle">
            <input type="checkbox" id="emailNotifications" v-model="emailNotifications">
            <span class="toggle-slider"></span>
          </div>
        </div>
        <div class="toggle-group">
          <label for="smsNotifications">SMS Bildirimleri</label>
          <div class="toggle">
            <input type="checkbox" id="smsNotifications" v-model="smsNotifications">
            <span class="toggle-slider"></span>
          </div>
        </div>
        <div class="toggle-group">
          <label for="alarmNotifications">Alarm Bildirimleri</label>
          <div class="toggle">
            <input type="checkbox" id="alarmNotifications" v-model="alarmNotifications">
            <span class="toggle-slider"></span>
          </div>
        </div>
      </div>

      <div class="settings-section">
        <h3>Sistem Ayarları</h3>
        <div class="form-group">
          <label for="dataRefreshRate">Veri Yenileme Sıklığı</label>
          <select id="dataRefreshRate" v-model="dataRefreshRate">
            <option value="5">5 saniye</option>
            <option value="15">15 saniye</option>
            <option value="30">30 saniye</option>
            <option value="60">1 dakika</option>
          </select>
        </div>
        <div class="form-group">
          <label for="theme">Tema</label>
          <select id="theme" v-model="theme">
            <option value="dark">Koyu Tema</option>
            <option value="light">Açık Tema</option>
            <option value="system">Sistem Teması</option>
          </select>
        </div>
      </div>

      <div class="settings-actions">
        <button class="save-btn" @click="saveSettings">Ayarları Kaydet</button>
        <button class="reset-btn" @click="resetSettings">Varsayılana Sıfırla</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  selectedFirm: {
    type: Object,
    required: true
  }
})

// Form state
const firmName = ref('Firma A')
const contactEmail = ref('info@firmaa.com')
const contactPhone = ref('0212 123 45 67')

// Notification settings
const emailNotifications = ref(true)
const smsNotifications = ref(false)
const alarmNotifications = ref(true)

// System settings
const dataRefreshRate = ref('15')
const theme = ref('dark')

// Methods
const saveSettings = () => {
  // Ayarları kaydetme işlemi
  alert('Ayarlar kaydedildi!')
}

const resetSettings = () => {
  // Ayarları sıfırlama işlemi
  firmName.value = 'Firma A'
  contactEmail.value = 'info@firmaa.com'
  contactPhone.value = '0212 123 45 67'
  emailNotifications.value = true
  smsNotifications.value = false
  alarmNotifications.value = true
  dataRefreshRate.value = '15'
  theme.value = 'dark'
}
</script>

<style scoped>
.settings {
  height: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.settings h2 {
  margin-bottom: 20px;
  color: #fff;
}

.settings-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.settings-section {
  background-color: #1f2937;
  padding: 20px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.settings-section h3 {
  color: #9ca3af;
  margin-bottom: 5px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  color: #9ca3af;
  font-size: 0.875rem;
}

.form-group input, .form-group select {
  padding: 10px;
  background-color: #374151;
  border: 1px solid #4b5563;
  border-radius: 6px;
  color: #fff;
  font-size: 1rem;
}

.form-group input:focus, .form-group select:focus {
  outline: none;
  border-color: #3b82f6;
}

.toggle-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.toggle-group label {
  color: #9ca3af;
  font-size: 0.875rem;
}

.toggle {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #4b5563;
  transition: .4s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: #3b82f6;
}

input:checked + .toggle-slider:before {
  transform: translateX(26px);
}

.settings-actions {
  grid-column: 1 / -1;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

.save-btn {
  padding: 10px 20px;
  background-color: #3b82f6;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.save-btn:hover {
  background-color: #2563eb;
}

.reset-btn {
  padding: 10px 20px;
  background-color: #4b5563;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.reset-btn:hover {
  background-color: #6b7280;
}
</style> 