<template>
  <div class="mt-4">
    <h4>Add New Ticket</h4>
    <form @submit.prevent="addTicket">
      <div class="mb-2">
        <input v-model="title" class="form-control" placeholder="Ticket Title" required>
      </div>
      <button class="btn btn-primary">Add Ticket</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { defineEmits } from 'vue'

const title = ref("")
const emit = defineEmits(['ticket-added'])

const addTicket = async () => {
  try {
    const token = localStorage.getItem('access_token')
    await axios.post('http://127.0.0.1:8000/api/v1/tickets', 
      { title },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    title.value = ""
    emit('ticket-added')
  } catch (err) {
    console.error("Failed to add ticket", err)
  }
}
</script>
