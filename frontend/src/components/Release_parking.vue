<template>
  <div class="page-wrapper pt-3">
    <UserNavbar />

    <div class="d-flex justify-content-center align-items-center" style="min-height: 80vh;">
      <div class="card shadow-sm border-0 p-4" style="width: 100%; max-width: 450px;">
        <h4 class="text-center mb-4 fw-bold text-primary">Release Parking Spot</h4>

        <div v-if="loading" class="text-center py-5 text-muted">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <div class="mt-2">Loading details...</div>
        </div>

        <div v-else>
          <div v-if="error" class="alert alert-danger text-center shadow-sm">{{ error }}</div>

          <form v-else @submit.prevent="releaseSpot">
            <div class="mb-3">
              <label class="form-label fw-semibold text-muted small text-uppercase">Spot ID</label>
              <div class="form-control-plaintext border-bottom fw-bold">{{ reservation.spot_id || '----' }}</div>
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold text-muted small text-uppercase">Vehicle Number</label>
              <div class="form-control-plaintext border-bottom fw-bold text-dark">{{ reservation.vehicle_number || '----' }}</div>
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold text-muted small text-uppercase">Start Time</label>
              <div class="form-control-plaintext border-bottom">{{ formatDate(reservation.start_time) }}</div>
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold text-muted small text-uppercase">Release Time (Now)</label>
              <div class="form-control-plaintext border-bottom">{{ formatDate(now) }}</div>
            </div>

            <div class="mb-4">
              <label class="form-label fw-semibold text-muted small text-uppercase">Estimated Cost</label>
              <div class="form-control-plaintext border-bottom text-success fw-bold fs-5">{{ displayCost }}</div>
            </div>

            <div class="d-grid gap-2">
              <button type="submit" class="btn btn-primary py-2 fw-bold">Confirm Release</button>
              <button type="button" class="btn btn-outline-secondary" @click="cancel">Cancel</button>
            </div>

            <div v-if="success" class="alert alert-success mt-3 text-center shadow-sm">{{ success }}</div>
          </form>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import UserNavbar from './UserNavbar.vue'

const route = useRoute()
const router = useRouter()

// reservation id comes from ?reservation_id= or params
const reservationId = route.query.reservation_id || route.params.reservation_id

const reservation = ref({})
const loading = ref(true)
const error = ref('')
const success = ref('')
const now = ref(new Date())

// safe date formatter
function formatDate(v) {
  if (!v) return '----'
  // If it's already formatted (contains comma or slash), return as is
  if (typeof v === 'string' && (v.includes(',') || v.includes('/'))) {
    return v
  }
  try {
    let s = v
    if (typeof s === 'string' && /^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}/.test(s)) {
      s = s.replace(/\s+/, 'T')
    }
    // Don't add Z - let the browser parse it as local time if no timezone specified
    const d = new Date(s)
    if (isNaN(d.getTime())) return '----'
    return d.toLocaleString('en-IN', { timeZone: 'Asia/Kolkata', hour12: true })
  } catch {
    return '----'
  }
}

const displayCost = computed(() => {
  const rate = reservation.value.parking_cost_per_unit
  if (rate == null) return '----'
  
  // Use ISO time if available for accurate calculation
  let startStr = reservation.value.start_time_iso || reservation.value.start_time
  
  // If start_time is the formatted string (DD/MM/YYYY...), we can't easily parse it with new Date() directly in all browsers
  // But start_time_iso should be present from the backend
  
  if (!startStr) return '----'
  
  let start = new Date(startStr)
  
  // Fallback parsing for non-ISO strings if needed (though backend sends ISO)
  if (isNaN(start.getTime()) && typeof startStr === 'string') {
      // Try to handle the specific format if ISO is missing
      // But let's rely on ISO first.
      return '----'
  }

  const end = now.value
  const diffMs = end - start
  // Ensure non-negative
  if (diffMs < 0) return '₹0.00'
  
  const diffHrs = diffMs / (1000 * 60 * 60)
  const cost = diffHrs * rate
  
  return `₹${cost.toFixed(2)}`
})

// fetch reservation data (example: uses /api/user/dashboard to find reservation)
// adjust if you have a direct reservation endpoint
const fetchReservation = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await fetch('/api/user/dashboard', {
      headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
    })
    const data = await res.json()
    if (!res.ok) {
      error.value = data.msg || 'Failed to load reservation'
      loading.value = false
      return
    }
    // find reservation by id
    const found = Array.isArray(data) ? data.find(r => String(r.id) === String(reservationId)) : null
    if (!found) {
      error.value = 'Reservation not found'
      loading.value = false
      return
    }
    reservation.value = found
  } catch (e) {
    error.value = 'Network error'
  } finally {
    loading.value = false
  }
}

// call release endpoint
const releaseSpot = async () => {
  error.value = ''
  success.value = ''
  try {
    const res = await fetch(`/api/user/release/${reservationId}`, {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
    })
    const data = await res.json()
    if (!res.ok) {
      error.value = data.msg || 'Release failed'
      return
    }
    success.value = 'Spot released successfully!'
    // small delay then go back to dashboard
    setTimeout(() => router.push('/user/dashboard'), 1100)
  } catch (e) {
    error.value = 'Network error'
  }
}

const cancel = () => {
  router.push('/user/dashboard')
}

// load data when component mounts
onMounted(() => {
  now.value = new Date()
  fetchReservation()
})
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
