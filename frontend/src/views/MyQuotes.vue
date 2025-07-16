<template>
  <div>
    <h1>Mis Citas Asignadas</h1>
    <div v-if="role === 'admin'" style="margin-bottom: 1rem;">
      <label>Selecciona veterinario:
        <select v-model="selectedVetId">
          <option disabled value="">-- Selecciona --</option>
          <option v-for="vet in veterinarios" :key="vet.id" :value="vet.id">
            {{ vet.username }}
          </option>
        </select>
      </label>
    </div>
    <div class="table-scroll">
      <table>
        <thead>
          <tr>
            <th>Mascota</th>
            <th>Cliente</th>
            <th>Servicio</th>
            <th>Fecha</th>
            <th>Hora</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cita in citas" :key="cita.id">
            <td>{{ cita.pet?.name }}</td>
            <td>{{ cita.client?.name }}</td>
            <td>{{ cita.service?.name }}</td>
            <td>{{ formatearSoloFecha(cita.date) }}</td>
            <td>{{ cita.time }}</td>
            <td>{{ cita.status || 'Pendiente' }}</td>
            <td>
              <button @click="abrirObservacion(cita)">Agregar Observación</button>
              <button @click="verObservaciones(cita)">Ver Observaciones</button>
              <button v-if="cita.status?.toLowerCase() !== 'atendida'" @click="marcarAtendida(cita)">
                Marcar como Atendida
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal para agregar observación clínica -->
    <div v-if="mostrarModal">
      <div class="modal">
        <h3>Agregar Observación Clínica</h3>
        <textarea v-model="observacion" placeholder="Observación clínica"></textarea>
        <button @click="guardarObservacion">Guardar</button>
        <button @click="cerrarModal">Cancelar</button>
      </div>
    </div>

    <!-- Modal para ver observaciones clínicas -->
    <div v-if="mostrarObsModal">
      <div class="modal-backdrop"></div>
      <div class="modal">
        <h3>Observaciones clínicas</h3>
        <ul>
          <li v-for="obs in observaciones" :key="obs.id">
            {{ obs.observation }} <br>
            <small>{{ formatearFecha(obs.date) }}</small>
          </li>
        </ul>
        <button @click="cerrarObsModal">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '../axios'

const citas = ref([])
const mostrarModal = ref(false)
const citaSeleccionada = ref(null)
const observacion = ref('')

const mostrarObsModal = ref(false)
const observaciones = ref([])

const role = ref(localStorage.getItem('role') || '')
const veterinarios = ref([])
const selectedVetId = ref('')

onMounted(async () => {
  if (role.value === 'admin') {
    veterinarios.value = await api.get('/users?role=veterinario').then(r => r.data)
  }
  await cargarCitas()
})

async function cargarCitas() {
  // Si el admin está simulando veterinario
  if (role.value === 'veterinario' && localStorage.getItem('vet_id')) {
    const vetId = localStorage.getItem('vet_id')
    citas.value = await api.get(`/appointments/vet/${vetId}`).then(r => r.data)
  } else if (role.value === 'admin' && selectedVetId.value) {
    citas.value = await api.get(`/appointments/vet/${selectedVetId.value}`).then(r => r.data)
  } else if (role.value === 'veterinario') {
    citas.value = await api.get('/appointments/vet/me').then(r => r.data)
  } else {
    citas.value = []
  }
  citas.value = citas.value.sort((a, b) => new Date(b.date) - new Date(a.date))
}

watch(selectedVetId, cargarCitas)

function abrirObservacion(cita) {
  citaSeleccionada.value = cita
  observacion.value = ''
  mostrarModal.value = true
}

function cerrarModal() {
  mostrarModal.value = false
  citaSeleccionada.value = null
  observacion.value = ''
}

async function guardarObservacion() {
  if (!observacion.value) return
  await api.post('/clinical-history', {
    pet_id: citaSeleccionada.value.pet_id,
    observation: observacion.value,
    appointment_id: citaSeleccionada.value.id
  })
  cerrarModal()
}

async function marcarAtendida(cita) {
  await api.put(`/appointments/${cita.id}`, { status: 'atendida' })
  cita.status = 'atendida'
}

async function verObservaciones(cita) {
  observaciones.value = await api.get(`/clinical-history?appointment_id=${cita.id}`).then(r => r.data)
  mostrarObsModal.value = true
}

function cerrarObsModal() {
  mostrarObsModal.value = false
  observaciones.value = []
}

function formatearFecha(fechaIso) {
  if (!fechaIso) return ''
  const fecha = new Date(fechaIso)
  const dia = String(fecha.getDate()).padStart(2, '0')
  const mes = String(fecha.getMonth() + 1).padStart(2, '0')
  const anio = fecha.getFullYear()
  const hora = String(fecha.getHours()).padStart(2, '0')
  const min = String(fecha.getMinutes()).padStart(2, '0')
  return `${dia}/${mes}/${anio} ${hora}:${min}`
}

function formatearSoloFecha(fechaIso) {
  if (!fechaIso) return ''
  const fecha = new Date(fechaIso)
  const dia = String(fecha.getDate()).padStart(2, '0')
  const mes = String(fecha.getMonth() + 1).padStart(2, '0')
  const anio = fecha.getFullYear()
  return `${dia}/${mes}/${anio}`
}
</script>

<style scoped>
h1 {
  color: #1976d2;
  font-weight: 800;
  margin-bottom: 1.2rem;
  letter-spacing: 1px;
}

.table-scroll {
  max-height: 600px;
  overflow-y: auto;
  margin-top: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 1px 8px 0 rgba(33,150,243,0.04);
  background: #fff;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0; /* quita el margin extra */
  background: #fff;
  font-size: 1.07rem;
  /* Elimina border-radius y overflow aquí */
}

th, td {
  padding: 0.8rem 0.5rem;
  text-align: center;
  word-break: break-word;
}

th {
  background: #1976d2;
  color: #fff;
  font-weight: 700;
  border-bottom: 2px solid #b0bec5;
  position: sticky;
  top: 0;
  z-index: 2;
  /* Asegura que el fondo cubra toda la celda */
  background-clip: padding-box;
}

tbody tr:nth-child(even) {
  background: #f7fafd;
}
tbody tr:nth-child(odd) {
  background: #fff;
}

button {
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.4rem 1.1rem;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  margin: 0.2rem 0.2rem 0.2rem 0;
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

/* Fondo semitransparente para el modal */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(33, 150, 243, 0.10);
  z-index: 999;
}

/* Modal mejorado */
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  min-width: 340px;
  max-width: 95vw;
  transform: translate(-50%, -50%);
  background: #fff;
  padding: 2.2rem 2rem 1.5rem 2rem;
  border-radius: 16px;
  border: 1.5px solid #90caf9;
  box-shadow: 0 8px 32px 0 rgba(33,150,243,0.18);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  animation: modalIn 0.18s cubic-bezier(.4,0,.2,1);
}

@keyframes modalIn {
  from { opacity: 0; transform: translate(-50%, -60%) scale(0.97);}
  to   { opacity: 1; transform: translate(-50%, -50%) scale(1);}
}

.modal h3 {
  color: #1976d2;
  margin-bottom: 1.2rem;
  font-weight: 800;
  font-size: 1.35rem;
  text-align: center;
  letter-spacing: 1px;
}

.modal textarea {
  min-height: 80px;
  border-radius: 6px;
  border: 1px solid #b0bec5;
  padding: 0.5rem;
  margin-bottom: 1rem;
  font-size: 1rem;
  resize: vertical;
}

.modal ul {
  padding-left: 1.2rem;
  margin-bottom: 1.5rem;
}

.modal li {
  margin-bottom: 0.7rem;
  text-align: left;
}

.modal small {
  display: block;
  margin-top: 2px;
  font-size: 0.97em;
  color: #888;
}

.modal button {
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.7rem 0;
  font-size: 1.08rem;
  font-weight: 700;
  cursor: pointer;
  margin: 0.5rem auto 0 auto;
  width: 90%;
  transition: background 0.2s;
  box-shadow: 0 1px 4px 0 rgba(33,150,243,0.04);
  display: block;
}
.modal button:hover:not(:disabled) {
  background: #368a6e;
}

@media (max-width: 700px) {
  table, th, td {
    font-size: 0.97rem;
  }
  .modal {
    min-width: 90vw;
    padding: 1rem 0.5rem;
  }
}
</style>