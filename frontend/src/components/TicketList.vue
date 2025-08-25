<template>
  <div class="ticket-table container-fluid p-4 bg-light min-vh-100">
    <div class="card shadow-lg mx-auto" style="max-width: 900px;">
      <div class="card-body p-0">
        <table class="table table-bordered table-striped table-hover m-0">
          <thead class="bg-light">
            <tr>
              <th scope="col" class="px-3 py-2 text-left text-xs font-weight-bold text-secondary text-uppercase">Ticket ID</th>
              <th scope="col" class="px-3 py-2 text-left text-xs font-weight-bold text-secondary text-uppercase">Status</th>
              <th scope="col" class="px-3 py-2 text-left text-xs font-weight-bold text-secondary text-uppercase">Created At</th>
              <th scope="col" class="px-3 py-2 text-left text-xs font-weight-bold text-secondary text-uppercase">QR Code</th>
              <th scope="col" class="px-3 py-2 text-left text-xs font-weight-bold text-secondary text-uppercase">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="ticket in tickets" :key="ticket.id">
              <td class="px-3 py-2 align-middle text-sm">{{ ticket.id }}</td>
              <td class="px-3 py-2 align-middle text-sm">
                <span :class="{'badge bg-success': ticket.status === 'Paid', 'badge bg-warning text-dark': ticket.status !== 'Paid'}">
                  {{ ticket.status }}
                </span>
              </td>
              <td class="px-3 py-2 align-middle text-sm text-secondary">{{ new Date(ticket.created_at).toLocaleString() }}</td>
              <td class="px-3 py-2 align-middle">
                <qrcode-vue
                  :value="ticket.qr_code"
                  :size="80"
                  :level="'H'"
                  :fg-color="'#000000'"
                  :bg-color="'#ffffff'"
                />
              </td>
              <td class="px-3 py-2 align-middle">
                <div class="d-flex flex-nowrap">
                  <button
                    :disabled="ticket.status === 'Paid'"
                    @click="payTicket(ticket.id)"
                    :class="{'btn-secondary': ticket.status === 'Paid'}"
                    class="btn btn-success btn-sm me-2">
                    Pay
                  </button>
                  <button
                    @click="confirmDelete(ticket.id)"
                    class="btn btn-danger btn-sm">
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Payment Modal -->
  <div v-if="showPaymentModal" class="modal fade show d-block" tabindex="-1">
    <div class="modal-dialog modal-sm modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Pay for Ticket {{ ticketToPayId }}</h5>
          <button type="button" class="btn-close" @click="closePaymentModal"></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label for="phoneNumber" class="form-label">Phone Number</label>
            <input
              type="tel"
              id="phoneNumber"
              v-model="phoneNumber"
              class="form-control"
              placeholder="e.g., 0712345678"
            />
          </div>
          <div class="d-flex gap-2 mb-3">
            <button
              @click="paymentProvider = 'momo'"
              :class="{'btn-primary': paymentProvider === 'momo'}"
              class="btn btn-light w-100">
              Momo
            </button>
            <button
              @click="paymentProvider = 'tigocash'"
              :class="{'btn-primary': paymentProvider === 'tigocash'}"
              class="btn btn-light w-100">
              TigoCash
            </button>
          </div>
          <p v-if="message" :class="{'text-success': message.includes('success'), 'text-danger': !message.includes('success')}" class="text-center">
            {{ message }}
          </p>
        </div>
        <div class="modal-footer d-flex justify-content-between">
          <button
            type="button"
            class="btn btn-outline-secondary"
            @click="closePaymentModal">
            Cancel
          </button>
          <button
            type="button"
            @click="handlePayment"
            :disabled="!phoneNumber || !paymentProvider || loading"
            class="btn btn-success"
            :class="{'disabled': !phoneNumber || !paymentProvider || loading}">
            {{ loading ? 'Processing...' : 'Pay Now' }}
          </button>
        </div>
      </div>
    </div>
  </div>
  <div v-if="showPaymentModal" class="modal-backdrop fade show"></div>

  <!-- Delete Confirmation Modal -->
  <div v-if="showDeleteModal" class="modal fade show d-block" tabindex="-1">
    <div class="modal-dialog modal-sm modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Confirm Deletion</h5>
          <button type="button" class="btn-close" @click="closeDeleteModal"></button>
        </div>
        <div class="modal-body">
          <p>Do you want to delete this ticket?</p>
        </div>
        <div class="modal-footer d-flex justify-content-end">
          <button
            type="button"
            class="btn btn-outline-secondary me-2"
            @click="closeDeleteModal">
            Cancel
          </button>
          <button
            type="button"
            @click="executeDelete"
            class="btn btn-danger">
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
  <div v-if="showDeleteModal" class="modal-backdrop fade show"></div>
</template>

<script setup>
/* eslint-disable */
import axios from 'axios';
import QrcodeVue from 'qrcode.vue';
import { ref, watch } from 'vue';

const props = defineProps({
  tickets: {
    type: Array,
    required: true
  }
});

const tickets = ref([...props.tickets]);
const showPaymentModal = ref(false);
const showDeleteModal = ref(false);
const ticketToPayId = ref(null);
const ticketToDeleteId = ref(null);
const phoneNumber = ref('');
const paymentProvider = ref('');
const loading = ref(false);
const message = ref('');


watch(
  () => props.tickets,
  (newVal) => {
    tickets.value = [...newVal];
  }, { deep: true }
);

/**
 * Opens the payment modal and sets the current ticket ID.
 * @param {string} ticket_id
 */
const payTicket = (ticket_id) => {
  ticketToPayId.value = ticket_id;
  showPaymentModal.value = true;
  phoneNumber.value = '';
  paymentProvider.value = '';
  message.value = '';
};

const handlePayment = async () => {
  if (!phoneNumber.value || !paymentProvider.value) {
    message.value = 'Please enter a phone number and select a payment provider.';
    return;
  }

  loading.value = true;
  message.value = 'Processing your payment...';

  const payload = {
    ticket_id: ticketToPayId.value,
    phone_number: phoneNumber.value,
    provider: paymentProvider.value,
  };

  try {
    const token = localStorage.getItem('access_token');
    const response = await axios.post('http://127.0.0.1:8000/api/v1/payments/', payload, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (response.data) {
      message.value = response.data.detail;
      const ticketIndex = tickets.value.findIndex(t => t.id === ticketToPayId.value);
      if (ticketIndex !== -1) {
        tickets.value[ticketIndex].status = t.status;
      }
      setTimeout(() => {
        closePaymentModal();
      }, 2000);
    }
  } catch (err) {
    console.error("Payment API error", err);
    const errorMessage = err.response?.data?.detail || 'Payment failed. Please try again.';
    message.value = errorMessage;
  } finally {
    loading.value = false;
  }
};

/**
 * Opens the delete confirmation modal.
 * @param {string} ticket_id
 */
const confirmDelete = (ticket_id) => {
  ticketToDeleteId.value = ticket_id;
  showDeleteModal.value = true;
};

const executeDelete = async () => {
  try {
    const token = localStorage.getItem('access_token');
    const response = await axios.put(`http://127.0.0.1:8000/api/v1/tickets/${ticketToDeleteId.value}`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (response.data) {
      tickets.value = tickets.value.filter(t => t.id !== ticketToDeleteId.value);
    }
  } catch (err) {
    console.error("Delete ticket error", err);
  } finally {
    closeDeleteModal();
  }
};


const closePaymentModal = () => {
  showPaymentModal.value = false;
  ticketToPayId.value = null;
};


const closeDeleteModal = () => {
  showDeleteModal.value = false;
  ticketToDeleteId.value = null;
};
</script>
