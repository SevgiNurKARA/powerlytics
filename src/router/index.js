import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Analysis from '../views/Analysis.vue'
import Reports from '../views/Reports.vue'
import Settings from '../views/Settings.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    props: true
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: Analysis,
    props: true
  },
  {
    path: '/reports',
    name: 'Reports',
    component: Reports,
    props: true
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    props: true
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guard to ensure page transitions work
router.beforeEach((to, from, next) => {
  // Add any necessary authentication or navigation guards here
  next()
})

export default router 