<template>
  <div class="wrapper pt-3">
    <AdminNavbar />

    <!-- Main Title -->
    <h3 class="text-center section-title mb-4">Parking Lots Management</h3>

    <!-- Parking Lot Cards -->
    <div class="row g-4">
      <div class="col-md-6 col-lg-4" v-for="lot in lots" :key="lot.id">
        <div class="card lot-card h-100 border-0 shadow-sm">
          <div class="card-body d-flex flex-column">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <h5 class="card-title fw-bold text-primary mb-0">{{ lot.prime_location_name }}</h5>
              <span class="badge bg-light text-dark border">ID: {{ lot.id }}</span>
            </div>

            <p class="text-muted small mb-2">
              <i class="bi bi-geo-alt-fill me-1"></i> {{ lot.address }} - {{ lot.pin_code }}
            </p>
            <p class="fw-bold text-success mb-3">
              ₹{{ lot.price }}/hr
            </p>

            <div class="mb-3">
              <div class="d-flex justify-content-between small text-muted mb-1">
                <span>Occupancy</span>
                <span>{{ lot.occupied_spots }} / {{ lot.maximum_number_of_spots }}</span>
              </div>
              <div class="progress" style="height: 8px;">
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

            <div class="spots-grid mb-3 flex-grow-1">
              <span
                v-for="spot in lot.spots"
                :key="spot.id"
                class="spot-box"
                :class="spot.status === 'O' ? 'spot-occupied' : 'spot-free'"
                :title="`Spot #${spot.spot_number} - ${spot.status === 'O' ? 'Occupied' : 'Available'}`"
                @click="spot.status === 'O' && goToOccupied(spot.id)"
              >
                {{ spot.spot_number }}
              </span>
            </div>

            <div class="d-flex gap-2 mt-auto">
              <router-link :to="`/admin/edit-lot/${lot.id}`" class="btn btn-sm btn-outline-primary flex-grow-1">
                <i class="bi bi-pencil-square"></i> Edit
              </router-link>
              <button class="btn btn-sm btn-outline-danger flex-grow-1" @click="deleteLot(lot.id)">
                <i class="bi bi-trash"></i> Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add New Lot FAB or Button -->
    <div class="text-center mt-5 mb-5">
      <router-link to="/admin/new-lot" class="btn btn-primary btn-lg shadow-sm px-4 rounded-pill">
        <i class="bi bi-plus-lg me-2"></i> Create New Parking Lot
      </router-link>
    </div>

    <div v-if="error" class="alert alert-danger mt-3 text-center shadow-sm">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import AdminNavbar from './AdminNavbar.vue';
import { API_BASE } from '../config'

const router = useRouter();
const lots = ref([]);
const error = ref("");

const fetchLots = async () => {
  try {
    error.value = "";
    // Add timestamp to bypass all caching
    const timestamp = new Date().getTime();
    const res = await fetch(`/api/admin/lots?_t=${timestamp}`, {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
      },
    });

    if (res.status === 403) {
      router.push("/");
      return;
    }

    lots.value = await res.json();
  } catch {
    error.value = "Unable to fetch parking lots";
  }
};

const deleteLot = async (id) => {
  if (!confirm("Delete this parking lot? This action cannot be undone.")) return;

  try {
    const res = await fetch(`/api/admin/lots/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    });

    const result = await res.json();

    if (!res.ok) {
      error.value = result.msg || "Deletion failed";
    } else {
      fetchLots();
    }
  } catch {
    error.value = "Error while deleting";
  }
};

const goToOccupied = (id) => {
  router.push(`/admin/occupied/${id}`);
};

const getProgressColor = (occupied, total) => {
  const ratio = occupied / total;
  if (ratio > 0.8) return '#ef233c'; // Red
  if (ratio > 0.5) return '#ffb703'; // Yellow
  return '#2ec4b6'; // Teal
};

onMounted(fetchLots);
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

.lot-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border-radius: 12px;
  background: #fff;
}

.lot-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.08) !important;
}

.spots-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  background: #f8f9fa;
  border-radius: 8px;
  padding: 8px;
  max-height: 120px;
  overflow-y: auto;
}

.spot-box {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: default;
  transition: opacity 0.2s;
}

.spot-occupied {
  background: #ffddd2;
  color: #d00000;
  cursor: pointer;
}

.spot-occupied:hover {
  opacity: 0.8;
}

.spot-free {
  background: #d8f3dc;
  color: #008000;
}

/* Custom Scrollbar for spots grid */
.spots-grid::-webkit-scrollbar {
  width: 4px;
}
.spots-grid::-webkit-scrollbar-track {
  background: #f1f1f1; 
}
.spots-grid::-webkit-scrollbar-thumb {
  background: #ccc; 
  border-radius: 4px;
}
</style>
