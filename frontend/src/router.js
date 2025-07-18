import { createRouter, createWebHistory } from 'vue-router'
import Login from './views/Login.vue'
import RoleSelector from './views/RoleSelector.vue' 
import Dashboard from './views/Dashboard.vue'
import Users from './views/Users.vue'
import Appointments from './views/Appointments.vue'
import Payments from './views/Payments.vue'
import ClinicalHistory from './views/ClinicalHistory.vue'
import Services from './views/Services.vue'
import Clients from './views/Clients.vue'
import Reports from './views/Reports.vue'
import MyQuotes from './views/MyQuotes.vue'
import Pet from './views/Pet.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/role-selector', component: RoleSelector, meta: { requiresAuth: true, roles: ['admin'] } },
  {
    path: '/dashboard',
    component: Dashboard,
    meta: { requiresAuth: true },
    children: [
      { path: 'users', component: Users, meta: { requiresAuth: true, roles: ['admin'] } },
      { path: 'appointments', component: Appointments, meta: { requiresAuth: true } },
      { path: 'payments', component: Payments, meta: { requiresAuth: true } },
      { path: 'clinical-history', component: ClinicalHistory, meta: { requiresAuth: true } },
      { path: 'services', component: Services, meta: { requiresAuth: true, roles: ['admin'] } },
      { path: 'clients', component: Clients, meta: { requiresAuth: true } },
      { path: 'clients/:id/pets', component: Pet, meta: { requiresAuth: true }, props: route => ({ clienteId: route.params.id }) },
      { path: 'my-quotes', component: MyQuotes, meta: { requiresAuth: true } },
      { path: 'reports', component: Reports, meta: { requiresAuth: true } }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard para proteger rutas privadas
router.beforeEach((to, from) => {
  const token = localStorage.getItem('token')
  const expiresAt = localStorage.getItem('expiresAt')
  const isAuthenticated = !!token && expiresAt && Date.now() < Number(expiresAt)

  // Si no está autenticado, siempre redirige a login
  if (!isAuthenticated) {
    localStorage.removeItem('token')
    localStorage.removeItem('expiresAt')
    localStorage.removeItem('role')
    if (to.path !== '/login') return { path: '/login' }
    return true
  }

  // Si la ruta requiere roles y el rol no coincide, redirige al dashboard
  if (to.meta.roles && (!localStorage.getItem('role') || !to.meta.roles.includes(localStorage.getItem('role')))) {
    return { path: '/dashboard' }
  }

  // Si ya está autenticado y va a /login, redirige al dashboard
  if (to.path === '/login' && isAuthenticated) {
    return { path: '/dashboard' }
  }

  return true
})

export default router