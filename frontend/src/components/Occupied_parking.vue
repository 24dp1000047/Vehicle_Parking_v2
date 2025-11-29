<template>
  <div class="page-wrapper pt-3">
    <AdminNavbar />

    <div class="d-flex justify-content-center align-items-center" style="min-height: 80vh;">
      <div class="card shadow-sm border-0 p-4" style="width: 100%; max-width: 450px;">
        <h4 class="text-center mb-4 fw-bold text-primary">Occupied Spot Details</h4>

        <div v-if="loading" class="text-center py-5 text-muted">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <div class="mt-2">Loading details...</div>
        </div>

        <div v-else>
          <div v-if="error" class="alert alert-danger text-center shadow-sm">{{ error }}</div>

          <div v-else>
            <div class="mb-3">
              <label class="form-label fw-semibold text-muted small text-uppercase">Spot ID</label>
              <div class="form-control-plaintext border-bottom fw-bold">{{ spot.id || '----' }}</div>
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold text-muted small text-uppercase">Customer ID</label>
              <div class="form-control-plaintext border-bottom">{{ reservation?.user_id || '----' }}</div>
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold text-muted small text-uppercase">Vehicle Number</label>
              <div class="form-control-plaintext border-bottom fw-bold text-dark">{{ reservation?.vehicle_number || '----' }}</div>
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold text-muted small text-uppercase">Start Time</label>
              <div class="form-control-plaintext border-bottom">{{ formatDate(reservation?.start_time) }}</div>
            </div>

            <div class="mb-4">
              <label class="form-label fw-semibold text-muted small text-uppercase">Estimated Cost / Unit</label>
              <div class="form-control-plaintext border-bottom text-success fw-bold">
                {{ reservation?.parking_cost_per_unit ? '₹' + reservation.parking_cost_per_unit : '----' }}
              </div>
            </div>

            <div class="d-grid">
              <button class="btn btn-secondary" @click="close">Close</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AdminNavbar from './AdminNavbar.vue'

const route = useRoute()
const router = useRouter()
const spotId = route.params.spot_id || route.query.spot_id

const spot = ref({})
const reservation = ref(null)
const loading = ref(true)
const error = ref('')

function formatDate(val) {
  if (!val) return '----'
  // If it's already formatted by backend (contains / or ,), return as is
  if (typeof val === 'string' && (val.includes('/') || val.includes(','))) {
    return val
  }
  try {
    let s = val
    if (typeof s === 'string' && /^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}/.test(s)) {
      s = s.replace(/\s+/, 'T') + 'Z'
    }
    const d = new Date(s)
    if (isNaN(d.getTime())) return '----'
    return d.toLocaleString('en-IN', { timeZone: 'Asia/Kolkata', hour12: true })
  } catch {
    return '----'
  }
}

const fetchSpot = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await fetch(`/api/admin/spots/${spotId}`, {
      headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
    })
    const data = await res.json()
    if (!res.ok) {
      error.value = data.msg || 'Failed to load'
      loading.value = false
      return
    }
    // API may return spot and reservation or flat object
    spot.value = data.spot || data || {}
    reservation.value = data.reservation || data.reservation || null
  } catch {
    error.value = 'Network error'
  }
  loading.value = false
}

const close = () => {
  router.back()
}

onMounted(fetchSpot)
</script>

<style scoped>
.page-wrapper {
  max-width: 1200px;
  margin: auto;
  padding-left: 15px;
  padding-right: 15px;
}

.card {
  border-radius: 12px;
  background: #fff;
}
</style>
