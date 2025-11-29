<template>
  <div class="summary-wrap pt-3">
    <AdminNavbar />

    <!-- compact header -->
    <header class="mb-4 text-center">
      <h3 class="section-title">Admin Insights</h3>
      <p class="text-muted">Visual overview of parking performance</p>
    </header>

    <!-- charts row -->
    <div class="row gx-4 gy-4">
      <div class="col-md-6">
        <div class="card chart-card h-100 border-0 shadow-sm">
          <div class="card-body d-flex flex-column">
            <h6 class="card-heading text-primary fw-bold mb-3">Revenue by Lot</h6>
            <div class="chart-area flex-grow-1">
              <Pie v-if="pieChart" :data="pieChart" :options="pieOptions" />
            </div>
            <small class="mt-3 text-muted text-center">Total revenue collected per lot (completed sessions)</small>
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card chart-card h-100 border-0 shadow-sm">
          <div class="card-body d-flex flex-column">
            <h6 class="card-heading text-primary fw-bold mb-3">Slot Occupancy</h6>
            <div class="chart-area flex-grow-1">
              <Bar v-if="stackBar" :data="stackBar" :options="barOptions" />
            </div>
            <small class="mt-3 text-muted text-center">Occupied vs free spots across lots</small>
          </div>
        </div>
      </div>
    </div>

    <!-- messages -->
    <div v-if="error" class="alert alert-danger mt-4 text-center shadow-sm">{{ error }}</div>
    <div v-if="loading" class="text-center py-4 text-muted">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <div class="mt-2">Fetching analytics...</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Pie, Bar } from 'vue-chartjs'
import {
  Chart,
  ArcElement,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { useRouter } from 'vue-router'
import AdminNavbar from './AdminNavbar.vue'

Chart.register(ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const router = useRouter()
const pieChart = ref(null)
const stackBar = ref(null)
const pieOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { position: 'right' } }
}
const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { position: 'top' } },
  scales: {
    y: { beginAtZero: true }
  }
}
const error = ref('')
const loading = ref(true)

/*
  Fetch summary data and prepare:
  - Pie: revenue summed per lot name
  - Bar: occupied and free counts per lot
*/
const fetchAnalytics = async () => {
  loading.value = true
  error.value = ''
  try {
    // get raw summary (sessions / bookings)
    const res = await fetch('/api/admin/summary', {
      headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
    })
    const sessions = await res.json()
    if (!res.ok) {
      error.value = sessions.msg || 'Unable to load summary'
      loading.value = false
      return
    }

    // fetch lots to map names and spots
    const lotsRes = await fetch('/api/admin/lots', {
      headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
    })
    const lots = await lotsRes.json()
    if (!lotsRes.ok) {
      error.value = lots.msg || 'Failed to fetch lots'
      loading.value = false
      return
    }

    // build maps keyed by lot id
    const revenueByLot = new Map()
    const occupancyByLot = new Map()
    // initialize from lots list
    lots.forEach(l => {
      revenueByLot.set(l.id, 0)
      const occ = { occupied: 0, free: 0 }
      l.spots.forEach(s => {
        if (s.status === 'O') occ.occupied += 1
        else occ.free += 1
      })
      occupancyByLot.set(l.id, occ)
    })

    // accumulate revenue from session records (assume sessions include lot_id or spot_id)
    sessions.forEach(s => {
      // prefer explicit lot_id, otherwise try to match using spot_id
      const lotId = s.lot_id ?? s.lotId ?? null
      if (lotId && revenueByLot.has(lotId)) {
        if (s.status === 'completed') {
          revenueByLot.set(lotId, revenueByLot.get(lotId) + (s.parking_cost_per_unit || 0))
        }
      } else {
        // try matching by spot id to find parent lot
        if (s.spot_id) {
          for (const l of lots) {
            if (l.spots.some(sp => sp.id === s.spot_id)) {
              if (s.status === 'completed') {
                revenueByLot.set(l.id, revenueByLot.get(l.id) + (s.parking_cost_per_unit || 0))
              }
              break
            }
          }
        }
      }
    })

    // prepare Pie (labels & values)
    const pieLabels = []
    const pieValues = []
    const palette = []
    lots.forEach((l, idx) => {
      pieLabels.push(l.prime_location_name)
      pieValues.push(revenueByLot.get(l.id) || 0)
      // simple color rotation
      const colours = ['#4361ee', '#3a0ca3', '#7209b7', '#f72585', '#4cc9f0', '#4895ef']
      palette.push(colours[idx % colours.length])
    })
    pieChart.value = {
      labels: pieLabels,
      datasets: [{ data: pieValues, backgroundColor: palette }]
    }

    // prepare stacked bar: occupied and free
    const barLabels = []
    const occData = []
    const freeData = []
    lots.forEach(l => {
      barLabels.push(l.prime_location_name)
      const occ = occupancyByLot.get(l.id) || { occupied: 0, free: 0 }
      occData.push(occ.occupied)
      freeData.push(occ.free)
    })
    stackBar.value = {
      labels: barLabels,
      datasets: [
        { label: 'Occupied', data: occData, backgroundColor: '#ef233c' },
        { label: 'Free', data: freeData, backgroundColor: '#2ec4b6' }
      ]
    }
  } catch (e) {
    error.value = 'Network error while loading analytics'
  } finally {
    loading.value = false
  }
}

onMounted(fetchAnalytics)
</script>

<style scoped>
.summary-wrap { 
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

.chart-card {
  border-radius: 12px;
  background: #fff;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.chart-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.08) !important;
}

.chart-area {
  min-height: 300px;
  position: relative;
}
</style>
