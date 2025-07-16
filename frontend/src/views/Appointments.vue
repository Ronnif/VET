<template>
  <div>
    <h1>Gestión de Citas</h1>
    <button @click="showForm = !showForm">
      {{ showForm ? 'Cancelar' : 'Agendar Cita' }}
    </button>

    <form v-if="showForm" @submit.prevent="agendarCita" class="form">
      <select v-model="nuevaCita.client_id" required>
        <option disabled value="">Selecciona un cliente</option>
        <option v-for="cliente in clientes" :key="cliente.id" :value="cliente.id">
          {{ cliente.name }}
        </option>
      </select>
      <select v-model="nuevaCita.pet_id" required>
        <option disabled value="">Selecciona una mascota</option>
        <option v-for="mascota in mascotasFiltradas" :key="mascota.id" :value="mascota.id">
          {{ mascota.name }}
        </option>
      </select>
      <select v-model="nuevaCita.service_id" required>
        <option disabled value="">Selecciona un servicio</option>
        <option v-for="servicio in servicios" :key="servicio.id" :value="servicio.id">
          {{ servicio.name }}
        </option>
      </select>
      <select v-model="nuevaCita.vet_id" required>
        <option disabled value="">Selecciona un veterinario</option>
        <option v-for="vet in veterinarios" :key="vet.id" :value="vet.id">
          {{ vet.username }}
        </option>
      </select>
      <input v-model="nuevaCita.date" type="date" required />
      <input v-model="nuevaCita.time" type="time" required />
      <label>
        <input type="checkbox" v-model="nuevaCita.drop_off" />
        El cliente dejará la mascota y la recogerá después
      </label>
      <button type="submit">Guardar</button>
    </form>

    <div v-if="loading" style="margin:1rem 0; color:#888;">Cargando datos...</div>
    <div v-if="errorMsg" style="color:red;">{{ errorMsg }}</div>
    <div class="table-scroll" v-if="!loading && !errorMsg">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Cliente</th>
            <th>Mascota</th>
            <th>Servicio</th>
            <th>Veterinario</th>
            <th>Fecha</th>
            <th>Hora</th>
            <th>Drop-off</th>
            <th>Código Recogida</th>
            <th>Validar Recogida</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cita in appointments" :key="cita.id">
            <td>{{ cita.id }}</td>
            <td>{{ getNombreCliente(cita.client_id) }}</td>
            <td>{{ getNombreMascota(cita.pet_id) }}</td>
            <td>{{ getNombreServicio(cita.service_id) }}</td>
            <td>{{ getNombreVeterinario(cita.vet_id) }}</td>
            <td>{{ formatearFecha(cita.date) }}</td>
            <td>{{ cita.time }}</td>
            <td>{{ cita.drop_off ? 'Sí' : 'No' }}</td>
            <td>
              <span v-if="cita.drop_off" style="font-weight:bold">{{ cita.pickup_code }}</span>
            </td>
            <td v-if="cita.drop_off">
              <template v-if="cita.collected">
                <span style="color: green; font-weight: bold;">Recogida</span>
              </template>
              <template v-else>
                <input
                  v-model="codigoIngresado[cita.id]"
                  placeholder="Código recogida"
                  style="width: 110px"
                />
                <button @click="verificarCodigo(cita)">Validar</button>
              </template>
            </td>
            <td v-else>-</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import api from '../axios'
import jsPDF from 'jspdf'

const appointments = ref([])
const showForm = ref(false)
const nuevaCita = ref({
  client_id: '',
  pet_id: '',
  service_id: '',
  vet_id: '',
  date: '',
  time: '',
  drop_off: false,
  pickup_code: ''
})
const codigoIngresado = ref({})

const clientes = ref([])
const mascotas = ref([])
const servicios = ref([])
const veterinarios = ref([])
const loading = ref(true)
const errorMsg = ref('')

onMounted(async () => {
  loading.value = true
  errorMsg.value = ''
  try {
    const [clientesRes, mascotasRes, serviciosRes, veterinariosRes, appointmentsRes] = await Promise.all([
      api.get('/clients'),
      api.get('/pets'),
      api.get('/services'),
      api.get('/users?role=veterinario'),
      api.get('/appointments')
    ])
    clientes.value = clientesRes.data
    mascotas.value = mascotasRes.data
    servicios.value = serviciosRes.data
    veterinarios.value = veterinariosRes.data
    appointments.value = appointmentsRes.data
  } catch (e) {
    errorMsg.value = 'No se pudieron cargar los datos. Verifica tu conexión o el servidor.'
  } finally {
    loading.value = false
  }
})

const mascotasFiltradas = computed(() =>
  mascotas.value.filter(m => m.client_id == nuevaCita.value.client_id)
)

function getNombreCliente(id) {
  const c = clientes.value.find(x => x.id == id)
  return c ? c.name : id
}
function getNombreMascota(id) {
  const m = mascotas.value.find(x => x.id == id)
  return m ? m.name : id
}
function getNombreServicio(id) {
  const s = servicios.value.find(x => x.id == id)
  return s ? s.name : id
}
function getNombreVeterinario(id) {
  const v = veterinarios.value.find(x => x.id == id)
  return v ? v.username : id
}

async function agendarCita() {
  try {
    if (nuevaCita.value.drop_off) {
      nuevaCita.value.pickup_code = generarCodigoRecogida()
    } else {
      nuevaCita.value.pickup_code = ''
    }
    const res = await api.post('/appointments', { ...nuevaCita.value })
    appointments.value.unshift(res.data.data)
    if (nuevaCita.value.drop_off) {
      imprimirComprobante(res.data.data)
    }
    nuevaCita.value = {
      client_id: '',
      pet_id: '',
      service_id: '',
      vet_id: '',
      date: '',
      time: '',
      drop_off: false,
      pickup_code: ''
    }
    showForm.value = false
  } catch (error) {
    alert('Error al agendar cita: ' + (error.response?.data?.msg || error.message))
  }
}

function generarCodigoRecogida() {
  return Math.random().toString(36).substring(2, 8).toUpperCase()
}

function imprimirComprobante(cita) {
  const mascota = getNombreMascota(cita.pet_id)
  const cliente = getNombreCliente(cita.client_id)
  const fecha = cita.date
  const hora = cita.time
  const codigo = cita.pickup_code

  const doc = new jsPDF()
  doc.setFontSize(16)
  doc.text('Comprobante de Recogida de Mascota', 10, 15)
  doc.setFontSize(12)
  doc.text(`Cliente: ${cliente}`, 10, 30)
  doc.text(`Mascota: ${mascota}`, 10, 40)
  doc.text(`Fecha de recogida: ${fecha}`, 10, 50)
  doc.text(`Hora de recogida: ${hora}`, 10, 60)
  doc.text(`Código de recogida: ${codigo}`, 10, 75)
  doc.text('Por favor, presente este código al recoger la mascota.', 10, 90)
  doc.save(`Recogida_${mascota}_${codigo}.pdf`)
}

async function verificarCodigo(cita) {
  const ingresado = (codigoIngresado.value[cita.id] || '').trim().toUpperCase()
  if (ingresado === cita.pickup_code) {
    try {
      await api.put(`/appointments/${cita.id}`, { collected: true })
      cita.collected = true
      alert('Código correcto. Mascota marcada como recogida.')
      codigoIngresado.value[cita.id] = ''
    } catch (error) {
      alert('Error al actualizar el estado de recogida.')
    }
  } else {
    alert('Código incorrecto. Verifique con el dueño.')
  }
}

watch(() => nuevaCita.value.client_id, () => {
  nuevaCita.value.pet_id = ''
})

function formatearFecha(fecha) {
  return fecha ? fecha.split('T')[0] : ''
}
</script>

<style scoped>
h1 {
  color: #1976d2;
  font-weight: 800;
  margin-bottom: 1.2rem;
  letter-spacing: 1px;
}

.form {
  margin: 1.5rem 0 2rem 0;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem 1.5rem;
  align-items: end;
  background: #f7fafd;
  border-radius: 10px;
  padding: 1.2rem 1.5rem;
  box-shadow: 0 1px 8px 0 rgba(33,150,243,0.04);
  max-width: 100%;
}

.form select,
.form input[type="date"],
.form input[type="time"] {
  border-radius: 6px;
  border: 1px solid #b0bec5;
  font-size: 1rem;
  padding: 0.4rem 0.8rem;
  background: #fff;
  min-width: 160px;
}

.form label {
  grid-column: span 2;
  font-size: 1rem;
  margin-left: 0.5rem;
  color: #333;
  align-items: center;
  display: flex;
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
  max-height: 340px;
  overflow-y: auto;
  margin-top: 2rem;
  border-radius: 10px;
  box-shadow: 0 1px 8px 0 rgba(33,150,243,0.04);
  background: #fff;
  padding: 0;       
}

table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  font-size: 1.07rem;
  margin: 0;
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
}

tbody tr:nth-child(even) {
  background: #f7fafd;
}
tbody tr:nth-child(odd) {
  background: #fff;
}

@media (max-width: 1100px) {
  .form {
    grid-template-columns: repeat(2, 1fr);
  }
  .form label, .form button {
    grid-column: span 2;
  }
}

@media (max-width: 700px) {
  .form {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    max-width: 99vw;
  }
  .form label, .form button {
    width: 100%;
    grid-column: auto;
  }
}

@media (max-width: 900px) {
  .form {
    flex-direction: column;
    gap: 0.5rem;
    max-width: 99vw;
  }
  table, th, td {
    font-size: 0.97rem;
  }
}
</style>