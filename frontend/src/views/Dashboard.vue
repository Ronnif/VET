<template>
  <div class="dashboard-layout">
    <aside :class="['sidebar', { collapsed: isCollapsed }]">
      <button class="collapse-btn" @click="isCollapsed = !isCollapsed">
        <span class="sidebar-icon"><i class="fas fa-bars"></i></span>
      </button>
      <ul>
        <li>
          <button @click="goToHome">
            <span class="sidebar-icon"><i class="fas fa-home"></i></span>
            <span v-if="!isCollapsed">Inicio</span>
          </button>
        </li>
        <li v-if="role === 'admin'">
          <button @click="goTo('users')">
            <span class="sidebar-icon"><i class="fas fa-user"></i></span>
            <span v-if="!isCollapsed">Gestión de Usuarios</span>
          </button>
        </li>
        <li v-if="role === 'admin'">
          <button @click="goTo('services')">
            <span class="sidebar-icon"><i class="fas fa-tools"></i></span>
            <span v-if="!isCollapsed">Gestión de Servicios</span>
          </button>
        </li>
        <li v-if="role === 'admin'">
          <button @click="goTo('reports')">
            <span class="sidebar-icon"><i class="fas fa-chart-bar"></i></span>
            <span v-if="!isCollapsed">Reportes</span>
          </button>
        </li>
        <li v-if="role === 'admin'">
          <button @click="cambiarRol">
            <span class="sidebar-icon"><i class="fas fa-random"></i></span>
            <span v-if="!isCollapsed">Cambiar de rol</span>
          </button>
        </li>
        <li v-if="role === 'admin'">
          <button @click="logout">
            <span class="sidebar-icon"><i class="fas fa-sign-out-alt"></i></span>
            <span v-if="!isCollapsed">Cerrar sesión</span>
          </button>
        </li>

        <li v-if="role === 'recepcionista'">
          <button @click="goTo('payments')">
            <span class="sidebar-icon"><i class="fas fa-money-bill-wave"></i></span>
            <span v-if="!isCollapsed">Pagos</span>
          </button>
        </li>
        <li v-if="role === 'recepcionista'">
          <button @click="goTo('clinical-history')">
            <span class="sidebar-icon"><i class="fas fa-notes-medical"></i></span>
            <span v-if="!isCollapsed">Historial Clínico</span>
          </button>
        </li>
        <li v-if="role === 'recepcionista'">
          <button @click="goTo('clients')">
            <span class="sidebar-icon"><i class="fas fa-users"></i></span>
            <span v-if="!isCollapsed">Gestión de Clientes</span>
          </button>
        </li>
        <li v-if="role === 'recepcionista'">
          <button @click="goTo('appointments')">
            <span class="sidebar-icon"><i class="fas fa-calendar-alt"></i></span>
            <span v-if="!isCollapsed">Gestión de Citas</span>
          </button>
        </li>
        <li v-if="role === 'recepcionista'">
          <button @click="logout">
            <span class="sidebar-icon"><i class="fas fa-sign-out-alt"></i></span>
            <span v-if="!isCollapsed">Cerrar sesión</span>
          </button>
        </li>

        <li v-if="role === 'veterinario'">
          <button @click="goTo('my-quotes')">
            <span class="sidebar-icon"><i class="fas fa-calendar-check"></i></span>
            <span v-if="!isCollapsed">Mis Citas</span>
          </button>
        </li>
        <li v-if="role === 'veterinario'">
          <button @click="goTo('clinical-history')">
            <span class="sidebar-icon"><i class="fas fa-notes-medical"></i></span>
            <span v-if="!isCollapsed">Historial Clínico</span>
          </button>
        </li>
        <li v-if="role === 'veterinario'">
          <button @click="logout">
            <span class="sidebar-icon"><i class="fas fa-sign-out-alt"></i></span>
            <span v-if="!isCollapsed">Cerrar sesión</span>
          </button>
        </li>
      </ul>
    </aside>
    <!-- Solo el contenido principal, no sidebar -->
    <div class="main-section">
      <header class="dashboard-header">
        <div class="header-left">
          <span class="clinic-name">🐾 SunsetVet</span>
        </div>
        <div class="header-right">
          <div class="user-avatar" :title="roleLabel">
            <span v-if="role === 'admin'">👨🏻‍💼</span>
            <span v-else-if="role === 'recepcionista'">👨🏻‍💻</span>
            <span v-else-if="role === 'veterinario'">🩺</span>
          </div>
        </div>
      </header>
      <div :class="['dashboard-content', { 'collapsed-content': isCollapsed }]">
        <template v-if="route.path === '/dashboard'">
          <h1 class="font-bold text-3xl mb-6">
            <span v-if="role === 'admin'">Panel de Administrador</span>
            <span v-else-if="role === 'veterinario'">Panel de Veterinario</span>
            <span v-else-if="role === 'recepcionista'">Panel de Recepcionista</span>
          </h1>

          <div class="row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4 mt-4">
            <div
              v-for="card in filteredCards"
              :key="card.label"
              class="col"
            >
              <div
                :class="['card', card.bg, 'text-white', 'shadow', 'mb-4', 'dashboard-card']"
                style="cursor:pointer; transition:transform 0.18s, box-shadow 0.18s;"
                @click="goTo(card.route)"
              >
                <div class="card-body d-flex flex-column align-items-center justify-content-center py-4">
                  <i :class="[card.icon, 'fs-1 mb-3']"></i>
                  <span class="fw-bold fs-4">{{ card.label }}</span>
                </div>
              </div>
            </div>
          </div>
        </template>
        <router-view v-else />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { ref, onMounted, computed, watch } from 'vue'

const router = useRouter()
const route = useRoute()
const role = ref('')
const isCollapsed = ref(false)

onMounted(() => {
  role.value = localStorage.getItem('role') || 'admin'
  isCollapsed.value = route.path !== '/dashboard'
})

watch(
  () => route.fullPath,
  () => {
    isCollapsed.value = route.path !== '/dashboard'
  }
)

// Tarjetas disponibles (puedes agregar/quitar según tu app)
const cards = [
  { label: 'Gestión de Usuarios', icon: 'bi-person-badge', bg: 'bg-primary', route: 'users', roles: ['admin'] },
  { label: 'Gestión de Servicios', icon: 'bi-tools', bg: 'bg-warning', route: 'services', roles: ['admin'] },
  { label: 'Reportes', icon: 'bi-bar-chart-line', bg: 'bg-danger', route: 'reports', roles: ['admin'] },
  { label: 'Pagos', icon: 'bi-credit-card-2-front', bg: 'bg-info', route: 'payments', roles: ['recepcionista'] },
  { label: 'Historial Clínico', icon: 'bi-journal-medical', bg: 'bg-success', route: 'clinical-history', roles: ['recepcionista', 'veterinario'] },
  { label: 'Gestión de Clientes', icon: 'bi-people', bg: 'bg-secondary', route: 'clients', roles: ['recepcionista'] },
  { label: 'Gestión de Citas', icon: 'bi-calendar-event', bg: 'bg-dark', route: 'appointments', roles: ['recepcionista'] },
  { label: 'Mis Citas', icon: 'bi-calendar-check', bg: 'bg-primary', route: 'my-quotes', roles: ['veterinario'] }
]

// Solo muestra las tarjetas permitidas para el rol
const filteredCards = computed(() =>
  cards.filter(card => card.roles.includes(role.value))
)

function goTo(section) {
  router.push(`/dashboard/${section}`)
}

function goToHome() {
  router.push('/dashboard')
}

function cambiarRol() {
  router.push('/role-selector')
}

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('expiresAt')
  localStorage.removeItem('role')
  sessionStorage.removeItem('userRole')
  router.push('/login')
}

const roleLabel = computed(() => {
  if (role.value === 'admin') return 'Administrador'
  if (role.value === 'recepcionista') return 'Recepcionista'
  if (role.value === 'veterinario') return 'Veterinario'
  return ''
})
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  min-height: 100vh;
  background: #f6f8fc;
}
.sidebar {
  width: 200px;
  min-width: 60px;
  max-width: 100vw;
  height: 100vh;
  background: #ffffff;
  box-shadow: 0 4px 32px 0 rgba(44, 62, 80, 0.10);
  display: flex;
  flex-direction: column;
  align-items: stretch;
  padding: 32px 0 24px 0;
  box-sizing: border-box;
  overflow: hidden;
  transition: width 0.3s cubic-bezier(.4,2,.6,1), background 0.3s;
}

.sidebar.collapsed {
  width: 64px;
  transition: width 0.3s cubic-bezier(.4,2,.6,1), background 0.3s;
}
.collapse-btn {
  width: 100%;
  margin: 0 0 18px 0;
  border-radius: 0;
  padding: 12px 0; /* Igual que los otros botones */
  background: none;
  border: none;
  text-align: left;
  font-size: 1.08rem;
  color: #222b45;
  display: flex;
  align-items: center;
  gap: 16px;
  box-sizing: border-box;
  cursor: pointer;
}
.sidebar.collapsed .collapse-btn {
  margin-left: 10px;
}
.sidebar h2 {
  font-size: 1.15rem;
  font-weight: 700;
  margin: 0 0 28px 0;
  padding-left: 0;
  color: #2563eb;
  letter-spacing: 1px;
}
.sidebar.collapsed h2 {
  opacity: 0;
  height: 0;
  margin: 0;
  padding: 0;
}
.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.sidebar li {
  margin-bottom: 8px;
  width: 100%;
}
.sidebar button {
  width: 100%;
  background: none;
  border: none;
  text-align: left;
  padding: 12px 0; /* Sin padding lateral */
  font-size: 1.08rem;
  color: #222b45;
  display: flex;
  align-items: center;
  border-radius: 0;
  transition: background 0.18s, color 0.18s;
  cursor: pointer;
  margin: 0 0 6px 0;
  font-weight: 500;
  box-sizing: border-box;
  overflow: hidden;
}
.sidebar button:hover,
.sidebar button:focus {
  background: #e7edfb;
  color: #2563eb;
  transform: none; /* Quita el translateX y scale */
  outline: none;
  z-index: 1;
}
.sidebar-icon {
  font-size: 1.3rem;
  min-width: 38px;
  text-align: center;
  color: #2563eb;
  opacity: 0.95;
  transition: color 0.18s, transform 0.18s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.sidebar button:hover .sidebar-icon,
.sidebar button:focus .sidebar-icon {
  color: #7c3aed;
  transform: scale(1.15) rotate(-8deg);
}
.sidebar.collapsed span:not(.sidebar-icon) {
  display: none !important;
}

/* HEADER */
.dashboard-header {
  height: 68px;
  background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 48px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 16px 0 rgba(44, 62, 80, 0.10);
}
.header-left .clinic-name {
  font-size: 2rem;
  font-weight: 900;
  letter-spacing: 2px;
  display: flex;
  align-items: center;
  gap: 14px;
  text-shadow: 0 4px 16px rgba(0,0,0,0.10);
  color: #fff;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 22px;
}

.user-avatar {
  background: linear-gradient(135deg, #fff 60%, #e3e6ff 100%);
  color: #7c3aed;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
  box-shadow: 0 2px 16px 0 rgba(44, 62, 80, 0.13);
  cursor: pointer;
  border: 2.5px solid #fff;
  transition: box-shadow 0.2s, transform 0.2s;
}
.user-avatar:hover {
  box-shadow: 0 4px 24px 0 rgba(44, 62, 80, 0.25);
  transform: scale(1.07);
}

/* Ajuste para el contenido principal */
.main-section {
  flex: 1;
  min-width: 0;
  /* Elimina display: flex y flex-direction aquí */
}
.dashboard-content {
  flex: 1;
  min-height: 0;
  background: #f6f8fc;
  padding: 22px 0 0 28px;
  transition: padding-left 0.3s cubic-bezier(.4,2,.6,1);
  /* Elimina display: flex y flex-direction aquí */
}
.collapsed-content {
  padding-left: 64px !important;
  transition: padding-left 0.3s cubic-bezier(.4,2,.6,1);
}
.dashboard-card {
  border-radius: 12px;
  box-shadow: 0 4px 24px 0 rgba(44, 62, 80, 0.13);
  transition: transform 0.18s, box-shadow 0.18s;
}
.dashboard-card:hover {
  transform: translateY(-6px) scale(1.03);
  box-shadow: 0 8px 32px 0 rgba(44, 62, 80, 0.18);
  filter: brightness(1.08);
}
.dashboard-card .card-body i {
  transition: transform 0.18s;
}
.dashboard-card:hover .card-body i {
  transform: scale(1.18) rotate(-8deg);
}
</style>