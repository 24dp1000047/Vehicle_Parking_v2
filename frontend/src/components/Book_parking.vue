<template>
  <div class="page-wrapper pt-3">
    <UserNavbar />

    <div class="d-flex justify-content-center align-items-center" style="min-height: 80vh;">
      <div class="card shadow-sm border-0 p-4" style="width: 100%; max-width: 450px;">
        
        <h4 class="text-center mb-4 fw-bold text-primary">Reserve Parking Spot</h4>

        <form @submit.prevent="reserve">

          <div class="mb-3">
            <label class="form-label fw-semibold text-muted small text-uppercase">Spot ID</label>
            <input type="text" class="form-control" :value="spotId" readonly />
          </div>

          <div class="mb-3">
            <label class="form-label fw-semibold text-muted small text-uppercase">Lot ID</label>
            <input type="text" class="form-control" :value="lotId" readonly />
          </div>

          <div class="mb-3">
            <label class="form-label fw-semibold text-muted small text-uppercase">User ID</label>
            <input type="text" class="form-control" :value="userId" readonly />
          </div>

          <div class="mb-4">
            <label class="form-label fw-semibold text-muted small text-uppercase">Vehicle Number</label>
            <input v-model="vehicleNumber" type="text" class="form-control" placeholder="e.g. MH12AB1234" required />
          </div>

          <div class="d-grid gap-2">
            <button type="submit" class="btn btn-primary py-2 fw-bold">Confirm Reservation</button>
            <button type="button" class="btn btn-outline-secondary" @click="cancel">Cancel</button>
          </div>

          <div v-if="error" class="alert alert-danger mt-3 py-2 text-center shadow-sm">{{ error }}</div>
          <div v-if="success" class="alert alert-success mt-3 py-2 text-center shadow-sm">{{ success }}</div>

        </form>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import UserNavbar from './UserNavbar.vue'

const route = useRoute()
const router = useRouter()

const lotId = route.query.lot_id || route.params.lot_id
const spotId = ref('')
const userId = ref('')
const vehicleNumber = ref('')
const error = ref('')
const success = ref('')

const loadData = async () => {
  error.value = ''

  try {
    // get user ID
    const userRes = await fetch('/api/user/dashboard', {
      headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
    })
    const userData = await userRes.json()

    if (userRes.ok && userData.length > 0) {
      userId.value = userData[0].user_id || ''
    }

    // get spot for this lot
    const lotRes = await fetch(`/api/user/lots?lot_id=${lotId}`, {
      headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
    })
    const lotData = await lotRes.json()

    if (lotRes.ok && lotData.length > 0) {
      const lot = lotData[0]
      const freeSpot = lot.spots.find(s => s.status === 'A')
      spotId.value = freeSpot ? freeSpot.id : ''
    }

  } catch (e) {
    error.value = 'Could not load data'
  }
}

const reserve = async () => {
  error.value = ''
  success.value = ''

  if (!vehicleNumber.value) {
    error.value = 'Please enter vehicle number'
    return
  }

  try {
    const res = await fetch(`/api/user/book/${lotId}`, {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
        Authorization: 'Bearer ' + localStorage.getItem('token')
      },
      body: JSON.stringify({ vehicle_number: vehicleNumber.value })
    })

    const data = await res.json()

    if (!res.ok) {
      error.value = data.msg || 'Booking failed'
      return
    }

    success.value = 'Spot booked successfully!'
    setTimeout(() => router.push('/user/dashboard'), 1200)

  } catch (e) {
    error.value = 'Network error'
  }
}

const cancel = () => {
  router.push('/user/dashboard')
}

onMounted(loadData)
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
