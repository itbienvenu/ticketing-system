<template>
  <div class="p-4">
    <h3>Available Routes</h3>

    <!-- Search box -->
    <input
      v-model="search"
      type="text"
      class="form-control mb-3"
      placeholder="Search by origin or destination..."
    />

    <!-- Routes Table -->
    <table border="1" cellpadding="8" cellspacing="0" width="100%">
      <thead>
        <tr>
          <th>Origin</th>
          <th>Destination</th>
          <th>Price</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="route in paginatedRoutes" :key="route.id">
          <td style="text-align: left;">{{ route.origin }}</td>
          <td style="text-align: left;">{{ route.destination }}</td>
          <td class="text-end">{{ route.price }}</td>
          <td>
            <button class="btn btn-primary btn-sm" @click="openBusModal(route.id)">
              Book
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination controls -->
    <div class="mt-3 d-flex justify-content-between align-items-center">
      <button
        class="btn btn-secondary btn-sm"
        :disabled="currentPage === 1"
        @click="currentPage--"
      >
        Previous
      </button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button
        class="btn btn-secondary btn-sm"
        :disabled="currentPage === totalPages"
        @click="currentPage++"
      >
        Next
      </button>
    </div>

    <!-- Bus Selection Modal -->
    <div class="modal fade" tabindex="-1" ref="busModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              Select a Bus for {{ selectedRoute.origin }} → {{ selectedRoute.destination }}
            </h5>
            <button type="button" class="btn-close" @click="closeModal()"></button>
          </div>
          <div class="modal-body">
            <ul class="list-group">
              <li
                v-for="bus in filteredBuses"
                :key="bus.id"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                {{ bus.plate_number }}
                <button class="btn btn-success btn-sm" @click="bookTicket(bus)">Select</button>
              </li>
            </ul>
            <div v-if="filteredBuses.length === 0" class="text-center mt-2">
              No buses available for this route.
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { nextTick } from "vue";
import * as bootstrap from "bootstrap";

export default {
  name: "RoutesComponent",
  data() {
    return {
      routes: [],
      buses: [],
      selectedRoute: {},
      search: "",
      currentPage: 1,
      perPage: 10,
    };
  },
  computed: {
    // Filter routes by search
    filteredRoutes() {
      return this.routes.filter((r) =>
        `${r.origin} ${r.destination}`.toLowerCase().includes(this.search.toLowerCase())
      );
    },
    // Calculate total pages
    totalPages() {
      return Math.ceil(this.filteredRoutes.length / this.perPage) || 1;
    },
    // Slice filtered routes for current page
    paginatedRoutes() {
      const start = (this.currentPage - 1) * this.perPage;
      return this.filteredRoutes.slice(start, start + this.perPage);
    },
    // Show buses fetched for selected route
    filteredBuses() {
      return this.buses;
    },
  },
  mounted() {
    const token = localStorage.getItem("access_token");

    // Fetch all routes
    axios
      .get("http://127.0.0.1:8000/api/v1/routes/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => (this.routes = res.data))
      .catch((err) => console.error("Error fetching routes:", err));
  },
  methods: {
    async openBusModal(route_id) {
      // Find the selected route
      const route = this.routes.find((r) => r.id === route_id);
      this.selectedRoute = route;

      // Fetch buses for this route only
      const token = localStorage.getItem("access_token");
      try {
        const res = await axios.get(`http://127.0.0.1:8000/api/v1/buses/by-route/${route_id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.buses = res.data;
      } catch (err) {
        console.error("Error fetching buses for route:", err);
        this.buses = [];
      }

      // Show modal
      await nextTick();
      const modal = new bootstrap.Modal(this.$refs.busModal);
      modal.show();
    },

    closeModal() {
      const modal = bootstrap.Modal.getInstance(this.$refs.busModal);
      modal.hide();
      this.buses = [];
    },

    async bookTicket(bus) {
      try {
        const token = localStorage.getItem("access_token");
        const userRes = await axios.get("http://127.0.0.1:8000/api/v1/me", {
          headers: { Authorization: `Bearer ${token}` },
        });
        const payload = {
          user_id: userRes.data.id,
          bus_id: bus.id,
          route_id: this.selectedRoute.id,
        };
        await axios.post("http://127.0.0.1:8000/api/v1/tickets", payload, {
          headers: { Authorization: `Bearer ${token}` },
        });
        alert("Ticket booked successfully!");
        this.closeModal();
      } catch (err) {
        console.error("Failed to book ticket:", err);

  // Show backend error detail if available
  const message = err.response?.data?.detail || "Error booking ticket!";
  alert(message);
      }
    },
  },
};
</script>

<style scoped>
/* Optional styling for modal or table */
</style>
