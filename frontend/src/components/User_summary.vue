<template>
  <div class="page-wrapper pt-3">
    <UserNavbar />

    <div class="content-area container">
      <header class="mb-4 text-center">
        <h3 class="section-title">My Parking Summary</h3>
        <p class="text-muted">Overview of your parking usage and activity</p>
      </header>

      <div v-if="loading" class="text-center py-5 text-muted">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <div class="mt-2">Loading summary...</div>
      </div>

      <div v-else>
        <div v-if="error" class="alert alert-danger text-center shadow-sm">{{ error }}</div>

        <!-- simple stat cards -->
        <div class="row g-4 justify-content-center mb-5">
          <div class="col-md-5 col-lg-4">
            <div class="card stat-card h-100 border-0 shadow-sm">
              <div class="card-body text-center py-4">
                <div class="icon-circle bg-primary-subtle text-primary mb-3 mx-auto">
                  <i class="bi bi-p-square-fill fs-4"></i>
                </div>
                <h6 class="text-muted text-uppercase small fw-bold mb-2">Total Used Spots</h6>
                <h2 class="display-5 fw-bold text-dark mb-0">{{ usedSpots }}</h2>
              </div>
            </div>
          </div>

          <div class="col-md-5 col-lg-4">
            <div class="card stat-card h-100 border-0 shadow-sm">
              <div class="card-body text-center py-4">
                <div class="icon-circle bg-success-subtle text-success mb-3 mx-auto">
                  <i class="bi bi-check-circle-fill fs-4"></i>
                </div>
                <h6 class="text-muted text-uppercase small fw-bold mb-2">Currently Active</h6>
                <h2 class="display-5 fw-bold text-dark mb-0">{{ activeSpots }}</h2>
              </div>
            </div>
          </div>
        </div>

        <!-- small bar chart -->
        <div class="row justify-content-center">
          <div class="col-md-10 col-lg-8">
            <div class="card border-0 shadow-sm">
              <div class="card-body p-4">
                <h5 class="card-title fw-bold text-dark mb-4">Activity Overview</h5>
                <div class="chart-container" style="position: relative; height:300px;">
                  <Bar v-if="barData" :data="barData" :options="barOptions" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js'
import { useRouter } from 'vue-router'
import UserNavbar from './UserNavbar.vue'

Chart.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend)

const usedSpots = ref(0)
const activeSpots = ref(0)
const barData = ref(null)
const barOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: { 
    y: { 
      beginAtZero: true, 
      ticks: { precision: 0 },
      grid: { color: '#f0f0f0' }
    },
    x: {
      grid: { display: false }
    }
  }
})

const error = ref('')
const loading = ref(true)
const router = useRouter()

const fetchSummary = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await fetch('/api/user/summary', {
      headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
    })
    const data = await res.json()
    if (!res.ok) {
      error.value = data.msg || 'Failed to load summary'
      loading.value = false
      return
    }

    // simple numbers (safe fallbacks)
    usedSpots.value = Number(data.used_spots || 0)
    activeSpots.value = Number(data.active_spots || 0)

    // prepare bar data
    barData.value = {
      labels: ['Total Used', 'Currently Active'],
      datasets: [
        {
          label: 'Count',
          data: [usedSpots.value, activeSpots.value],
          backgroundColor: ['#4361ee', '#2ec4b6'],
          borderRadius: 6,
          barThickness: 50
        }
      ]
    }
  } catch (e) {
    error.value = 'Network error'
  }
  loading.value = false
}

onMounted(fetchSummary)
</script>

<style scoped>
.page-wrapper {
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

.stat-card {
  border-radius: 12px;
  background: #fff;
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.icon-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card {
  border-radius: 12px;
}
</style>
