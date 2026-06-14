<template>
  <div class="page-wrapper pt-3">
    <AdminNavbar />

    <div class="d-flex justify-content-center align-items-center" style="min-height: 80vh;">
      <div class="card shadow-sm border-0 p-4" style="width: 100%; max-width: 500px;">
        
        <h4 class="text-center mb-4 fw-bold text-primary">Edit Parking Lot</h4>

        <div v-if="loaded">
          <form @submit.prevent="updateLot">

            <div class="mb-3">
              <label class="form-label fw-semibold">Location Name</label>
              <input v-model="prime_location_name" type="text" class="form-control" required />
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold">Address</label>
              <textarea v-model="address" class="form-control" rows="2" required></textarea>
            </div>

            <div class="row mb-3">
              <div class="col-md-6">
                <label class="form-label fw-semibold">Pin Code</label>
                <input v-model="pin_code" type="text" class="form-control" required />
              </div>
              <div class="col-md-6">
                <label class="form-label fw-semibold">Price (per hour)</label>
                <input v-model="price" type="number" min="0" class="form-control" required />
              </div>
            </div>

            <div class="mb-4">
              <label class="form-label fw-semibold">Total Spots</label>
              <input v-model="maximum_number_of_spots" type="number" min="1" class="form-control" required />
            </div>

            <div class="d-grid gap-2 d-md-flex justify-content-md-between">
              <button type="button" class="btn btn-outline-secondary px-4" @click="cancel">Cancel</button>
              <button type="submit" class="btn btn-primary px-4">Update Lot</button>
            </div>

            <div v-if="error" class="alert alert-danger mt-3 py-2 text-center shadow-sm">
              {{ error }}
            </div>

            <div v-if="success" class="alert alert-success mt-3 py-2 text-center shadow-sm">
              {{ success }}
            </div>

          </form>
        </div>

        <div v-else class="text-center py-5 text-muted">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <div class="mt-2">Loading details...</div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import AdminNavbar from './AdminNavbar.vue'
import { API_BASE } from '../config'

const route = useRoute()
const router = useRouter()
const lotId = route.params.id

const prime_location_name = ref("")
const address = ref("")
const pin_code = ref("")
const price = ref("")
const maximum_number_of_spots = ref("")
const loaded = ref(false)
const error = ref("")
const success = ref("")

// fetch lot details for editing
const loadLot = async () => {
  error.value = ""
  try {
    const res = await fetch(`${API_BASE}/api/admin/lots`, {
      headers: { Authorization: "Bearer " + localStorage.getItem("token") }
    })

    const lots = await res.json()
    const lot = lots.find(l => l.id == lotId)

    if (!lot) {
      error.value = "Lot not found"
      return
    }

    prime_location_name.value = lot.prime_location_name
    address.value = lot.address
    pin_code.value = lot.pin_code
    price.value = lot.price
    maximum_number_of_spots.value = lot.maximum_number_of_spots

    loaded.value = true

  } catch (e) {
    error.value = "Failed to load lot"
  }
}

// update request
const updateLot = async () => {
  error.value = ""
  success.value = ""

  try {
    const res = await fetch(`/api/admin/lots/${lotId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + localStorage.getItem("token")
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
      error.value = data.msg || "Update failed"
      return
    }

    success.value = "Lot updated successfully!"
    setTimeout(() => router.push("/admin"), 1000)

  } catch (e) {
    error.value = "Network error"
  }
}

const cancel = () => {
  router.push("/admin")
}

onMounted(loadLot)
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
