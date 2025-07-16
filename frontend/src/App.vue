<template>
  <div :id="'app'" :class="{ 'login-fullscreen': $route.path === '/login' }">
    <router-view />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const isAuthenticated = computed(() => !!localStorage.getItem('token'))
</script>

<style scoped>
nav {
  margin-bottom: 2rem;
}
router-link {
  margin: 0 1rem;
  text-decoration: none;
  color: #42b983;
}
router-link.active {
  font-weight: bold;
}
</style>