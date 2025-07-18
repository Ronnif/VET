<template>
  <div class="historial-container">
    <h1>Historial Clínico</h1>
    <div style="margin-bottom: 1.2rem;">
      <button
        v-if="role === 'veterinario'"
        @click="iniciarAgregar"
        :disabled="editando"
      >
        Agregar nueva observación
      </button>
    </div>

    <!-- FORMULARIO DE AGREGAR/EDITAR -->
    <div v-if="editando" class="form-edicion">
      <h3>{{ modalObs.id ? 'Editar observación' : 'Agregar nueva observación' }}</h3>
      <label>Mascota:</label>
      <select v-model="modalObs.pet">
        <option v-for="pet in pets" :key="pet.id" :value="pet">{{ pet.name }}</option>
      </select>
      <label>Observación:</label>
      <textarea v-model="modalObs.observation" placeholder="Observación" required></textarea>
      <div style="display: flex; gap: 1rem;">
        <button @click="guardarObsCard" :disabled="!modalObs.pet || !modalObs.observation">
          Guardar
        </button>
        <button @click="cancelarEdicion">Cancelar</button>
      </div>
    </div>

    <!-- RESTO DE TU LISTA -->
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
          <span v-if="h.appointment_id" class="badge-principal">Principal</span>
          <span v-else class="badge-seguimiento">Seguimiento</span>
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
            v-if="h.vet_id === currentVetId"
            @click="iniciarEdicion(h)"
            :disabled="editando"
          >Editar</button>
        </div>
      </div>
    </div>
    <div style="height: 4rem;"></div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '../axios'
import { useToast } from 'vue-toastification'
import jsPDF from 'jspdf'

const toast = useToast()
const historial = ref([])
const pets = ref([])
const filtroPetId = ref('')
const role = ref('')
const modalObs = reactive({ pet: null, observation: '', id: null })
const currentVetName = ref('')
const currentVetId = ref(Number(localStorage.getItem('user_id')) || null)
const editando = ref(false)

onMounted(async () => {
  role.value = localStorage.getItem('role') || ''
  if (role.value !== 'veterinario' && role.value !== 'recepcionista') {
    window.location.href = '/'
    return
  }
  currentVetName.value = localStorage.getItem('user_name') || ''
  await fetchMascotas()
  await fetchHistorial()
})

async function fetchMascotas() {
  let res = await api.get('/pets')
  if (role.value === 'veterinario') {
    const resHist = await api.get(`/clinical-history?vet_id=${currentVetId.value}`)
    const atendidasIds = [...new Set(resHist.data.map(h => h.pet_id))]
    pets.value = res.data.filter(p => atendidasIds.includes(p.id))
  } else {
    pets.value = res.data
  }
}

async function fetchHistorial() {
  let url = '/clinical-history'
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

function iniciarAgregar() {
  modalObs.pet = pets.value.length > 0 ? pets.value[0] : null
  modalObs.observation = ''
  modalObs.id = null
  editando.value = true
}

function cancelarEdicion() {
  modalObs.pet = null
  modalObs.observation = ''
  modalObs.id = null
  editando.value = false
}

function iniciarEdicion(h) {
  modalObs.pet = pets.value.find(p => p.id === h.pet_id) || null
  modalObs.observation = h.observation
  modalObs.id = h.id
  editando.value = true
}

async function guardarObsCard() {
  try {
    if (modalObs.id) {
      await api.put(`/clinical-history/${modalObs.id}`, {
        observation: modalObs.observation
      })
      toast.success('Observación editada correctamente')
    } else {
      await api.post('/clinical-history', {
        pet_id: modalObs.pet.id,
        observation: modalObs.observation
      })
      toast.success('Observación agregada correctamente')
    }
    await fetchHistorial()
    cancelarEdicion()
  } catch (error) {
    toast.error('Error al guardar observación: ' + (error.response?.data?.msg || error.message))
  }
}

function formatearFecha(fecha) {
  if (!fecha) return ''
  const d = new Date(fecha)
  return d.toLocaleDateString('es-PE', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function descargarObservacion(h) {
  const doc = new jsPDF()
  const petName = nombreMascota(h.pet_id)
  const owner = h.owner_name || ''
  const vet = h.veterinarian_name || ''
  const service = h.service_name || ''
  const date = formatearFecha(h.date)
  const obs = h.observation || ''

  doc.setFontSize(16)
  doc.text('Historial Clínico', 10, 15)
  doc.setFontSize(12)
  doc.text(`Mascota: ${petName}`, 10, 30)
  doc.text(`Dueño: ${owner}`, 10, 40)
  doc.text(`Veterinario: ${vet}`, 10, 50)
  if (service) doc.text(`Servicio: ${service}`, 10, 60)
  doc.text(`Fecha: ${date}`, 10, 70)
  doc.text('Observación:', 10, 85)
  doc.setFontSize(11)
  doc.text(obs, 10, 95, { maxWidth: 180 })

  doc.save(`observacion_${petName}_${date}.pdf`)
}
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
  height: calc(100vh - 120px);
  overflow-y: auto;
  margin-top: 2rem;
  border-radius: 10px;
  box-shadow: 0 1px 8px 0 rgba(33,150,243,0.04);
  background: #fff;
  padding: 1rem 1rem 10rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}
.historial-list > .historial-card:last-child {
  margin-bottom: 20rem;
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
  width: 100%;
}

textarea {
  border-radius: 6px;
  border: 1px solid #b0bec5;
  font-size: 1rem;
  padding: 0.4rem 0.8rem;
  background: #fff;
  min-width: 220px;
  min-height: 60px;
  resize: vertical;
  width: 100%;
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

/* --- Formulario de edición --- */
.form-edicion {
  background: #f7fafd;
  border-radius: 10px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 1px 8px 0 rgba(33,150,243,0.04);
  max-width: 600px;
}
.form-edicion label {
  font-weight: 600;
  color: #1976d2;
  font-size: 1.05rem;
  margin-right: 0.5rem;
  display: block;
  margin-top: 1rem;
}
.form-edicion select,
.form-edicion textarea {
  border-radius: 6px;
  border: 1px solid #b0bec5;
  font-size: 1rem;
  padding: 0.4rem 0.8rem;
  background: #fff;
  width: 100%;
  margin-bottom: 1rem;
}
.form-edicion textarea {
  min-height: 60px;
  resize: vertical;
}
</style>