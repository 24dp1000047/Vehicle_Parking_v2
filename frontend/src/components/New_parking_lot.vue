<template>
  <div class="page-wrapper pt-3">
    <AdminNavbar />

    <div class="d-flex justify-content-center align-items-center" style="min-height: 80vh;">
      <div class="card shadow-sm border-0 p-4" style="width: 100%; max-width: 500px;">
        
        <h4 class="text-center mb-4 fw-bold text-primary">Add New Parking Lot</h4>

        <form @submit.prevent="addLot">

          <div class="mb-3">
            <label class="form-label fw-semibold">Location Name</label>
            <input type="text" v-model="prime_location_name" class="form-control" placeholder="e.g. Central Plaza" required />
          </div>

          <div class="mb-3">
            <label class="form-label fw-semibold">Address</label>
            <textarea v-model="address" class="form-control" rows="2" placeholder="Full street address" required></textarea>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label fw-semibold">Pin Code</label>
              <input type="text" v-model="pin_code" class="form-control" placeholder="123456" required />
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold">Price / Hour (₹)</label>
              <input type="number" v-model="price" min="0" class="form-control" placeholder="0" required />
            </div>
          </div>

          <div class="mb-4">
            <label class="form-label fw-semibold">Total Spots</label>
            <input type="number" v-model="maximum_number_of_spots" min="1" class="form-control" placeholder="e.g. 50" required />
          </div>

          <div class="d-grid gap-2 d-md-flex justify-content-md-between">
            <button type="button" class="btn btn-outline-secondary px-4" @click="cancel">Cancel</button>
            <button type="submit" class="btn btn-primary px-4">Create Lot</button>
          </div>

          <div v-if="error" class="alert alert-danger mt-3 py-2 text-center shadow-sm">
            {{ error }}
          </div>

          <div v-if="success" class="alert alert-success mt-3 py-2 text-center shadow-sm">
            {{ success }}
          </div>

        </form>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AdminNavbar from './AdminNavbar.vue'

const prime_location_name = ref('')
const address = ref('')
const pin_code = ref('')
const price = ref('')
const maximum_number_of_spots = ref('')
const error = ref('')
const success = ref('')

const router = useRouter()

const addLot = async () => {
  error.value = ''
  success.value = ''

  try {
    const res = await fetch('/api/admin/lots', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + localStorage.getItem('token')
      },
      body: JSON.stringify({
        prime_location_name: prime_location_name.value,
        address: address.value,
        pin_code: pin_code.value,
        price: price.value,
        maximum_number_of_spots: maximum_number_of_spots.value
      })
    })

    const data = await res.json()

    if (!res.ok) {
      error.value = data.msg || 'Failed to add parking lot'
      return
    }

    success.value = 'Parking lot added successfully!'
    setTimeout(() => router.push('/admin'), 1000)

  } catch (e) {
    error.value = 'Network error'
  }
}

const cancel = () => {
  router.push('/admin')
}
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
