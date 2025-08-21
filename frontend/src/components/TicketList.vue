<template>
  <div v-for="ticket in tickets" :key="ticket.id" class="ticket-card">
    <p>Status: {{ ticket.status }}</p>
    <p>Created: {{ ticket.created_at }}</p>
    <qrcode-vue
      :value="ticket.qr_code"
      :size="150"
      :level="'H'"
      :fg-color="'#0000ff'"
      :bg-color="'#f0f0ff'"
    />
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
