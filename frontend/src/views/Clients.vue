<template>
  <div>
    <h1>Gestión de Clientes</h1>
    <button @click="showForm = !showForm">
      {{ showForm ? 'Cancelar' : 'Agregar Cliente' }}
    </button>
    <form v-if="showForm" @submit.prevent="agregarCliente">
      <input v-model="nuevoCliente.name" placeholder="Nombre" required />
      <input v-model="nuevoCliente.email" placeholder="Email" />
      <input v-model="nuevoCliente.phone" placeholder="Teléfono" />
      <input v-model="nuevoCliente.address" placeholder="Dirección" />
      <button type="submit">Guardar</button>
    </form>

    <!-- Tabla de clientes solo si NO hay cliente seleccionado -->
    <div class="table-scroll" v-if="!clienteActual">
      <table>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Email</th>
            <th>Teléfono</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cliente in clientes" :key="cliente.id">
            <td>{{ cliente.name }}</td>
            <td>{{ cliente.email }}</td>
            <td>{{ cliente.phone }}</td>
            <td>
              <button @click="irAMascotas(cliente.id)">Agregar Mascota</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Perfil del cliente seleccionado y mascotas -->
    <div v-if="clienteActual">
      <h2>Cliente Seleccionado</h2>
      <p><b>ID:</b> {{ clienteActual.id }}</p>
      <p><b>Nombre:</b> {{ clienteActual.name }}</p>
      <p><b>Email:</b> {{ clienteActual.email }}</p>
      <p><b>Teléfono:</b> {{ clienteActual.phone }}</p>
      <h3>Mascotas de este cliente</h3>
      <ul>
        <li v-for="mascota in mascotasCliente" :key="mascota.id">
          {{ mascota.name }} ({{ mascota.species }}, {{ mascota.breed }}, {{ mascota.age }} años)
        </li>
        <li v-if="mascotasCliente.length === 0">Sin mascotas registradas.</li>
      </ul>
      <button @click="clienteActual = null" style="margin-top: 10px;">Volver a clientes</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const showForm = ref(false)
const clientes = ref([])
const nuevoCliente = ref({ name: '', email: '', phone: '', address: '' })
const clienteActual = ref(null)
const mascotasCliente = ref([])

onMounted(async () => {
  await cargarClientes()
})

async function cargarClientes() {
  const res = await api.get('/clients')
  clientes.value = res.data
}

function seleccionarCliente(cliente) {
  clienteActual.value = cliente
  cargarMascotas()
}

async function cargarMascotas() {
  if (!clienteActual.value) return
  const res = await api.get(`/pets?client_id=${clienteActual.value.id}`)
  mascotasCliente.value = res.data
}

async function agregarCliente() {
  try {
    const token = localStorage.getItem('token')
    const res = await api.post('/clients', { ...nuevoCliente.value }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    clientes.value.unshift(res.data.data) // Agrega el nuevo cliente al inicio
    nuevoCliente.value = { name: '', email: '', phone: '', address: '' }
    showForm.value = false
  } catch (error) {
    alert('Error al agregar cliente: ' + (error.response?.data?.msg || error.message))
  }
}

function irAMascotas(clienteId) {
  router.push(`/dashboard/clients/${clienteId}/pets`)
}
</script>
<style scoped>
h1, h2, h3 {
  color: #1976d2;
  font-weight: 800;
  margin-bottom: 1.2rem;
  letter-spacing: 1px;
}

div {
  max-width: 1200px;
  margin: 2rem auto;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px 0 rgba(0,0,0,0.08);
  padding: 2rem 2.5rem 2.5rem 2.5rem;
  width: 95vw;
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

form input {
  border-radius: 6px;
  border: 1px solid #b0bec5;
  font-size: 1rem;
  padding: 0.4rem 0.8rem;
  background: #fff;
}

.table-scroll {
  max-height: 400px;
  overflow-y: auto;
  overflow-x: auto;
  margin-bottom: 2rem;
  border-radius: 10px 10px 0 0;
  box-shadow: 0 1px 8px 0 rgba(33,150,243,0.04);
  background: #fff;
  width: 100%;         /* <-- Asegura que ocupe todo el ancho del padre */
  padding: 0;          /* <-- Elimina padding extra */
}

table {
  width: 100%;         /* <-- Ocupa todo el ancho del contenedor */
  min-width: 800px;    /* <-- Evita que se comprima demasiado */
  border-collapse: collapse;
  background: #fff;
  font-size: 1.07rem;
  margin: 0;           /* <-- Elimina margen extra */
}

th {
  background: #1976d2 !important;
  color: #fff;
  font-weight: 700;
  border-bottom: 2px solid #b0bec5;
  position: sticky;
  top: 0;
  z-index: 2;
  box-shadow: 0 2px 6px -2px rgba(33,150,243,0.08);
  padding: 0.8rem 0.5rem;
  text-align: center;
}

td {
  padding: 0.8rem 0.5rem;
  text-align: center;
  word-break: break-word;
}

tbody tr:nth-child(even) {
  background: #f7fafd;
}
tbody tr:nth-child(odd) {
  background: #fff;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0 0 1rem 0;
}

ul li {
  padding: 0.4rem 0;
  border-bottom: 1px solid #e0e0e0;
}

ul li:last-child {
  border-bottom: none;
}

@media (max-width: 900px) {
  div {
    padding: 1rem 0.5rem;
    width: 99vw;
  }
  table, th, td {
    font-size: 0.97rem;
  }
  form {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>