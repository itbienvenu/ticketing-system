<template>
  <div class="d-flex vh-100 bg-light">
    <!-- Sidebar -->
    <Sidebar @navigate="activeTab = $event" />

    <!-- Main Content -->
    <div class="flex-grow-1 p-4">
      <Header :user="user" />

      <div class="mt-4">
        <!-- Tickets Section -->
        <div v-if="activeTab === 'tickets'">
          <TicketList :tickets="tickets" />
          <TicketForm @ticket-added="fetchTickets" />
        </div>

        <!-- Routes Section -->
        <div v-else-if="activeTab === 'routes'">
          <Routes />
        </div>

        <!-- Fallback -->
        <div v-else>
          <p class="text-muted">Please select a section from the sidebar.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

import Sidebar from './SideBar.vue'
import Header from './HeaderBar.vue'
import TicketList from './TicketList.vue'
import TicketForm from './TicketForm.vue'
import Routes from './RoutesComponent.vue'
import router from '@/router/router'

const user = ref({})
const tickets = ref([])
const activeTab = ref('tickets') // default view
const API_BASE = process.env.VUE_APP_API_BASE_URL;

const fetchUser = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await axios.get(`${API_BASE}/me`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    user.value = response.data
    if (response.data.role == "admin") {
      router.push('/admin')
    } else if(response.data.role == "manager"){
      router.push('/admin')
    }
    fetchTickets(user.value.id)
  } catch (err) {
    console.error('Failed to fetch user', err)
  }
}

const fetchTickets = async (userId) => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await axios.get(
      `${API_BASE}/tickets/users/${userId}`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    tickets.value = response.data
  } catch (err) {
    console.error('Failed to fetch tickets', err)
  }
}

onMounted(() => {
  fetchUser()
})
</script>
