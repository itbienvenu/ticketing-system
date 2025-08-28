<template>
  <div class="p-4">
    <h3 class="text-purple mb-4">Tickets Management</h3>

    <div class="mb-3">
      <input
        v-model="search"
        type="text"
        class="form-control"
        placeholder="Search tickets by user, route, or status..."
      />
    </div>

    <div class="table-responsive">
      <table class="table table-striped table-hover">
        <thead class="bg-purple text-white">
          <tr>
            <th>Ticket ID</th>
            <th>User</th>
            <th>Route</th>
            <th>Bus</th>
            <th>Status</th>
            <th>Created At</th>
            <th class="text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ticket in filteredTickets" :key="ticket.id">
            <td>{{ ticket.id }}</td>
            <td>{{ ticket.user.name }}</td>
            <td>{{ ticket.route.origin }} → {{ ticket.route.destination }}</td>
            <td>{{ ticket.bus.plate_number }}</td>
            <td>
              <span :class="getStatusBadge(ticket.status)">{{ ticket.status }}</span>
            </td>
            <td>{{ formatDate(ticket.created_at) }}</td>
            <td class="text-center">
              <div class="btn-group">
                <button
                  class="btn btn-sm btn-outline-purple me-1"
                  @click="updateTicketStatus(ticket)"
                >
                  <i class="fas fa-sync-alt"></i> Update Status
                </button>
                <button class="btn btn-sm btn-outline-danger" @click="deleteTicket(ticket.id)">
                  <i class="fas fa-trash-alt"></i> Delete
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="filteredTickets.length === 0" class="alert alert-info text-center mt-3">
      No tickets found matching your search.
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "TicketsManagement",
  data() {
    return {
      tickets: [],
      search: '',
    };
  },
  computed: {
    filteredTickets() {
      if (!this.search) return this.tickets;
      const searchTerm = this.search.toLowerCase();
      return this.tickets.filter(ticket =>
        ticket.user.name.toLowerCase().includes(searchTerm) ||
        ticket.route.origin.toLowerCase().includes(searchTerm) ||
        ticket.route.destination.toLowerCase().includes(searchTerm) ||
        ticket.status.toLowerCase().includes(searchTerm)
      );
    },
  },
  mounted() {
    this.fetchTickets();
  },
  methods: {
    async fetchTickets() {
      try {
        const token = localStorage.getItem('access_token');
        const res = await axios.get('http://127.0.0.1:8000/api/v1/tickets', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.tickets = res.data;
      } catch (err) {
        console.error('Error fetching tickets:', err);
      }
    },
    async updateTicketStatus(ticket) {
      const newStatus = prompt(`Current status is "${ticket.status}". Enter new status (e.g., booked, used, canceled):`);
      if (newStatus && newStatus !== ticket.status) {
        try {
          const token = localStorage.getItem('access_token');
          await axios.put(`http://127.0.0.1:8000/api/v1/tickets/${ticket.id}`, { status: newStatus }, {
            headers: { Authorization: `Bearer ${token}` }
          });
          alert('Ticket status updated successfully!');
          this.fetchTickets();
        } catch (err) {
          console.error('Failed to update ticket status:', err);
          alert(`Error: ${err.response?.data?.detail || "Failed to update ticket."}`);
        }
      }
    },
    async deleteTicket(ticketId) {
      if (confirm('Are you sure you want to delete this ticket? This action is permanent.')) {
        try {
          const token = localStorage.getItem('access_token');
          await axios.delete(`http://127.0.0.1:8000/api/v1/tickets/${ticketId}`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          alert('Ticket deleted successfully!');
          this.fetchTickets();
        } catch (err) {
          console.error('Failed to delete ticket:', err);
          alert(`Error: ${err.response?.data?.detail || "Failed to delete ticket."}`);
        }
      }
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    getStatusBadge(status) {
      const statusMap = {
        'booked': 'badge bg-success',
        'used': 'badge bg-primary',
        'canceled': 'badge bg-danger',
        'pending': 'badge bg-warning text-dark',
      };
      return statusMap[status.toLowerCase()] || 'badge bg-secondary';
    },
  },
};
</script>

<style scoped>
.text-purple {
  color: #5D3FD3;
}
.bg-purple {
  background-color: #5D3FD3 !important;
}
.btn-purple {
  background-color: #5D3FD3;
  color: white;
  border-color: #5D3FD3;
}
.btn-purple:hover {
  background-color: #7A5AC9;
  border-color: #7A5AC9;
}
.btn-outline-purple {
  color: #5D3FD3;
  border-color: #5D3FD3;
}
.btn-outline-purple:hover {
  background-color: #5D3FD3;
  color: white;
}
.badge {
  text-transform: capitalize;
}
</style>