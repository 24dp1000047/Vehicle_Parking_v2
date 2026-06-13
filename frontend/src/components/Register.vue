<template>
  <div class="d-flex justify-content-center align-items-center" style="min-height:100vh; padding:20px;">
    <div class="card p-3" style="width:350px;">
      
      <h3 class="text-center mb-3">Sign Up</h3>

      <form @submit.prevent="registerUser">

        <div class="mb-2">
          <label class="form-label">Email</label>
          <input type="email" v-model="email" class="form-control" required />
        </div>

        <div class="mb-2">
          <label class="form-label">Password</label>
          <input type="password" v-model="password" class="form-control" required />
        </div>

        <div class="mb-2">
          <label class="form-label">Full Name</label>
          <input type="text" v-model="fullname" class="form-control" required />
        </div>

        <div class="mb-2">
          <label class="form-label">Address</label>
          <input type="text" v-model="address" class="form-control" required />
        </div>

        <div class="mb-2">
          <label class="form-label">Pin Code</label>
          <input type="text" v-model="pin_code" class="form-control" required />
        </div>

        <button type="submit" class="btn btn-primary w-100 mt-2">
          Register
        </button>
      </form>

      <div class="text-center mt-3">
        <router-link to="/">Already have an account?</router-link>
      </div>

      <div v-if="error" class="alert alert-danger mt-2 text-center py-1">
        {{ error }}
      </div>

      <div v-if="success" class="alert alert-success mt-2 text-center py-1">
        {{ success }}
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const fullname = ref('')
const address = ref('')
const pin_code = ref('')
const error = ref('')
const success = ref('')
const router = useRouter()

const registerUser = async () => {
  error.value = ''
  success.value = ''

  try {
    const res = await fetch(`${window.API_URL}/api/register`, {
      method: 'POST',
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: email.value,
        password: password.value,
        fullname: fullname.value,
        address: address.value,
        pin_code: pin_code.value
      })
    })

    const data = await res.json()

    if (!res.ok) {
      error.value = data.msg || 'Registration failed'
      return
    }

    success.value = 'Signup successful! Redirecting...'
    setTimeout(() => router.push('/'), 1200)

  } catch (e) {
    error.value = 'Network error'
  }
}
</script>

<style scoped>
.card {
  border-radius: 6px;
}
h3 {
  font-size: 1.3rem;
  margin: 0;
}
</style>
