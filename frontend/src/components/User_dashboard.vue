<template>
  <div class="wrapper pt-3">
    <UserNavbar />

    <!-- Main Title -->
    <h3 class="text-center section-title mb-4">Find & Book Parking</h3>

    <!-- Search Bar -->
    <div class="search-container mb-5">
      <div class="input-group shadow-sm">
        <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-muted"></i></span>
        <input 
          v-model="searchString" 
          @keyup.enter="searchLots" 
          class="form-control border-start-0 ps-0" 
          placeholder="Search by location (e.g. 'Downtown')" 
        />
        <button class="btn btn-primary px-4" @click="searchLots">Search</button>
        <button v-if="searchString" class="btn btn-outline-secondary px-3" @click="clearSearch">Clear</button>
      </div>
    </div>

    <!-- Parking Lots Grid -->
    <div class="row g-4 mb-5">
      <div class="col-md-6 col-lg-4" v-for="lot in lots" :key="lot.id">
        <div class="card lot-card h-100 border-0 shadow-sm">
          <div class="card-body d-flex flex-column">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <h5 class="card-title fw-bold text-dark mb-0">{{ lot.prime_location_name }}</h5>
              <span class="badge bg-light text-dark border">₹{{ lot.price }}/hr</span>
            </div>
            
            <p class="text-muted small mb-3">
              <i class="bi bi-geo-alt-fill me-1 text-danger"></i> {{ lot.address }} - {{ lot.pin_code }}
            </p>

            <div class="mb-3">
              <div class="d-flex justify-content-between small text-muted mb-1">
                <span>Availability</span>
                <span :class="lot.available > 0 ? 'text-success fw-bold' : 'text-danger fw-bold'">
                  {{ lot.available }} spots left
                </span>
              </div>
              <div class="progress" style="height: 6px;">
                <div 
                  class="progress-bar" 
                  role="progressbar" 
                  :style="{ width: (100 - (lot.available / lot.maximum_number_of_spots * 100)) + '%', backgroundColor: getProgressColor(lot.available, lot.maximum_number_of_spots) }"
                  :aria-valuenow="lot.available" 
                  aria-valuemin="0" 
                  :aria-valuemax="lot.maximum_number_of_spots">
                </div>
              </div>
            </div>

            <div class="mt-auto">
              <button 
                v-if="lot.available > 0" 
                class="btn btn-primary w-100 fw-bold" 
                @click="openBookingModal(lot.id)"
              >
                Book Now
              </button>
              <button v-else class="btn btn-secondary w-100" disabled>
                Full
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Download CSV Button -->
    <div class="mb-4 text-end">
      <button class="btn btn-outline-primary" @click="downloadCSV" :disabled="csvLoading">
        <span v-if="csvLoading"><i class="bi bi-arrow-repeat"></i> Preparing...</span>
        <span v-else><i class="bi bi-download"></i> Download CSV Report</span>
      </button>
    </div>

    <!-- Booking History Section -->
    <div class="history-section mt-5">
      <h4 class="mb-4 fw-bold text-dark border-bottom pb-2">Your Booking History</h4>
      
      <div class="card border-0 shadow-sm">
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th class="py-3 ps-4">Location</th>
                  <th class="py-3">Spot</th>
                  <th class="py-3">Vehicle</th>
                  <th class="py-3">Start Time</th>
                  <th class="py-3">Status</th>
                  <th class="py-3 pe-4 text-end">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="history.length === 0">
                  <td colspan="6" class="text-center py-4 text-muted">No bookings found.</td>
                </tr>
                <tr v-for="r in history" :key="r.id">
                  <td class="ps-4 fw-bold text-primary">{{ r.location }}</td>
                  <td><span class="badge bg-light text-dark border">{{ r.spot_id }}</span></td>
                  <td>{{ r.vehicle_number }}</td>
                  <td class="small text-muted">{{ formatDate(r.start_time) }}</td>
                  <td>
                    <span :class="getStatusBadgeClass(r.status)" class="badge">
                      {{ r.status }}
                    </span>
                  </td>
                  <td class="pe-4 text-end">
                    <button 
                      v-if="r.status === 'active'" 
                      class="btn btn-sm btn-outline-danger" 
                      @click="goToRelease(r.id)"
                    >
                      Release
                    </button>
                    <span v-else class="text-muted small">-</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Booking Modal -->
    <div v-if="showModal" class="modal-backdrop">
      <div class="modal-box shadow-lg">
        <h4 class="mb-3 fw-bold text-center">Confirm Booking</h4>
        <div v-if="selectedLot" class="text-center mb-3">
          <span class="badge bg-primary fs-6">Rate: ₹{{ selectedLot.price }}/hr</span>
        </div>
        <p class="text-muted text-center small mb-4">Enter your vehicle number to reserve a spot.</p>
        
        <div class="mb-3">
          <label class="form-label fw-semibold">Vehicle Number</label>
          <input 
            v-model="bookingVehicleNumber" 
            type="text" 
            class="form-control" 
            placeholder="e.g. MH12AB1234" 
            autofocus
          />
        </div>

        <div class="d-grid gap-2">
          <button class="btn btn-primary" @click="book">Confirm Booking</button>
          <button class="btn btn-outline-secondary" @click="closeBookingModal">Cancel</button>
        </div>

        <div v-if="error" class="alert alert-danger mt-3 py-2 text-center small mb-0">{{ error }}</div>
        <div v-if="success" class="alert alert-success mt-3 py-2 text-center small mb-0">{{ success }}</div>
      </div>
    </div>

    <div v-if="error && !showModal" class="alert alert-danger mt-3 text-center shadow-sm">{{ error }}</div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import UserNavbar from './UserNavbar.vue'

const router = useRouter()
const lots = ref([])
const history = ref([])
const searchString = ref('')
const error = ref('')
const success = ref('')
const csvLoading = ref(false)

// Modal state
const showModal = ref(false)
const bookingLotId = ref(null)
const bookingVehicleNumber = ref('')

const openBookingModal = (lotId) => {
  bookingLotId.value = lotId
  bookingVehicleNumber.value = ''
  error.value = ''
  success.value = ''
  showModal.value = true
}

const closeBookingModal = () => {
  showModal.value = false
  bookingLotId.value = null
  bookingVehicleNumber.value = ''
}

const selectedLot = computed(() => {
  if (!bookingLotId.value) return null
  return lots.value.find(l => l.id == bookingLotId.value)
})

function formatDate(dt) {
  if (!dt) return '----'
  if (typeof dt === 'string' && (dt.includes(',') || dt.includes('/'))) {
    return dt
  }
  try {
    let s = dt
    if (typeof s === 'string') {
      if (/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}/.test(s)) {
        s = s.replace(' ', 'T')
      }
    }
    const d = new Date(s)
    if (isNaN(d.getTime())) return '----'
    return d.toLocaleString('en-IN', { timeZone: 'Asia/Kolkata', hour12: true, timeZoneName: 'short' })
  } catch (e) {
    return '-'
  }
}

const fetchHistory = async () => {
  error.value = ''
  try {
    const res = await fetch('/api/user/dashboard', {
      headers: {
        Authorization: 'Bearer ' + localStorage.getItem('token')
      }
    })
    const data = await res.json()
    if (!res.ok) {
      error.value = data.msg || 'Failed to load history'
      return
    }
    
    // Use the backend data directly - it already includes location
    history.value = data
  } catch (e) {
    error.value = 'Network error'
  }
}

const fetchLots = async () => {
  error.value = ''
  lots.value = []
  try {
    let url = '/api/user/lots'
    const params = new URLSearchParams()
    if (searchString.value) {
      params.append('location', searchString.value)
    }
    // Add cache buster
    params.append('_t', Date.now())
    if (params.toString()) {
      url += `?${params.toString()}`
    }
    const res = await fetch(url, {
      headers: {
        Authorization: 'Bearer ' + localStorage.getItem('token')
      }
    })
    const data = await res.json()
    if (!res.ok) {
      error.value = data.msg || 'Failed to load lots'
      return
    }
    lots.value = data.map(lot => ({
      ...lot,
      available: (lot.maximum_number_of_spots || 0) - (lot.occupied_spots || 0)
    }))
  } catch (e) {
    error.value = 'Network error'
  }
}

const searchLots = () => {
  fetchLots()
}

const clearSearch = () => {
  searchString.value = ''
  fetchLots()
}

const book = async () => {
  error.value = ''
  success.value = ''
  if (!bookingVehicleNumber.value) {
    error.value = 'Please enter your vehicle number.'
    return
  }
  try {
    const res = await fetch(`/api/user/book/${bookingLotId.value}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + localStorage.getItem('token')
      },
      body: JSON.stringify({ vehicle_number: bookingVehicleNumber.value })
    })
    const data = await res.json()
    if (!res.ok) {
      error.value = data.msg || 'Booking failed'
      return
    }
    success.value = 'Spot booked successfully!'
    setTimeout(() => {
      closeBookingModal()
      fetchLots()
      fetchHistory()
    }, 1000)
  } catch (e) {
    error.value = 'Network error'
  }
}

const goToRelease = (reservationId) => {
  router.push(`/user/release?reservation_id=${reservationId}`)
}

const getProgressColor = (available, total) => {
  const ratio = available / total;
  if (ratio < 0.2) return '#ef233c'; // Red (Low availability)
  if (ratio < 0.5) return '#ffb703'; // Yellow
  return '#2ec4b6'; // Teal (High availability)
};

const getStatusBadgeClass = (status) => {
  if (status === 'active') return 'bg-success';
  if (status === 'completed') return 'bg-secondary';
  return 'bg-light text-dark border';
};

const downloadCSV = async () => {
  csvLoading.value = true
  error.value = ''
  try {
    const res = await fetch('/api/user/export/csv', {
      method: 'GET',
      headers: {
        Authorization: 'Bearer ' + localStorage.getItem('token')
      }
    })
    if (!res.ok) {
      const data = await res.json()
      error.value = data.msg || 'Failed to export CSV'
      csvLoading.value = false
      return
    }
    const blob = await res.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'parking_report.csv'
    document.body.appendChild(a)
    a.click()
    a.remove()
    window.URL.revokeObjectURL(url)
  } catch (e) {
    error.value = 'Network error'
  }
  csvLoading.value = false
}

onMounted(() => {
  fetchHistory()
  fetchLots()
})
</script>

<style scoped>
.wrapper {
  max-width: 1200px;
  margin: auto;
  padding-left: 15px;
  padding-right: 15px;
}

.section-title {
  color: #2b2d42;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.search-container {
  max-width: 600px;
  margin: 0 auto;
}

.lot-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border-radius: 12px;
  background: #fff;
}

.lot-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.08) !important;
}

.modal-backdrop {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-box {
  background: #fff;
  padding: 30px;
  border-radius: 16px;
  width: 90%;
  max-width: 400px;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>
