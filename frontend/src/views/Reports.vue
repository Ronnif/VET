<!-- filepath: frontend/src/views/Reports.vue -->
<template>
  <div class="reports-container">
    <h2>Reportes de Pagos</h2>
    <p class="reporte-total">Total pagado: {{ report.total_pagado }}</p>

    <!-- Filtros -->
    <div class="filtros-bar">
      <label>Desde: <input type="date" v-model="filtros.start_date"></label>
      <label>Hasta: <input type="date" v-model="filtros.end_date"></label>
      <button @click="fetchReport">Filtrar</button>
      <button @click="limpiarFiltros">Limpiar</button>
    </div>
    <div class="table-scroll">
      <table class="reports-table">
        <thead>
          <tr>
            <th>Cliente</th>
            <th>Mascota</th>
            <th>Servicio</th>
            <th>Monto</th>
            <th>Método</th>
            <th>Fecha</th>
            <th>Hora</th> <!-- Nueva columna -->
          </tr>
        </thead>
        <tbody>
          <tr v-for="pago in report.pagos" :key="pago.id">
            <td>{{ pago.client?.name || pago.client_id }}</td>
            <td>{{ pago.pet?.name || pago.pet_id }}</td>
            <td>{{ pago.service?.name || pago.service_id }}</td>
            <td>{{ pago.payment_amount }}</td>
            <td>{{ pago.payment_method }}</td>
            <td>{{ formatFecha(pago.payment_date) }}</td>
            <td>{{ formatHora(pago.payment_date) }}</td>
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
      report: { total_pagado: 0, pagos: [] },
      filtros: {
        start_date: '',
        end_date: ''
      }
    }
  },
  mounted() {
    this.fetchReport()
  },
  methods: {
    async fetchReport() {
      const token = localStorage.getItem('token')
      const res = await axios.get('/api/reports/payments', {
        headers: { Authorization: `Bearer ${token}` },
        params: {
          start_date: this.filtros.start_date,
          end_date: this.filtros.end_date
        }
      })
      // Ordena los pagos por fecha descendente
      res.data.pagos.sort((a, b) => new Date(b.payment_date) - new Date(a.payment_date))
      this.report = res.data
    },
    limpiarFiltros() {
      this.filtros.start_date = ''
      this.filtros.end_date = ''
      this.fetchReport()
    },
    formatFecha(datetime) {
      // Devuelve solo la fecha en formato YYYY-MM-DD
      return datetime ? datetime.split('T')[0] : '';
    },
    formatHora(datetime) {
      // Devuelve solo la hora en formato HH:mm:ss
      return datetime ? datetime.split('T')[1]?.slice(0, 8) : '';
    }
  }
}
</script>

<style scoped>
.reports-container {
  max-width: 1200px;
  margin: 2rem auto;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px 0 rgba(0,0,0,0.08);
  padding: 1.2rem;
  display: flex;
  flex-direction: column;
  width: 90vw;
}

h2 {
  font-size: 2.2rem;
  font-weight: 800;
  color: #1976d2;
  margin-bottom: 0.5rem;
  letter-spacing: 1px;
}

.reporte-total {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2196f3;
  background: #e3f2fd;
  display: inline-block;
  padding: 0.5rem 1.2rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.filtros-bar {
  margin-bottom: 2rem;
  display: flex;
  gap: 1.2rem;
  align-items: center;
  flex-wrap: wrap;
  background: #f7fafd;
  border-radius: 8px;
  padding: 1rem 1.5rem;
  box-shadow: 0 1px 4px 0 rgba(33,150,243,0.04);
}

.filtros-bar label {
  font-weight: 600;
  color: #1976d2;
  font-size: 1.05rem;
}

.filtros-bar input[type="date"] {
  padding: 0.5rem 0.9rem;
  border-radius: 6px;
  border: 1px solid #b0bec5;
  font-size: 1rem;
  background: #fff;
  margin-left: 0.3rem;
}

.filtros-bar button {
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.5rem 1.5rem;
  font-size: 1.05rem;
  font-weight: 700;
  cursor: pointer;
  margin-left: 0.5rem;
  transition: background 0.2s;
  box-shadow: 0 1px 4px 0 rgba(33,150,243,0.04);
}
.filtros-bar button:last-child {
  background: #b0bec5;
  color: #222;
}
.filtros-bar button:hover {
  background: #368a6e;
}
.filtros-bar button:last-child:hover {
  background: #78909c;
  color: #fff;
}

.table-scroll {
  max-height: 340px; /* o el valor que prefieras */
  overflow-y: auto;
  margin-top: 1rem;
  border-radius: 10px 10px 0 0;
  box-shadow: 0 1px 8px 0 rgba(33,150,243,0.04);
  padding-bottom: 0;
  display: block;
}

.reports-table {
  width: 100%;
  table-layout: fixed; /* <-- Esto es clave para que la tabla no crezca fuera del contenedor */
  border-collapse: separate;
  border-spacing: 0;
  background: transparent;
  font-size: 1.07rem;
}

.reports-table th, .reports-table td {
  padding: 0.6rem 0.4rem;
  text-align: center;
  word-break: break-word;
}

.reports-table th {
  background: #1976d2;
  color: #fff;
  font-weight: 700;
  border-bottom: 2px solid #b0bec5;
  font-size: 1.08rem;
  position: sticky;
  top: 0;
  z-index: 2;
}

.reports-table tbody tr:nth-child(even) {
  background: #f7fafd;
}
.reports-table tbody tr:nth-child(odd) {
  background: #fff;
}

.reports-table tbody tr:hover {
  background: #e3f2fd;
  transition: background 0.2s;
}
</style>