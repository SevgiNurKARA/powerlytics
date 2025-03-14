import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)


/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import { faUser, faGauge, faChartLine, faFileLines, faGears } from '@fortawesome/free-solid-svg-icons'

/* add icons to the library */
library.add(faUser, faGauge, faChartLine, faFileLines, faGears)



// Router'ı kullan
app.use(router)

// Font Awesome bileşenini global olarak kaydet
app.component('font-awesome-icon', FontAwesomeIcon)

// Uygulamayı başlat
app.mount('#app')
