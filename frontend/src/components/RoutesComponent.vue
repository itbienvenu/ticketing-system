<template>
  <div class="p-4">
    <h3>Available Routes</h3>
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
        <tr v-for="route in routes" :key="route.id">
          <td style="text-align: left;">{{ route.origin }}</td>
          <td style="text-align: left;">{{ route.destination }}</td>
          <td class="text-end">{{ route.price }}</td>
          <td>
            <button class="btn btn-primary btn-sm" @click="openBusModal(route)">
              Book
            </button>
          </td>
        </tr>
      </tbody>
    </table>

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
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import axios from "axios";
import { nextTick} from "vue";
import * as bootstrap from 'bootstrap';


export default {
  name: "RoutesComponent",
  data() {
    return {
      routes: [],
      buses: [],
      selectedRoute: {},
    };
  },
  computed: {
    filteredBuses() {
      // For now, show only buses whose route_id matches selectedRoute.id
      // return this.buses.filter((b) => b.route_id === this.selectedRoute.id);
      return this.buses;
    },
  },
  mounted() {
    const token = localStorage.getItem("access_token");

    // Fetch routes
    axios
      .get("http://127.0.0.1:8000/api/v1/routes", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => (this.routes = res.data))
      .catch((err) => console.error("Error fetching routes:", err));

    // Fetch all buses (later filtered by route)
    axios
      .get("http://127.0.0.1:8000/api/v1/buses", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => (this.buses = res.data))
      .catch((err) => console.error("Error fetching buses:", err));
  },
  methods: {
    async openBusModal(route) {
      this.selectedRoute = route;
      await nextTick();
      const modal = new bootstrap.Modal(this.$refs.busModal);
      modal.show();
    },
    closeModal() {
      const modal = bootstrap.Modal.getInstance(this.$refs.busModal);
      modal.hide();
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
        alert("Error booking ticket!");
      }
    },
  },
};
</script>

<style scoped>
/* optional styling for modal or table */
</style>
