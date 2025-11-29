<template>
  <div class="admin-bar d-flex justify-content-between align-items-center px-4 py-3 mb-4 shadow-sm">
    <div class="d-flex align-items-center">
      <strong class="brand-text me-4">Admin Panel</strong>
      <nav class="d-none d-md-flex gap-3">
        <router-link to="/admin" class="nav-link-custom" active-class="active-link">Dashboard</router-link>
        <router-link to="/admin/users" class="nav-link-custom" active-class="active-link">Users</router-link>
        <router-link to="/admin/search" class="nav-link-custom" active-class="active-link">Search</router-link>
        <router-link to="/admin/summary" class="nav-link-custom" active-class="active-link">Summary</router-link>
      </nav>
    </div>

    <div class="d-flex align-items-center gap-3">
      <router-link to="/admin/edit-profile" class="profile-link">
        <i class="bi bi-person-circle me-1"></i> Profile
      </router-link>
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
.admin-bar {
  background: #ffffff;
  border-radius: 12px;
  border-left: 5px solid #4361ee;
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
  color: #4361ee;
  background: #f8f9fa;
}

.active-link {
  color: #4361ee;
  background: #eef2ff;
  font-weight: 600;
}

.profile-link {
  text-decoration: none;
  color: #4361ee;
  font-weight: 500;
  font-size: 0.95rem;
}

.logout-btn {
  border-radius: 6px;
  font-weight: 500;
}
</style>
