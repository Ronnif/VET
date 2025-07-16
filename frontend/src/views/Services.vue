<template>
  <div class="services-container">
    <h2>Servicios</h2>

    <div class="add-service-title">Agregar Servicio</div>
    <form class="service-form" @submit.prevent="addService">
      <input v-model="newService.name" placeholder="Nombre" required />
      <input v-model="newService.description" placeholder="Descripción" />
      <input v-model.number="newService.price" placeholder="Precio" type="number" required />
      <select v-model="newService.attention_type" required>
        <option disabled value="">Tipo de atención</option>
        <option value="servicios medicos">servicios medicos</option>
        <option value="servicios de estetica">servicios de estetica</option>
      </select>
      <button type="submit" class="save-btn">Agregar</button>
    </form>

    <div class="table-card">
      <table class="services-table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Precio</th>
            <th>Tipo de atención</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in services" :key="service.id">
            <td v-if="editId !== service.id">{{ service.name }}</td>
            <td v-else><input v-model="editService.name" /></td>
            <td v-if="editId !== service.id">{{ service.description }}</td>
            <td v-else><input v-model="editService.description" /></td>
            <td v-if="editId !== service.id">{{ service.price }}</td>
            <td v-else><input v-model.number="editService.price" type="number" /></td>
            <td v-if="editId !== service.id">{{ service.attention_type }}</td>
            <td v-else>
              <select v-model="editService.attention_type">
                <option value="servicios medicos">servicios medicos</option>
                <option value="servicios de estetica">servicios de estetica</option>
              </select>
            </td>
            <td>
              <button v-if="editId !== service.id" class="edit-btn" @click="startEdit(service)">Editar</button>
              <button v-if="editId === service.id" class="save-btn" @click="saveEdit(service.id)">Guardar</button>
              <button v-if="editId === service.id" class="cancel-btn" @click="cancelEdit">Cancelar</button>
              <button class="delete-btn" @click="deleteService(service.id)">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      services: [],
      newService: {
        name: '',
        description: '',
        price: null,
        attention_type: ''
      },
      editId: null,
      editService: {
        name: '',
        description: '',
        price: null,
        attention_type: ''
      }
    }
  },
  mounted() {
    this.fetchServices()
  },
  methods: {
    async fetchServices() {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.get('/api/services', {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.services = res.data
      } catch (error) {
        console.error('Error al obtener servicios:', error)
      }
    },
    async addService() {
      if (
        !this.newService.name ||
        this.newService.price === null ||
        this.newService.price === '' ||
        !this.newService.attention_type
      ) {
        alert('Todos los campos son obligatorios');
        return;
      }
      try {
        const token = localStorage.getItem('token')
        await axios.post('/api/services', this.newService, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.newService = { name: '', description: '', price: null, attention_type: '' }
        this.fetchServices()
      } catch (error) {
        alert('Error al agregar servicio: ' + (error.response?.data?.message || JSON.stringify(error.response?.data) || error.message))
        console.error(error)
      }
    },
    startEdit(service) {
      this.editId = service.id
      this.editService = { ...service }
    },
    cancelEdit() {
      this.editId = null
      this.editService = { name: '', description: '', price: null, attention_type: '' }
    },
    async saveEdit(id) {
      try {
        const token = localStorage.getItem('token')
        await axios.put(`/api/services/${id}`, this.editService, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.editId = null
        this.editService = { name: '', description: '', price: null, attention_type: '' }
        this.fetchServices()
      } catch (error) {
        alert('Error al editar servicio: ' + (error.response?.data?.message || JSON.stringify(error.response?.data) || error.message))
        console.error(error)
      }
    },
    async deleteService(id) {
      if (!confirm('¿Seguro que deseas eliminar este servicio?')) return
      try {
        const token = localStorage.getItem('token')
        await axios.delete(`/api/services/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.fetchServices()
      } catch (error) {
        const msg = error.response?.data?.message || ''
        if (msg.includes('asociado a citas')) {
          alert('No se puede eliminar el servicio porque está asociado a citas existentes. Solo puedes editarlo.')
        } else {
          alert('Error al eliminar servicio: ' + (msg || JSON.stringify(error.response?.data) || error.message))
        }
        console.error(error)
      }
    }
  }
}
</script>

<style scoped>
.services-container {
  max-width: 1200px;
  margin: 1.5rem auto 2rem auto;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px 0 rgba(0,0,0,0.07);
  padding: 1.5rem 2rem 2rem 2rem;
}

h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #222;
  margin-bottom: 1.5rem;
}

.table-card {
  background: #f7fafd;
  border-radius: 0 0 12px 12px; /* Solo abajo */
  box-shadow: 0 2px 8px 0 rgba(0,0,0,0.03);
  padding: 0 0.2rem 1.5rem 0.2rem; /* Quita padding-top */
  margin-bottom: 2rem;
  width: 100%;
  max-height: 420px;
  overflow-y: auto;
  overflow-x: auto;
  position: relative;
}

.services-table {
  width: 100%;
  border-collapse: collapse; /* Importante para sticky header */
  background: transparent;
  table-layout: fixed;
}

.services-table thead tr {
  background: none !important;
}

.services-table th, .services-table td {
  padding: 0.8rem 0.5rem;
  text-align: center;
  word-break: break-word;
  border-bottom: 1px solid #e3f2fd;
  font-size: 1.05rem;
  vertical-align: middle;
}

/* SOLO el header tiene el borde inferior oscuro y más grueso */
.services-table th {
  background: #e3f2fd !important;
  color: #1976d2;
  font-weight: 700;
  border-bottom: 3px solid #b0bec5 !important;
  position: sticky;
  top: 0;
  z-index: 999;
  padding-top: 0.3rem;
  padding-bottom: 1rem;
  box-shadow: none;
}

/* Quita el borde superior de la primera fila de datos */
.services-table tbody tr:first-child td {
  border-top: none !important;
  border-bottom: none !important;
}

.services-table td:last-child {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  justify-content: center;
  align-items: center;
  max-width: 180px;
  word-break: break-word;
}

.action-btn, .edit-btn, .save-btn, .cancel-btn, .delete-btn {
  border: none;
  border-radius: 6px;
  padding: 0.3rem 0.8rem;
  font-size: 0.98rem;
  font-weight: 600;
  cursor: pointer;
  margin: 0.1rem 0.1rem;
  transition: background 0.2s, box-shadow 0.2s;
  white-space: nowrap;
  box-shadow: 0 1px 4px 0 rgba(33,150,243,0.08);
}

.edit-btn, .save-btn {
  background: #42b983;
  color: #fff;
}
.edit-btn:hover, .save-btn:hover {
  background: #368a6e;
}
.cancel-btn {
  background: #b0bec5;
  color: #222;
}
.cancel-btn:hover {
  background: #78909c;
  color: #fff;
}
.delete-btn {
  background: #ff5252;
  color: #fff;
}
.delete-btn:hover {
  background: #c62828;
}

.add-service-title {
  margin-top: 2rem;
  font-size: 1.3rem;
  font-weight: 700;
  color: #1976d2;
}

.service-form {
  background: #f7fafd;
  border-radius: 10px;
  padding: 1.5rem 1rem;
  margin-bottom: 1.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem 1.5rem;
  align-items: flex-end;
  justify-content: center;
}

.service-form input,
.service-form select {
  padding: 0.8rem 1rem;
  border-radius: 6px;
  border: 1px solid #b0bec5;
  font-size: 1.05rem;
  min-width: 180px;
  background: #fff;
  transition: border 0.2s;
}

.service-form input:focus,
.service-form select:focus {
  border: 1.5px solid #2196f3;
  outline: none;
}

@media (max-width: 900px) {
  .services-container {
    padding: 1rem 0.5rem;
  }
  .table-card {
    padding: 0.5rem 0.2rem;
  }
  .services-table th, .services-table td {
    font-size: 0.95rem;
    padding: 0.5rem 0.2rem;
  }
}

@media (max-width: 700px) {
  .services-container {
    padding: 1rem 0.2rem;
  }
  .service-form {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  .table-card {
    padding: 0.2rem 0.1rem;
  }
  .services-table th, .services-table td {
    font-size: 0.92rem;
    padding: 0.4rem 0.1rem;
  }
}
</style>