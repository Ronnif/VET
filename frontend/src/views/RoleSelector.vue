<template>
  <div class="role-selector-bg">
    <div class="role-selector-card">
      <h2>¿Con qué rol deseas operar?</h2>
      <div class="role-buttons">
        <button
          v-for="r in roles"
          :key="r.label"
          @click="onRoleClick(r.value)"
          class="role-btn"
          :style="{ background: r.bg }"
        >
          <span class="role-icon">{{ r.icon }}</span>
          <span class="role-label">{{ r.label }}</span>
        </button>
      </div>
      <!-- Selector de veterinario solo si el admin selecciona veterinario -->
      <div v-if="selectedRole === 'veterinario' && veterinarios.length" class="vets-list">
        <h3>Selecciona veterinario:</h3>
        <div class="vet-buttons">
          <button
            v-for="vet in veterinarios"
            :key="vet.id"
            :class="['vet-btn', { selected: selectedVetId === vet.id }]"
            @click="selectedVetId = vet.id; seleccionarRol('veterinario')"
          >
            <span class="vet-name">{{ vet.username }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../axios'

const roles = [
  { value: 'admin', label: 'Admin', icon: '👨🏻‍💼', bg: 'linear-gradient(135deg, #ff9800 80%, #ffc107 100%)' },
  { value: 'recepcionista', label: 'Recepcionista', icon: '👨🏻‍💻', bg: 'linear-gradient(135deg, #ff5252 80%, #ff867f 100%)' },
  { value: 'veterinario', label: 'Veterinario', icon: '👨🏻‍⚕️', bg: 'linear-gradient(135deg, #00bcd4 80%, #2196f3 100%)' }
]
const router = useRouter()
const selectedRole = ref('')
const veterinarios = ref([])
const selectedVetId = ref('')

// Si el usuario es admin y selecciona veterinario, carga la lista de veterinarios
async function onRoleClick(rol) {
  selectedRole.value = rol
  if (rol === 'veterinario') {
    veterinarios.value = await api.get('/users?role=veterinario').then(r => r.data)
  } else {
    seleccionarRol(rol)
  }
}

function seleccionarRol(rol) {
  localStorage.setItem('role', rol)
  if (rol === 'veterinario' && selectedVetId.value) {
    localStorage.setItem('vet_id', selectedVetId.value)
  } else {
    localStorage.removeItem('vet_id')
  }
  router.push('/dashboard')
}
</script>

<style scoped>
.role-selector-bg {
  min-height: 100vh;
  width: 100vw;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}
.role-selector-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 8px 32px 0 rgba(60, 60, 60, 0.10);
  padding: 2.5rem 2.5rem 2rem 2.5rem;
  min-width: 320px;
  max-width: 95vw;
  width: 370px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
h2 {
  color: #222;
  margin-bottom: 2rem;
  font-weight: 700;
  text-align: center;
}
.role-buttons {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  width: 100%;
}
.role-btn {
  width: 100%;
  min-height: 90px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 1.15rem;
  font-weight: 600;
  box-shadow: 0 2px 8px 0 rgba(60, 60, 60, 0.10);
  cursor: pointer;
  transition: transform 0.12s, box-shadow 0.12s;
  outline: none;
  position: relative;
}
.role-btn:hover {
  transform: translateY(-2px) scale(1.03);
  box-shadow: 0 4px 16px 0 rgba(60, 60, 60, 0.18);
}
.role-icon {
  font-size: 2.1rem;
  margin-bottom: 0.4rem;
  display: block;
}
.role-label {
  font-size: 1.1rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}
.vets-list {
  margin-top: 1.5rem;
  width: 100%;
}
.vet-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}
.vet-btn {
  width: 100%;
  padding: 1rem;
  border-radius: 10px;
  border: 2px solid #2196f3;
  background: #e3f2fd;
  color: #222;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, border 0.2s;
}
.vet-btn.selected,
.vet-btn:hover {
  background: #2196f3;
  color: #fff;
  border-color: #1976d2;
}
.vet-name {
  display: block;
}
</style>