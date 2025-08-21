<template>
  <div class="d-flex vh-100 bg-light">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Main Content -->
    <div class="flex-grow-1 p-4">
      <Header :user="user" />

      <div class="mt-4">
        <!-- Ticket Section -->
        <TicketList :tickets="tickets" />

        <!-- Add Ticket Form -->
        <TicketForm @ticket-added="fetchTickets" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Sidebar from './components/Sidebar.vue'
import Header from './components/Header.vue'
import TicketList from './components/TicketList.vue'
import TicketForm from './components/TicketForm.vue'

const user = ref({})
const tickets = ref([])

const fetchUser = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await axios.get('http://127.0.0.1:8000/api/v1/me', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    user.value = response.data
  } catch (err) {
    console.error('Failed to fetch user', err)
  }
}

const fetchTickets = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await axios.get('http://127.0.0.1:8000/api/v1/tickets', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    tickets.value = response.data
  } catch (err) {
    console.error('Failed to fetch tickets', err)
  }
}

onMounted(() => {
  fetchUser()
  fetchTickets()
})
</script>
