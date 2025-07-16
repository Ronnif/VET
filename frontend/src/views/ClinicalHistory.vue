<template>
  <div class="historial-container">
    <h1>Historial Clínico</h1>
    <div style="margin-bottom: 1.2rem;">
      <button
        v-if="role === 'veterinario'"
        @click="abrirModalAgregar('')"
      >
        Agregar nueva observación
      </button>
    </div>

    <div>
      <label>Filtrar por mascota:</label>
      <select v-model="filtroPetId" @change="fetchHistorial">
        <option value="">Todas</option>
        <option v-for="pet in pets" :key="pet.id" :value="pet.id">{{ pet.name }}</option>
      </select>
    </div>
    <div class="historial-list">
      <div
        class="historial-card"
        v-for="h in historial"
        :key="h.id"
        :class="{
          'principal': h.appointment_id,
          'seguimiento': !h.appointment_id
        }"
      >
        <div class="historial-header">
          <span class="historial-mascota">{{ nombreMascota(h.pet_id) }}</span>
          <span class="historial-fecha">{{ formatearFecha(h.date) }}</span>
          <span
            v-if="h.appointment_id"
            class="badge-principal"
          >Principal</span>
          <span
            v-else
            class="badge-seguimiento"
          >Seguimiento</span>
        </div>
        <div class="historial-extra">
          <span v-if="h.owner_name">Dueño: {{ h.owner_name }}</span>
          <span v-if="h.service_name"> | Servicio: {{ h.service_name }}</span>
        </div>
        <div class="historial-vet">
          <span>Veterinario: {{ h.veterinarian_name || 'Desconocido' }}</span>
        </div>
        <div class="historial-observacion">
          {{ h.observation }}
        </div>
        <div class="historial-actions">
          <button @click="descargarObservacion(h)">Descargar PDF</button>
          <button
            v-if="h.veterinarian_name === currentVetName"
            @click="editarObservacion(h)"
          >Editar</button>
        </div>
      </div>
    </div>

    <!-- Modal para agregar observación -->
    <div v-if="showModalObs" class="modal-backdrop">
      <div class="modal">
        <h3>Agregar nueva observación</h3>
        <label>Mascota:</label>
        <multiselect
          v-model="modalObs.pet_id"
          :options="mascotasAtendidas"
          :custom-label="pet => pet.name"
          placeholder="Seleccione una mascota"
          label="name"
          track-by="id"
        />
        <span v-if="mascotasAtendidas.length === 0" style="color: #c00; font-size: 0.95rem;">
          No hay mascotas atendidas por usted.
        </span>
        <textarea v-model="modalObs.observation" placeholder="Observación" required></textarea>
        <button @click="guardarObsCard" :disabled="!modalObs.pet_id || !modalObs.observation">Guardar</button>
        <button @click="cerrarModalObs">Cancelar</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../axios'
import jsPDF from 'jspdf'
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.min.css'

const historial = ref([])
const pets = ref([])
const filtroPetId = ref('')
const role = ref('')
const modalObs = ref({ pet_id: '', observation: '' })
const currentVetName = ref('')
const currentVetId = ref('')
const showModalObs = ref(false)

onMounted(async () => {
  role.value = localStorage.getItem('role') || ''
  currentVetName.value = localStorage.getItem('user_name') || ''
  currentVetId.value = localStorage.getItem('user_id') || ''
  await fetchMascotas()
  await fetchHistorial()
})

async function fetchMascotas() {
  const res = await api.get('/pets')
  pets.value = res.data
}

async function fetchHistorial() {
  let url = '/reports/clinical-history'
  const params = []
  if (filtroPetId.value) params.push(`pet_id=${filtroPetId.value}`)
  if (role.value === 'veterinario') {
    const vetId = localStorage.getItem('user_id')
    params.push(`vet_id=${vetId}`)
  }
  if (params.length) url += '?' + params.join('&')
  const res = await api.get(url)
  historial.value = res.data.sort((a, b) => b.date.localeCompare(a.date))
}

function nombreMascota(id) {
  const pet = pets.value.find(p => p.id === id)
  return pet ? pet.name : 'Mascota'
}

function descargarObservacion(h) {
  const doc = new jsPDF()
  doc.setFontSize(16)
  doc.text('Historial Clínico', 14, 18)
  doc.setFontSize(12)
  doc.text(`Mascota: ${nombreMascota(h.pet_id)}`, 14, 30)
  if (h.owner_name) doc.text(`Dueño: ${h.owner_name}`, 14, 38)
  if (h.service_name) doc.text(`Servicio: ${h.service_name}`, 14, 46)
  doc.text(`Veterinario: ${h.veterinarian_name || 'Desconocido'}`, 14, 54)
  doc.text(`Fecha: ${formatearFecha(h.date)}`, 14, 62)
  doc.text('Observación:', 14, 74)
  doc.setFontSize(11)
  doc.text(h.observation || '', 14, 82, { maxWidth: 180 })
  doc.save(`historial_${nombreMascota(h.pet_id)}_${h.date}.pdf`)
}

function formatearFecha(fechaIso) {
  if (!fechaIso) return ''
  const fecha = new Date(fechaIso)
  const dia = String(fecha.getDate()).padStart(2, '0')
  const mes = String(fecha.getMonth() + 1).padStart(2, '0')
  const anio = fecha.getFullYear()
  const horas = String(fecha.getHours()).padStart(2, '0')
  const minutos = String(fecha.getMinutes()).padStart(2, '0')
  return `${dia}/${mes}/${anio} ${horas}:${minutos}`
}

function abrirModalAgregar(pet_id = '') {
  modalObs.value = { pet_id, observation: '' }
  showModalObs.value = true
}
function cerrarModalObs() {
  modalObs.value = { pet_id: '', observation: '' }
  showModalObs.value = false
}
function editarObservacion(h) {
  modalObs.value = {
    pet_id: h.pet_id,
    observation: h.observation,
    id: h.id // Guarda el id para saber que es edición
  }
  showModalObs.value = true
}

// Modifica guardarObsCard para actualizar si existe id:
async function guardarObsCard() {
  try {
    if (modalObs.value.id) {
      // Editar observación existente
      await api.put(`/clinical-history/${modalObs.value.id}`, {
        observation: modalObs.value.observation
      })
    } else {
      // Nueva observación
      await api.post('/clinical-history', {
        pet_id: typeof modalObs.value.pet_id === 'object' ? modalObs.value.pet_id.id : modalObs.value.pet_id,
        observation: modalObs.value.observation
      })
    }
    await fetchHistorial()
    cerrarModalObs()
  } catch (error) {
    alert('Error al guardar observación: ' + (error.response?.data?.msg || error.message))
  }
}

// Filtrar mascotas atendidas por el veterinario autenticado usando el ID
const mascotasAtendidas = computed(() =>
  pets.value.filter(pet =>
    historial.value.some(
      h =>
        h.pet_id === pet.id &&
        String(h.vet_id) === String(currentVetId.value) &&
        h.appointment_id
    )
  )
)
</script>

<style scoped>
.historial-container {
  max-width: 1200px;
  margin: 2rem auto;
  width: 100%;
  background: none;
  border-radius: 0;
  box-shadow: none;
  padding: 0;
}
.historial-list {
  height: calc(100vh - 180px); /* Ajusta este valor según tu layout */
  overflow-y: auto;
  margin-top: 2rem;
  border-radius: 10px;
  box-shadow: 0 1px 8px 0 rgba(33,150,243,0.04);
  background: #fff;
  padding: 1rem 1rem 2.5rem 1rem; /* Más padding inferior */
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}
@media (max-width: 900px) {
  .historial-container {
    padding: 1rem 0.5rem;
    width: 100%;
  }
  .historial-list {
    padding: 1rem 0.5rem 1rem 0.5rem;
    max-height: calc(100vh - 100px);
  }
  form {
    flex-direction: column;
    gap: 0.5rem;
  }
}

h1 {
  color: #1976d2;
  font-weight: 800;
  margin-bottom: 1.2rem;
  letter-spacing: 1px;
}

button {
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.5rem 1.5rem;
  font-size: 1.05rem;
  font-weight: 700;
  cursor: pointer;
  margin: 0.5rem 0.5rem 1rem 0;
  transition: background 0.2s;
  box-shadow: 0 1px 4px 0 rgba(33,150,243,0.04);
}
button:disabled {
  background: #b0bec5;
  color: #222;
  cursor: not-allowed;
}
button:hover:not(:disabled) {
  background: #368a6e;
}

form {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
  align-items: center;
  background: #f7fafd;
  border-radius: 10px;
  padding: 1rem 1.5rem;
}

form select,
form textarea {
  border-radius: 6px;
  border: 1px solid #b0bec5;
  font-size: 1rem;
  padding: 0.4rem 0.8rem;
  background: #fff;
}

form textarea {
  min-width: 220px;
  min-height: 40px;
  resize: vertical;
}

label {
  font-weight: 600;
  color: #1976d2;
  font-size: 1.05rem;
  margin-right: 0.5rem;
}

select {
  border-radius: 6px;
  border: 1px solid #b0bec5;
  font-size: 1rem;
  padding: 0.4rem 0.8rem;
  background: #fff;
  margin-bottom: 1rem;
}

/* --- Cards --- */
.historial-card {
  background: #607d8b;
  color: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 12px 0 rgba(33,150,243,0.07);
  padding: 1.2rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  border: 1.5px solid #e3eafc;
}
.historial-card.principal {
  border-left: 6px solid #1976d2;
  background: #f3f7fd;
}
.historial-card.seguimiento {
  border-left: 6px solid #42b983;
  background: #f6fcf9;
}

.historial-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 700;
  color: #1976d2;
  font-size: 1.08rem;
  margin-bottom: 0.2rem;
}

.historial-mascota {
  font-weight: 800;
  font-size: 1.1rem;
}

.historial-fecha {
  color: #888;
  font-size: 0.98rem;
  font-weight: 400;
}

.historial-extra {
  color: #888;
  font-size: 0.97rem;
  margin-bottom: 0.2rem;
}

.historial-vet {
  color: #555;
  font-size: 0.95rem;
  font-weight: 500;
  margin-bottom: 0.2rem;
}

.historial-observacion {
  color: #222;
  font-size: 1.07rem;
  white-space: pre-line;
  word-break: break-word;
  margin-bottom: 0.2rem;
}

.historial-actions {
  display: flex;
  justify-content: flex-end;
}

.historial-actions button {
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.5rem 1.5rem;
  font-size: 1.05rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
  box-shadow: 0 1px 4px 0 rgba(33,150,243,0.04);
}
.historial-actions button:hover {
  background: #368a6e;
}

/* --- Modal --- */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: #fff;
  border-radius: 16px;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 8px 32px 0 rgba(33,150,243,0.18);
  position: relative;
}
.modal h3 {
  margin-bottom: 1rem;
  color: #1976d2;
  font-weight: 800;
  font-size: 1.2rem;
  text-align: center;
}
.modal textarea {
  width: 100%;
  min-height: 100px;
  border: 1px solid #b0bec5;
  border-radius: 6px;
  padding: 0.8rem;
  font-size: 1rem;
  margin-bottom: 1rem;
  resize: none;
}

.modal button {
  width: 48%;
  padding: 0.7rem;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  border: none;
  border-radius: 6px;
  transition: background 0.2s;
  box-shadow: 0 2px 8px 0 rgba(33,150,243,0.1);
}

.modal button:hover {
  background: #368a6e;
  color: #fff;
}

/* Multiselect scroll for many options */
.modal .multiselect__content {
  max-height: 140px;
  overflow-y: auto;
}
</style>