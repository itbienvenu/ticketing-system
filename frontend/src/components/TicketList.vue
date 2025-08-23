<template>
  <div class="ticket-table">
    <table border="1" cellpadding="8" cellspacing="0" style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr>
          <th>Ticket ID</th>
          <th>Status</th>
          <th>Created At</th>
          <th>QR Code</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ticket in tickets" :key="ticket.ticket_id">
          <td>{{ ticket.id }}</td>
          <td>{{ ticket.status }}</td>
          <td>{{ ticket.created_at }}</td>
          <td>
            <qrcode-vue
              :value="ticket.qr_code"
              :size="120"
              :level="'H'"
              :fg-color="'#0000ff'"
              :bg-color="'#f0f0ff'"
            />
          </td>
          <td>
            <div>
            <span style="margin: 10px;">
              <button class="btn btn-sm btn-warning">Cancel Ticket</button>
            </span>
            <span>
              <button class="btn btn-sm btn-danger" v-on:click="deleteTicket(ticket.id)">Delete Ticket</button>
            </span>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script setup>
/* eslint-disable */
import axios from 'axios';
import QrcodeVue from 'qrcode.vue'
import { ref, watch} from 'vue'


const props = defineProps({
  tickets: {
    type: Array,
    required: true
  }
})

const tickets = ref([...props.tickets])

watch(
  () => props.tickets,
  (newVal) => {
    tickets.value = [...newVal]
  }
)

const  deleteTicket = async (ticket_id) => {
    try {
    const token = localStorage.getItem('access_token')
    const confirmed = window.confirm("Do you want to delete this ticket")
    if (!confirmed) {
      return;
    }
    const response = await axios.put(`http://127.0.0.1:8000/api/v1/tickets/${ticket_id}`,
    {},

    {
      headers: {Authorization : `Bearer ${token}`}
    })
    if(response.data){
      tickets.value = tickets.value.filter(t => t.id !== ticket_id)

    }
    }
    catch (err) {
      console.log("Delete ticker error", err)
    }
}

</script>

<style scoped>
.ticket-card {
  border: 1px solid #ddd;
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 8px;
  background-color: #f9f9ff;
}
</style>
