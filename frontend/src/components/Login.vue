<template>
  <div>
    <div class="text-center mt-4 mb-2">
      <h1 class="app-title">Vechile Parking App V 2</h1>
    </div>
    <div class="d-flex flex-column justify-content-center align-items-center" style="min-height:80vh; padding:16px;">
      <div class="card login-card p-3" style="width:360px;">
        <h3 class="text-center mb-3 login-heading">Login</h3>

        <form @submit.prevent="login">
          <div class="mb-2">
            <label for="email" class="form-label">Email</label>
            <input id="email" v-model="email" type="email" class="form-control" required autocomplete="username" />
          </div>

          <div class="mb-2">
            <label for="password" class="form-label">Password</label>
            <input id="password" v-model="password" type="password" class="form-control" required autocomplete="current-password" />
          </div>

          <button type="submit" class="btn btn-primary w-100 mt-2 login-btn">Login</button>
        </form>

        <div class="text-center mt-3">
          <router-link to="/register" class="register-link">Create account</router-link>
        </div>

        <div v-if="error" class="alert alert-danger mt-3 mb-0 text-center py-1">
          {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const login = async () => {
  error.value = ''
  try {
    const res = await fetch('https://vehicle-parking-v2-5zb6.onrender.com/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value, password: password.value })
    })
    const data = await res.json()

    if (!res.ok) {
      // server sent message or simple fallback
      error.value = data.msg || 'Login failed'
      return
    }

    // save token and role
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('role', data.role)

    // simple redirect
    if (data.role === 'admin') router.push('/admin')
    else router.push('/user/dashboard')
  } catch (e) {
    error.value = 'Network error'
  }
}
</script>

<style scoped>
.app-title {
  color: #fff;
  background: linear-gradient(90deg, #007bff 0%, #00c6ff 100%);
  padding: 16px 0;
  border-radius: 12px;
  font-size: 2.2rem;
  font-weight: 700;
  letter-spacing: 2px;
  box-shadow: 0 2px 12px rgba(0,123,255,0.15);
}

.login-card {
  background: linear-gradient(135deg, #f8fafc 60%, #e3f0ff 100%);
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,123,255,0.12);
  border: none;
}

.login-heading {
  color: #007bff;
  font-weight: 700;
  letter-spacing: 1px;
}

.login-btn {
  background: linear-gradient(90deg, #007bff 0%, #00c6ff 100%);
  border: none;
  font-weight: 600;
  font-size: 1.1rem;
  transition: background 0.2s;
}

.login-btn:hover {
  background: linear-gradient(90deg, #0056b3 0%, #007bff 100%);
}

.register-link {
  color: #007bff;
  font-weight: 600;
  text-decoration: underline;
  transition: color 0.2s;
}

.register-link:hover {
  color: #0056b3;
}

.form-label {
  font-size: 1rem;
  color: #0056b3;
  font-weight: 500;
}

input.form-control {
  border-radius: 8px;
  border: 1px solid #b3d7ff;
  transition: border-color 0.2s;
}

input.form-control:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 2px #cce6ff;
}
</style>
