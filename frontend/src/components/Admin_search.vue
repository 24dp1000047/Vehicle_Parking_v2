<template>
  <div class="admin-search-page pt-3">
    <AdminNavbar />

    <!-- header (reworked) -->
    <header class="mb-4 text-center">
      <h3 class="section-title">Admin Console</h3>
      <p class="text-muted">Search and manage parking lots and users</p>
    </header>

    <!-- search controls -->
    <div class="search-controls d-flex justify-content-center align-items-center gap-2 mb-4 p-3 bg-light rounded shadow-sm">
      <label class="me-2 fw-bold text-primary">Filter By:</label>

      <select v-model="filterBy" class="form-select w-auto border-primary">
        <option value="location">Lot - Location</option>
        <option value="spot_status">Spot Status (A/O)</option>
        <option value="user">User (name / email)</option>
      </select>

      <input
        v-model="query"
        @keyup.enter="performSearch"
        :placeholder="hintText"
        class="form-control w-50 border-primary"
        type="text"
        aria-label="search input"
      />

      <button class="btn btn-primary" @click="performSearch">
        <i class="bi bi-search me-1"></i> Find
      </button>
    </div>

    <!-- dynamic hint -->
    <p v-if="query" class="text-center mb-4 hint-line text-muted">
      <span v-if="filterBy === 'location'">Searching parking lots near: <strong>{{ query }}</strong></span>
      <span v-else-if="filterBy === 'spot_status'">Looking for spots with status: <strong>{{ query }}</strong></span>
      <span v-else-if="filterBy === 'user'">Looking up user: <strong>{{ query }}</strong></span>
    </p>

    <!-- status messages -->
    <div v-if="error" class="alert alert-danger text-center shadow-sm">{{ error }}</div>
    <div v-if="loading" class="text-center py-4 text-muted">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <div class="mt-2">Fetching results...</div>
    </div>

    <!-- lots grid -->
    <div v-if="(filterBy === 'location' || filterBy === 'spot_status') && lotsList.length" class="row g-4">
      <div v-for="lot in lotsList" :key="lot.id" class="col-lg-6 mb-4">
        <article class="lot-panel card h-100 border-0 shadow-sm">
          <div class="card-body d-flex flex-column">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <div>
                <h5 class="lot-title fw-bold text-primary mb-1">{{ lot.prime_location_name }}</h5>
                <div class="meta small text-muted">
                  <i class="bi bi-geo-alt-fill me-1"></i>{{ lot.address }} • PIN {{ lot.pin_code }} • ₹{{ lot.price }}/hr
                </div>
              </div>
              <div class="actions d-flex gap-1">
                <router-link :to="`/admin/edit-lot/${lot.id}`" class="btn btn-sm btn-outline-warning">
                  <i class="bi bi-pencil"></i>
                </router-link>
                <button class="btn btn-sm btn-outline-danger" @click="removeLot(lot.id)">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>

            <div class="mb-3">
              <div class="d-flex justify-content-between small text-muted mb-1">
                <span>Occupancy</span>
                <span>{{ lot.occupied_spots }} / {{ lot.maximum_number_of_spots }}</span>
              </div>
              <div class="progress" style="height: 6px;">
                <div 
                  class="progress-bar" 
                  role="progressbar" 
                  :style="{ width: (lot.occupied_spots / lot.maximum_number_of_spots * 100) + '%', backgroundColor: getProgressColor(lot.occupied_spots, lot.maximum_number_of_spots) }"
                  :aria-valuenow="lot.occupied_spots" 
                  aria-valuemin="0" 
                  :aria-valuemax="lot.maximum_number_of_spots">
                </div>
              </div>
            </div>

            <div class="spots-wrap mt-auto">
              <div
                v-for="spot in lot.spots"
                :key="spot.id"
                class="spot-indicator"
                :class="spot.status === 'O' ? 'occupied' : 'available'"
                :title="`Spot ${spot.spot_number}`"
                @click="spot.status === 'O' && openOccupied(spot.id)"
              >
                {{ spot.status }}
              </div>
            </div>
          </div>
        </article>
      </div>
    </div>

    <!-- users table -->
    <div v-if="filterBy === 'user' && usersList.length" class="row">
      <div class="col-12">
        <div class="card border-0 shadow-sm">
          <div class="card-body p-0">
            <div class="table-responsive">
              <table class="table table-hover align-middle text-center mb-0">
                <thead class="table-light">
                  <tr>
                    <th class="py-3">ID</th>
                    <th class="py-3">Name</th>
                    <th class="py-3">Email</th>
                    <th class="py-3">Address</th>
                    <th class="py-3">PIN</th>
                    <th class="py-3">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="u in usersList" :key="u.id">
                    <td>{{ u.id }}</td>
                    <td class="fw-bold text-primary">{{ u.fullname }}</td>
                    <td>{{ u.email }}</td>
                    <td>{{ u.address || '-' }}</td>
                    <td>{{ u.pin_code || '-' }}</td>
                    <td>
                      <router-link :to="`/admin/user/${u.id}`" class="btn btn-sm btn-outline-primary">
                        View
                      </router-link>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- no results -->
    <div v-else-if="searched && !loading && !error && ((filterBy === 'user' && !usersList.length) || (filterBy !== 'user' && !lotsList.length))" class="text-center text-muted py-5">
      <i class="bi bi-search display-4 mb-3 d-block text-secondary"></i>
      <p class="lead">No matching records found.</p>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import AdminNavbar from './AdminNavbar.vue'

const router = useRouter()

// renamed/reactive variables
const filterBy = ref('location')
const query = ref('')
const lotsList = ref([])
const usersList = ref([])
const loading = ref(false)
const error = ref('')
const searched = ref(false)

// dynamic placeholder
const hintText = computed(() => {
  if (filterBy.value === 'location') return 'e.g. T Nagar, 600017'
  if (filterBy.value === 'spot_status') return 'A or O'
  if (filterBy.value === 'user') return 'name or email'
  return 'enter search'
})

// perform server search
const performSearch = async () => {
  error.value = ''
  lotsList.value = []
  usersList.value = []
  searched.value = false

  if (!query.value || !query.value.trim()) {
    error.value = 'Please type something to search'
    return
  }

  loading.value = true
  try {
    if (filterBy.value === 'location') {
      const url = `/api/admin/lots?location=${encodeURIComponent(query.value)}`
      const res = await fetch(url, { headers: { Authorization: 'Bearer ' + localStorage.getItem('token') } })
      const data = await res.json()
      if (!res.ok) error.value = data.msg || 'Search failed'
      else lotsList.value = data
    } else if (filterBy.value === 'spot_status') {
      const url = `/api/admin/lots?spot_status=${encodeURIComponent(query.value)}`
      const res = await fetch(url, { headers: { Authorization: 'Bearer ' + localStorage.getItem('token') } })
      const data = await res.json()
      if (!res.ok) error.value = data.msg || 'Search failed'
      else lotsList.value = data
    } else if (filterBy.value === 'user') {
      const url = `/api/admin/users?query=${encodeURIComponent(query.value)}`
      const res = await fetch(url, { headers: { Authorization: 'Bearer ' + localStorage.getItem('token') } })
      const data = await res.json()
      if (!res.ok) error.value = data.msg || 'Search failed'
      else usersList.value = data
    }
  } catch (e) {
    error.value = 'Network issue — try again'
  } finally {
    loading.value = false
    searched.value = true
  }
}

// remove lot (reused API)
const removeLot = async (id) => {
  if (!confirm('Confirm deletion of this lot?')) return
  try {
    const res = await fetch(`/api/admin/lots/${id}`, {
      method: 'DELETE',
      headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
    })
    const payload = await res.json()
    if (!res.ok) {
      error.value = payload.msg || 'Delete failed'
    } else {
      // refresh current view
      performSearch()
    }
  } catch {
    error.value = 'Delete request failed'
  }
}

const openOccupied = (spotId) => {
  router.push(`/admin/occupied/${spotId}`)
}

const getProgressColor = (occupied, total) => {
  const ratio = occupied / total;
  if (ratio > 0.8) return '#ef233c'; // Red
  if (ratio > 0.5) return '#ffb703'; // Yellow
  return '#2ec4b6'; // Teal
};
</script>

<style scoped>
.admin-search-page {
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

.search-controls {
  max-width: 800px;
  margin: 0 auto;
}

.lot-panel {
  border-radius: 12px;
  background: #fff;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.lot-panel:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.08) !important;
}

.spots-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  background: #f8f9fa;
  padding: 8px;
  border-radius: 8px;
}

.spot-indicator {
  width: 28px;
  height: 28px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: default;
  user-select: none;
}

.spot-indicator.occupied { 
  background: #ffddd2; 
  color: #d00000; 
  cursor: pointer;
}

.spot-indicator.available { 
  background: #d8f3dc; 
  color: #008000; 
}

/* responsive tweaks */
@media (max-width: 768px) {
  .search-controls { flex-direction: column; align-items: stretch; }
  .search-controls .form-control, .search-controls .form-select, .search-controls .btn { width: 100% !important; }
}
</style>
