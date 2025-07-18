<template>
  <div class="main-card">
    <h2>Gestión de Clientes</h2>
    <!-- ...botón agregar cliente... -->
    <button @click="router.push('/dashboard/clients')" style="margin-bottom:1rem">← Volver a clientes</button>

    <!-- Cliente Seleccionado -->
    <div>
      <!-- ...datos del cliente... -->
    </div>

    <!-- Agregar Mascota -->
    <h3>Agregar Mascota</h3>
    <form @submit.prevent="agregarMascota" class="form">
      <input v-model="nuevaMascota.name" placeholder="Nombre" required />
      <input v-model="nuevaMascota.species" placeholder="Especie" required />
      <input v-model="nuevaMascota.breed" placeholder="Raza" required />
      <input v-model.number="nuevaMascota.age" type="number" min="0" placeholder="Edad" required />
      <button type="submit">Guardar</button>
    </form>
    <div v-if="mensaje" style="color: green">{{ mensaje }}</div>
    <div class="table-scroll">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Especie</th>
            <th>Raza</th>
            <th>Edad</th>
            <th>ID Cliente</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pet in pets" :key="pet.id">
            <td>{{ pet.id }}</td>
            <td>{{ pet.name }}</td>
            <td>{{ pet.species }}</td>
            <td>{{ pet.breed }}</td>
            <td>{{ pet.age }}</td>
            <td>{{ pet.client_id }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '../axios'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

const toast = useToast()
const router = useRouter()

const props = defineProps({
  clienteId: { type: [String, Number], default: null }
})

const pets = ref([])
const nuevaMascota = ref({
  name: '',
  species: '',
  breed: '',
  age: '',
  client_id: Number(props.clienteId) || ''
})
const mensaje = ref('')
// Función para cargar solo las mascotas del cliente seleccionado
async function cargarMascotasCliente() {
  if (!props.clienteId) {
    pets.value = []
    return
  }
  const res = await api.get(`/pets?client_id=${props.clienteId}`)
  pets.value = res.data
}
// Actualiza client_id si cambia el prop y recarga mascotas
watch(() => props.clienteId, (nuevo) => {
  nuevaMascota.value.client_id = Number(nuevo) || ''
  cargarMascotasCliente()
})
// Carga mascotas al montar el componente
onMounted(() => {
  cargarMascotasCliente()
})

async function agregarMascota() {
  if (!nuevaMascota.value.client_id) {
    toast.error('Selecciona un cliente válido');
    return;
  }
  try {
    const res = await api.post('/pets', { ...nuevaMascota.value })
    toast.success('Mascota agregada correctamente')
    nuevaMascota.value = { name: '', species: '', breed: '', age: '', client_id: Number(props.clienteId) || '' }
    cargarMascotasCliente()
    // emit('mascota-agregada')
  } catch (error) {
    toast.error('Error al agregar mascota: ' + (error.response?.data?.msg || error.message))
  }
}
</script>

<style scoped>
h2 {
  color: #1976d2;
  font-weight: 800;
  margin-bottom: 1.2rem;
  letter-spacing: 1px;
}

.form {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
  align-items: center;
  background: #f7fafd;
  border-radius: 10px;
  padding: 1rem 1.5rem;
}

.form input {
  border-radius: 6px;
  border: 1px solid #b0bec5;
  font-size: 1rem;
  padding: 0.4rem 0.8rem;
  background: #fff;
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
  max-height: 260px;
  overflow-y: auto;
  margin-bottom: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 1px 8px 0 rgba(33,150,243,0.04);
  background: #fff;
}

table {
  width: 100%;
  min-width: 600px;
  border-collapse: collapse;
  background: #fff;
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

.main-card {
  max-width: 1100px;
  margin: 2rem auto;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px 0 rgba(0,0,0,0.08);
  padding: 2rem 2.5rem 2.5rem 2.5rem;
  width: 95vw;
}
.cliente-card {
  width: 100%;
  margin: 0 auto 2rem auto;
  background: transparent;
  border-radius: 0;
  box-shadow: none;
  padding: 0;
}

@media (max-width: 900px) {
  .form {
    flex-direction: column;
    gap: 0.5rem;
  }
  .table-scroll {
    max-width: 100vw;
    overflow-x: auto;
  }
  table, th, td {
    font-size: 0.97rem;
    min-width: 600px;
  }
}
</style>