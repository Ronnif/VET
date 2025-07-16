<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'info' // info, success, warning, error
  },
  message: {
    type: String,
    required: true
  }
})

const alertClass = computed(() => {
  switch (props.type) {
    case 'success': return 'alert-success'
    case 'warning': return 'alert-warning'
    case 'error': return 'alert-error'
    default: return 'alert-info'
  }
})
</script>

<template>
  <div :class="['alert', alertClass]">
    {{ message }}
  </div>
</template>

<style scoped>
.alert {
  padding: 1rem;
  border-radius: 6px;
  margin: 1rem 0;
  font-weight: 500;
}
.alert-info {
  background: #e3f2fd;
  color: #1565c0;
}
.alert-success {
  background: #e8f5e9;
  color: #2e7d32;
}
.alert-warning {
  background: #fffde7;
  color: #f9a825;
}
.alert-error {
  background: #ffebee;
  color: #c62828;
}
</style>
