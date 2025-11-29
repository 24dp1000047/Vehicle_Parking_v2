<template>
  <div class="members-page pt-3">
    <AdminNavbar />

    <!-- header -->
    <header class="mb-4 text-center">
      <h3 class="section-title">Members Registry</h3>
      <p class="text-muted">List of registered users and their current bookings</p>
    </header>

    <!-- states -->
    <div v-if="error" class="alert alert-danger text-center shadow-sm">{{ error }}</div>
    <div v-else-if="loading" class="text-center py-5 text-muted">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <div class="mt-2">Fetching users...</div>
    </div>

    <!-- content -->
    <div v-else>
      <div v-if="users.length === 0" class="empty-note text-center py-4 text-muted">No registered users found.</div>

      <div class="row g-4">
        <div class="col-md-6 col-lg-4" v-for="u in users" :key="u.id">
          <article class="card member-card h-100 border-0 shadow-sm">
            <div class="card-body d-flex flex-column">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <h5 class="card-title fw-bold text-primary mb-0">{{ u.fullname }}</h5>
                <span class="badge bg-light text-dark border">ID: {{ u.id }}</span>
              </div>

              <div class="small text-muted mb-3">
                <div class="mb-1"><i class="bi bi-envelope me-2"></i>{{ u.email }}</div>
                <div class="mb-1"><i class="bi bi-geo-alt me-2"></i>{{ u.address || '-' }}</div>
                <div><i class="bi bi-pin-map me-2"></i>{{ u.pin_code || '-' }}</div>
              </div>

              <div class="mt-auto">
                <div class="d-flex gap-2 mb-3">
                  <router-link :to="`/admin/user/${u.id}`" class="btn btn-sm btn-outline-primary flex-grow-1">
                    View Details
                  </router-link>
                  <button class="btn btn-sm btn-outline-danger flex-grow-1" @click="confirmDeleteUser(u.id)">
                    Remove
                  </button>
                </div>

                <div class="reservations border-top pt-3">
                  <h6 class="fw-bold small text-uppercase text-muted mb-2">Active Reservations</h6>
                  
                  <div v-if="!u.active_reservations || u.active_reservations.length === 0" class="small text-muted fst-italic">
                    No active bookings
                  </div>

                  <ul v-else class="list-unstyled mb-0">
                    <li v-for="r in u.active_reservations" :key="r.id" class="res-item p-2 mb-2 rounded bg-light border">
                      <div class="d-flex justify-content-between small mb-1">
                        <span class="fw-bold">{{ r.lot_name || 'Lot #' + r.lot_id }}</span>
                        <span class="badge bg-success">{{ r.status }}</span>
                      </div>
                      <div class="d-flex justify-content-between small text-muted">
                        <span>Spot: {{ r.spot_number }}</span>
                        <span>{{ r.vehicle_number }}</span>
                      </div>
                      <div class="small text-muted mt-1">
                        <i class="bi bi-clock me-1"></i> {{ formatDate(r.start_time) }}
                      </div>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </article>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AdminNavbar from './AdminNavbar.vue'

const router = useRouter()
const users = ref([])
const loading = ref(true)
const error = ref('')

// format date safely, show in Asia/Kolkata
function formatDate(val) {
  if (!val) return '-'
  try {
    let s = val
    // normalize common patterns to ISO
    if (typeof s === 'string') {
      // if "YYYY-MM-DD HH:MM:SS" convert to "YYYY-MM-DDTHH:MM:SS"
      if (/^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}/.test(s)) {
        s = s.replace(/\s+/, 'T')
      } else if (/^\d{4}-\d{2}-\d{2}$/.test(s)) {
        s = s + 'T00:00:00'
      }
      // if still missing timezone, assume UTC then display in IST
      if (!/Z$/.test(s) && !/[+-]\d{2}:\d{2}$/.test(s)) {
        s = s + 'Z'
      }
    }
    const d = new Date(s)
    if (isNaN(d.getTime())) return '-'
    return d.toLocaleString(undefined, { timeZone: 'Asia/Kolkata', hour12: true })
  } catch {
    return '-'
  }
}

// fetch users and for each user fetch active reservations
const fetchUsers = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await fetch('/api/admin/users', {
      headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
    })
    const data = await res.json()
    if (!res.ok) {
      error.value = data.msg || 'Failed to load users'
      loading.value = false
      return
    }

    // parallel fetch of each user's active reservations
    const enriched = await Promise.all(data.map(async (u) => {
      try {
        const rres = await fetch(`/api/admin/user/${u.id}/active-reservations`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
        })
        if (rres.ok) {
          const rv = await rres.json()
          return { ...u, active_reservations: rv }
        } else {
          return { ...u, active_reservations: [] }
        }
      } catch {
        return { ...u, active_reservations: [] }
      }
    }))

    users.value = enriched
  } catch (e) {
    error.value = 'Network error while fetching users'
  } finally {
    loading.value = false
  }
}

// optional: confirm + delete user (if API exists)
const confirmDeleteUser = async (userId) => {
  if (!confirm('Delete this user permanently?')) return
  try {
    const res = await fetch(`/api/admin/users/${userId}`, {
      method: 'DELETE',
      headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
    })
    const payload = await res.json()
    if (!res.ok) {
      alert(payload.msg || 'Delete failed')
    } else {
      // remove from local list for instant UI feedback
      users.value = users.value.filter(u => u.id !== userId)
    }
  } catch {
    alert('Network error during delete')
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
.members-page { 
  max-width: 1200px; 
  margin: 0 auto; 
  padding-left: 15px;
  padding-right: 15px;
}

.section-title {
  color: #2b2d42;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.member-card {
  border-radius: 12px;
  background: #fff;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.member-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.08) !important;
}

.res-item {
  font-size: 0.9rem;
}
</style>
