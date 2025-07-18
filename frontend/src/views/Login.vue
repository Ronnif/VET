<template>
  <div class="login-bg" :style="{ backgroundImage: `url(${fondoLogin})` }">
    <div class="login-overlay"></div>
    <div class="login-center">
      <div class="login-card">
        <div class="login-logo">
          <span class="logo-main">sunset</span><span class="logo-accent">VET</span>
        </div>
        <form @submit.prevent="login">
          <label class="login-label">Usuario</label>
          <input v-model="username" type="text" placeholder="Usuario" required />
          <label class="login-label">Contraseña</label>
          <input v-model="password" type="password" placeholder="Contraseña" required />
          <div class="login-actions">
            <button type="submit">INGRESAR</button>
          </div>
          <p v-if="error" class="error">{{ error }}</p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../axios'
import fondoLogin from '../assets/fondo6.png'
import { useToast } from 'vue-toastification'

const toast = useToast()
const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const login = async () => {
  error.value = ''
  try {
    const response = await api.post('/login', {
      username: username.value,
      password: password.value
    })
    const expiresAt = Date.now() + 30 * 60 * 1000 // 30 minutos
    localStorage.setItem('token', response.data.data.token)
    localStorage.setItem('expiresAt', expiresAt)
    localStorage.setItem('role', response.data.data.user.role)
    localStorage.setItem('user_id', response.data.data.user.id)
    localStorage.setItem('user_name', response.data.data.user.username)
    if (response.data.data.user.role === 'admin') {
      router.push('/role-selector')
    } else {
      router.push('/dashboard')
    }
  } catch (err) {
    toast.error(err.response?.data?.message || 'Usuario o contraseña incorrectos') // Mensaje moderno
  }
}
</script>

<style scoped>
:global(html, body) {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.login-bg {
  min-height: 100vh;
  height: 100vh;
  width: 100vw;
  position: relative;
  overflow: hidden;
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}
.login-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(120,0,120,0.55) 0%, rgba(66,185,131,0.35) 100%);
  z-index: 1;
}
.login-center {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}
.login-card {
  background: rgba(83, 84, 85, 0.10);
  border-radius: 18px;
  box-shadow: 0 8px 32px 0 rgba(60, 60, 60, 0.25);
  padding: 2.5rem 2.5rem 2rem 2.5rem;
  min-width: 400px;
  max-width: 98vw;
  width: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
  backdrop-filter: blur(8px);
  border: 1.5px solid rgba(255,255,255,0.18);
}
.login-logo {
  font-size: 2.8rem;
  font-weight: 700;
  margin-bottom: 2rem;
  letter-spacing: 1px;
  text-align: center;
}
.logo-main {
  color: #fff;
}
.logo-accent {
  color: #23acd6;
  margin-left: 0.3rem;
}
.login-label {
  color: #fff;
  font-size: 1.05rem;
  margin-bottom: 0.2rem;
  margin-top: 0.7rem;
  display: block;
  text-align: left;
}
input {
  display: block;
  width: 100%;
  margin: 0.3rem 0 1.1rem 0;
  padding: 0.8rem 1rem;
  font-size: 1.18rem;
  border-radius: 8px;
  border: 1.5px solid #bdbdbd;
  background: #f8f8f8;
  transition: border 0.2s;
}
input:focus {
  border: 1.5px solid #c2185b;
  outline: none;
  background: #fff;
}
.login-actions {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
  width: 100%;
  display: flex;
  justify-content: center;
}
button {
  width: 100%;
  padding: 0.9rem 0;
  font-size: 1.25rem;
  background: linear-gradient(90deg, #050c4d 60%, #330650 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  letter-spacing: 1px;
  box-shadow: 0 2px 8px 0 rgba(60, 60, 60, 0.08);
  transition: background 0.2s;
}
button:hover {
  background: linear-gradient(90deg, #0335ca 60%, #0594a4 100%);
}
.error {
  color: #ffb3b3;
  background: #3a1a1a;
  border-radius: 6px;
  padding: 0.7rem 0.5rem;
  margin-top: 1.2rem;
  font-size: 1rem;
  width: 100%;
  text-align: center;
}
@media (max-width: 600px) {
  .login-card {
    min-width: 90vw;
    padding: 1.5rem 0.7rem 1.2rem 0.7rem;
  }
  .login-logo {
    font-size: 1.5rem;
  }
}
</style>