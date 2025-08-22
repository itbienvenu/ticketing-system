<template>
  <div class="ticket-table">
    <table border="1" cellpadding="8" cellspacing="0" style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr>
          <th>Ticket ID</th>
          <th>Status</th>
          <th>Created At</th>
          <th>QR Code</th>
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
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script setup>
/* eslint-disable */
import QrcodeVue from 'qrcode.vue'

const props = defineProps({
  tickets: {
    type: Array,
    required: true
  }
})
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
