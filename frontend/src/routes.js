import { createRouter, createWebHistory } from 'vue-router'
import AdminDashboard from './components/Admin_dashboard.vue'
import NewParkingLot from './components/New_parking_lot.vue'
import EditParkingLot from './components/Edit_parking_lot.vue'
import OccupiedParking from './components/Occupied_parking.vue'
import AdminUser from './components/Admin_user.vue'
import AdminSummary from './components/Admin_summary.vue'
import Login from './components/Login.vue'
import Register from './components/Register.vue'
import UserDashboard from './components/User_dashboard.vue'
import BookParking from './components/Book_parking.vue'
import ReleaseParking from './components/Release_parking.vue'
import UserSummary from './components/User_summary.vue'
import AdminSearch from './components/Admin_search.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/register', component: Register },
  { path: '/admin', component: AdminDashboard },
  { path: '/admin/new-lot', component: NewParkingLot },
  { path: '/admin/edit-lot/:id', component: EditParkingLot, props: true },
  { path: '/admin/occupied', component: OccupiedParking },
  { path: '/admin/occupied/:spot_id', component: OccupiedParking },
  { path: '/admin/users', component: AdminUser },
  { path: '/admin/summary', component: AdminSummary },
  { path: '/user/dashboard', component: UserDashboard },
  { path: '/user/book', component: BookParking },
  { path: '/user/release', component: ReleaseParking },
  { path: '/user/summary', component: UserSummary },
  { path: '/admin/search', component: AdminSearch }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router