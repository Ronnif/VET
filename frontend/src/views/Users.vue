<template>
  <div class="users-container">
    <div class="users-header">
      <h1>Gestión de Usuarios</h1>
      <button class="add-btn" @click="mostrarFormulario = !mostrarFormulario">
        <i class="fas" :class="mostrarFormulario ? 'fa-times' : 'fa-user-plus'"></i>
        {{ mostrarFormulario ? 'Cancelar' : 'Agregar Usuario' }}
      </button>
    </div>

    <form v-if="mostrarFormulario" class="user-form" @submit.prevent="agregarUsuario">
      <input v-model="nuevoUsuario.nombre" placeholder="Nombre" required />
      <input v-model="nuevoUsuario.email" placeholder="Email" required type="email" />
      <select v-model="nuevoUsuario.rol" required>
        <option disabled value="">Selecciona un rol</option>
        <option value="admin">Administrador</option>
        <option value="recepcionista">Recepcionista</option>
        <option value="veterinario">Veterinario</option>
      </select>
      <input v-model="nuevoUsuario.password" placeholder="Contraseña" required type="password" autocomplete="new-password" />
      <button class="save-btn" type="submit">
        <i class="fas fa-save"></i> Guardar
      </button>
    </form>

    <div class="table-card">
      <table>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Email</th>
            <th>Rol</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="usuario in usuarios" :key="usuario.id">
            <td>{{ usuario.username }}</td>
            <td>{{ usuario.email }}</td>
            <td>
              <span :class="['role-badge', usuario.role]">
                <i v-if="usuario.role === 'admin'" class="fas fa-crown"></i>
                <i v-else-if="usuario.role === 'recepcionista'" class="fas fa-user-tie"></i>
                <i v-else-if="usuario.role === 'veterinario'" class="fas fa-user-md"></i>
                {{ usuario.role ? (usuario.role.charAt(0).toUpperCase() + usuario.role.slice(1)) : 'Sin rol' }}
              </span>
            </td>
            <td>
              <button
                v-if="usuario.role !== 'admin'"
                class="delete-btn"
                @click="eliminarUsuario(usuario.id)"
              >
                <i class="fas fa-trash"></i> Eliminar
              </button>
              <span v-else class="not-allowed">No permitido</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../axios'
import { useToast } from 'vue-toastification' // <-- Importa el toast

const toast = useToast() // <-- Inicializa el toast

const mostrarFormulario = ref(false)
const usuarios = ref([])

const nuevoUsuario = ref({
  nombre: '',
  email: '',
  rol: '',
  password: ''
})

onMounted(async () => {
  const res = await api.get('/users')
  usuarios.value = res.data
})

async function agregarUsuario() {
  try {
    await api.post('/users', {
      username: nuevoUsuario.value.nombre,
      email: nuevoUsuario.value.email,
      role: nuevoUsuario.value.rol,
      password: nuevoUsuario.value.password
    })
    const res = await api.get('/users')
    usuarios.value = res.data
    nuevoUsuario.value = { nombre: '', email: '', rol: '', password: '' }
    mostrarFormulario.value = false
    toast.success('Usuario agregado correctamente') // Verde, éxito
  } catch (error) {
    toast.error('Error al crear usuario: ' + (error.response?.data?.msg || error.message))
  }
}

async function eliminarUsuario(id) {
  try {
    await api.delete(`/users/${id}`)
    const res = await api.get('/users')
    usuarios.value = res.data
    toast.error('Usuario eliminado correctamente') // Rojo/naranja, acción destructiva
  } catch (error) {
    toast.error('Error al eliminar usuario: ' + (error.response?.data?.msg || error.message))
  }
}
</script>

<style scoped>
.users-container {
  max-width: 1200px;      /* Antes: 900px */
  margin: 2.5rem auto;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px 0 rgba(0,0,0,0.07);
  padding: 3rem 3rem 3rem 3rem; /* Más espacio interno */
}
.users-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}
h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #222;
  margin: 0;
}
.add-btn {
  background: linear-gradient(135deg, #00bcd4 80%, #2196f3 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background 0.2s;
}
.add-btn:hover {
  background: linear-gradient(135deg, #2196f3 80%, #00bcd4 100%);
}
.user-form {
  background: #f7fafd;
  border-radius: 10px;
  padding: 2rem 1.5rem 1.5rem 1.5rem;
  margin-bottom: 1.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem 1.5rem;
  align-items: flex-end;
  justify-content: center;
}
.user-form input,
.user-form select {
  padding: 0.8rem 1rem;
  border-radius: 6px;
  border: 1px solid #b0bec5;
  font-size: 1.05rem;
  min-width: 220px;
  background: #fff;
  transition: border 0.2s;
}
.user-form input:focus,
.user-form select:focus {
  border: 1.5px solid #2196f3;
  outline: none;
}
.save-btn {
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.8rem 2rem;
  font-size: 1.08rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background 0.2s;
  margin-left: 1rem;
}
.save-btn:hover {
  background: #368a6e;
}
.table-card {
  background: #f7fafd;
  border-radius: 12px;
  box-shadow: 0 2px 8px 0 rgba(0,0,0,0.03);
  padding: 2rem 1.5rem;   /* Más padding */
  margin-top: 2rem;
}
table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: transparent;
}
th, td {
  padding: 1.1rem 0.8rem; /* Más espacio en celdas */
  text-align: center;
}
th {
  background: #e3f2fd;
  color: #1976d2;
  font-weight: 700;
  border-bottom: 2px solid #b0bec5;
}
tr:nth-child(even) td {
  background: #f0f7fa;
}
tr:nth-child(odd) td {
  background: #fff;
}
.role-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  border-radius: 6px;
  padding: 0.3rem 0.7rem;
  font-size: 0.98rem;
  font-weight: 600;
}
.role-badge.admin {
  background: #ffe082;
  color: #b28704;
}
.role-badge.recepcionista {
  background: #ffcccb;
  color: #b71c1c;
}
.role-badge.veterinario {
  background: #b2ebf2;
  color: #006064;
}
.delete-btn {
  background: #ff5252;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.4rem 1rem;
  font-size: 0.98rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  transition: background 0.2s;
}
.delete-btn:hover {
  background: #c62828;
}
.not-allowed {
  color: #888;
  font-size: 0.95rem;
}
.vue-toastification__toast--success {
  background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
  color: #222;
  font-weight: 600;
  border-radius: 24px; /* Más pill */
  box-shadow: 0 8px 24px rgba(67, 233, 123, 0.18);
  font-size: 1.08rem;
  padding: 1.2rem 2.2rem;
}

/* Personaliza el toast de error */
.vue-toastification__toast--error {
  background: linear-gradient(90deg, #ff5858 0%, #f09819 100%);
  color: #fff;
  font-weight: 600;
  border-radius: 10px;
}

/* Personaliza el toast de info */
.vue-toastification__toast--info {
  background: linear-gradient(90deg, #56ccf2 0%, #2f80ed 100%);
  color: #fff;
  font-weight: 600;
  border-radius: 10px;
}
</style>