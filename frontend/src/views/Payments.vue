<template>
  <div>
    <h1>Pagos</h1>
    <button @click="showForm = !showForm">
      {{ showForm ? 'Cancelar' : 'Registrar Pago' }}
    </button>
    <div v-if="showForm">
      <h3>Citas atendidas pendientes de pago</h3>
      <div v-if="citasPendientes.length === 0">
        <em>No hay citas pendientes de pago.</em>
      </div>
      <div class="table-scroll">
        <table v-if="citasPendientes.length">
          <thead>
            <tr>
              <th>Mascota</th>
              <th>Cliente</th>
              <th>Fecha</th>
              <th>Servicio</th>
              <th>Monto</th>
              <th>Método de pago</th>
              <th>Acción</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="cita in citasPendientes" :key="cita.id">
              <td>{{ nombreMascota(cita.pet_id) }}</td>
              <td>{{ nombreCliente(cita.client_id) }}</td>
              <td>{{ cita.date }}</td>
              <td>{{ nombreServicio(cita.service_id) }}</td>
              <td>{{ obtenerPrecioServicio(cita.service_id) }}</td>
              <td>
                <select v-model="metodoPago[cita.id]" required>
                  <option disabled value="">Selecciona</option>
                  <option value="efectivo">Efectivo</option>
                  <option value="tarjeta">Tarjeta</option>
                  <option value="transferencia">Transferencia</option>
                </select>
              </td>
              <td>
                <button 
                  :disabled="!metodoPago[cita.id]" 
                  @click="registrarPagoDirecto(cita)">
                  Registrar Pago
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <h2>Citas Pagadas</h2>
    <div class="table-scroll">
      <table>
        <thead>
          <tr>
            <th>Mascota</th>
            <th>Cliente</th>
            <th>Fecha</th>
            <th>Monto</th>
            <th>Método</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pago in pagos" :key="pago.id">
            <td>{{ nombreMascota(pago.pet_id) }}</td>
            <td>{{ nombreCliente(pago.client_id) }}</td>
            <td>{{ formatearSoloFecha(pago.date) }}</td>
            <td>{{ pago.payment_amount ? pago.payment_amount : 'No registrado' }}</td>
            <td>{{ pago.payment_method ? pago.payment_method : 'No registrado' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../axios'

const showForm = ref(false)
const pagos = ref([])
const citasPendientes = ref([])
const pets = ref([])
const clients = ref([])
const servicios = ref([])
const metodoPago = ref({})

onMounted(async () => {
  await fetchPagos()
  await fetchCitasPendientes()
  await fetchMascotas()
  await fetchClientes()
  await fetchServicios()
})

async function fetchPagos() {
  const res = await api.get('/payments')
  pagos.value = res.data
}

async function fetchCitasPendientes() {
  const res = await api.get('/appointments')
  citasPendientes.value = res.data.filter(
    c => !c.paid && c.status && c.status.toLowerCase() === 'atendida'
  )
}

async function fetchMascotas() {
  const res = await api.get('/pets')
  pets.value = res.data
}

async function fetchClientes() {
  const res = await api.get('/clients')
  clients.value = res.data
}

async function fetchServicios() {
  const res = await api.get('/services')
  servicios.value = res.data
}

function nombreMascota(id) {
  const pet = pets.value.find(p => p.id === id)
  return pet ? pet.name : 'Mascota'
}

function nombreCliente(id) {
  const client = clients.value.find(c => c.id === id)
  return client ? client.name : 'Cliente'
}

function nombreServicio(id) {
  const servicio = servicios.value.find(s => s.id === id)
  return servicio ? servicio.name : 'Servicio'
}

function obtenerPrecioServicio(id) {
  const servicio = servicios.value.find(s => s.id === id)
  return servicio ? servicio.price : ''
}

async function registrarPagoDirecto(cita) {
  try {
    await api.post('/payments', {
      appointment_id: cita.id,
      payment_amount: obtenerPrecioServicio(cita.service_id),
      payment_method: metodoPago.value[cita.id]
    })
    await fetchPagos()
    await fetchCitasPendientes()
    metodoPago.value[cita.id] = ''
    showForm.value = false
  } catch (error) {
    alert('Error al registrar pago: ' + (error.response?.data?.msg || error.message))
  }
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
/* Elimina .pagos-container y usa el mismo patrón que Citas */
h1, h2, h3 {
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

.table-scroll {
  max-width: 1200px;
  margin: 2rem auto;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px 0 rgba(0,0,0,0.08);
  padding: 2rem 2.5rem 2.5rem 2.5rem;
  max-height: 340px;
  overflow-y: auto;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: transparent;
  font-size: 1.07rem;
  margin-bottom: 2rem;
  box-shadow: 0 1px 8px 0 rgba(33,150,243,0.04);
  border-radius: 10px 10px 0 0;
  overflow: hidden;
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
}

tbody tr:nth-child(even) {
  background: #f7fafd;
}
tbody tr:nth-child(odd) {
  background: #fff;
}

select {
  border-radius: 6px;
  border: 1px solid #b0bec5;
  font-size: 1rem;
  padding: 0.4rem 0.8rem;
  background: #fff;
}

em {
  color: #888;
  font-size: 1.05rem;
}

@media (max-width: 900px) {
  table, th, td {
    font-size: 0.97rem;
  }
}
</style>