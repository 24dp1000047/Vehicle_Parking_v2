<template>
  <div class="user-bar d-flex justify-content-between align-items-center px-4 py-3 mb-4 shadow-sm">
    <div class="d-flex align-items-center">
      <strong class="brand-text me-4">Parking System</strong>
      <nav class="d-none d-md-flex gap-3">
        <router-link to="/user/dashboard" class="nav-link-custom" active-class="active-link">Dashboard</router-link>
        <router-link to="/user/summary" class="nav-link-custom" active-class="active-link">My Summary</router-link>
      </nav>
    </div>

    <div class="d-flex align-items-center gap-3">
      <div class="user-info d-none d-sm-block text-muted small">
        <i class="bi bi-person-fill me-1"></i> User
      </div>
      <button @click="logout" class="btn btn-sm btn-outline-danger logout-btn">
        <i class="bi bi-box-arrow-right me-1"></i> Logout
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const logout = () => {
  localStorage.clear()
  router.push('/')
}
</script>

<style scoped>
.user-bar {
  background: #ffffff;
  border-radius: 12px;
  border-left: 5px solid #2ec4b6;
}

.brand-text {
  font-size: 1.25rem;
  color: #2b2d42;
  font-weight: 700;
}

.nav-link-custom {
  text-decoration: none;
  color: #6c757d;
  font-weight: 500;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.nav-link-custom:hover {
  color: #2ec4b6;
  background: #f0fdfa;
}

.active-link {
  color: #2ec4b6;
  background: #e6fffa;
  font-weight: 600;
}

.logout-btn {
  border-radius: 6px;
  font-weight: 500;
}
</style>
