<template>
  <div class="p-4">
    <h3 class="text-purple mb-4">Routes Management</h3>

    <div class="d-flex justify-content-between align-items-center mb-3">
      <input
        v-model="search"
        type="text"
        class="form-control me-3"
        placeholder="Search by origin or destination..."
      />
      <button class="btn btn-purple" @click="openAddRouteModal">
        <i class="fas fa-plus-circle me-2"></i> Add New Route
      </button>
    </div>

    <div class="table-responsive">
      <table class="table table-striped table-hover">
        <thead class="bg-purple text-white">
          <tr>
            <th>Origin</th>
            <th>Destination</th>
            <th class="text-end">Price</th>
            <th class="text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="route in paginatedRoutes" :key="route.id">
            <td>{{ route.origin }}</td>
            <td>{{ route.destination }}</td>
            <td class="text-end">{{ route.price }}</td>
            <td class="text-center">
              <div class="btn-group">
                <button class="btn btn-sm btn-outline-purple me-1" @click="editRoute(route)">
                  <i class="fas fa-edit"></i>
                  edit
                </button>
                <button class="btn btn-sm btn-outline-danger me-1" @click="deleteRoute(route.id)">
                  <i class="fas fa-trash-alt"></i>
                  delete
                </button>
                <button class="btn btn-sm btn-purple" @click="assignBus(route)">
                  <i class="fas fa-bus"></i> Assign Bus
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

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

    <div class="modal fade" tabindex="-1" ref="routeModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-purple text-white">
            <h5 class="modal-title">{{ isEditing ? 'Edit Route' : 'Add New Route' }}</h5>
            <button type="button" class="btn-close btn-close-white" @click="closeModal('routeModal')"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveRoute">
              <div class="mb-3">
                <label for="origin" class="form-label">Origin</label>
                <input type="text" class="form-control" id="origin" v-model="currentRoute.origin" required>
              </div>
              <div class="mb-3">
                <label for="destination" class="form-label">Destination</label>
                <input type="text" class="form-control" id="destination" v-model="currentRoute.destination" required>
              </div>
              <div class="mb-3">
                <label for="price" class="form-label">Price</label>
                <input type="number" class="form-control" id="price" v-model.number="currentRoute.price" required>
              </div>
              <div class="d-flex justify-content-end">
                <button type="button" class="btn btn-secondary me-2" @click="closeModal('routeModal')">Cancel</button>
                <button type="submit" class="btn btn-purple">{{ isEditing ? 'Update' : 'Save' }}</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" tabindex="-1" ref="assignBusModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-purple text-white">
            <h5 class="modal-title">Assign Bus to Route</h5>
            <button type="button" class="btn-close btn-close-white" @click="closeModal('assignBusModal')"></button>
          </div>
          <div class="modal-body">
            <h6 class="mb-3">Assigning bus to: **{{ selectedRoute.origin }}** → **{{ selectedRoute.destination }}**</h6>
            <div class="mb-3">
              <label for="busSelect" class="form-label">Select a Bus</label>
              <select id="busSelect" class="form-select" v-model="selectedBusId">
                <option value="">-- Select a bus --</option>
                <option v-for="bus in allBuses" :key="bus.id" :value="bus.id">
                  {{ bus.plate_number }} ({{ bus.seats }} seats)
                </option>
              </select>
            </div>
            <div class="d-flex justify-content-end">
              <button type="button" class="btn btn-secondary me-2" @click="closeModal('assignBusModal')">Cancel</button>
              <button class="btn btn-purple" @click="saveBusAssignment">Assign</button>
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
  name: "RoutesManagement",
  data() {
    return {
      routes: [],
      allBuses: [],
      selectedRoute: {},
      currentRoute: { id: null, origin: "", destination: "", price: 0 },
      selectedBusId: null,
      isEditing: false,
      search: "",
      currentPage: 1,
      perPage: 10,
    };
  },
  computed: {
    filteredRoutes() {
      if (!this.search) return this.routes;
      const searchTerm = this.search.toLowerCase();
      return this.routes.filter((r) =>
        r.origin.toLowerCase().includes(searchTerm) ||
        r.destination.toLowerCase().includes(searchTerm)
      );
    },
    totalPages() {
      return Math.ceil(this.filteredRoutes.length / this.perPage) || 1;
    },
    paginatedRoutes() {
      const start = (this.currentPage - 1) * this.perPage;
      return this.filteredRoutes.slice(start, start + this.perPage);
    },
  },
  mounted() {
    this.fetchRoutes();
    this.fetchAllBuses();
  },
  methods: {
    async fetchRoutes() {
      try {
        const token = localStorage.getItem("access_token");
        const res = await axios.get("http://127.0.0.1:8000/api/v1/routes/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.routes = res.data;
      } catch (err) {
        console.error("Error fetching routes:", err);
      }
    },
    async fetchAllBuses() {
      try {
        const token = localStorage.getItem("access_token");
        const res = await axios.get("http://127.0.0.1:8000/api/v1/buses/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.allBuses = res.data;
      } catch (err) {
        console.error("Error fetching all buses:", err);
      }
    },
    openAddRouteModal() {
      this.isEditing = false;
      this.currentRoute = { id: null, origin: "", destination: "", price: 0 };
      nextTick(() => {
        new bootstrap.Modal(this.$refs.routeModal).show();
      });
    },
    editRoute(route) {
      this.isEditing = true;
      this.currentRoute = { ...route };
      nextTick(() => {
        new bootstrap.Modal(this.$refs.routeModal).show();
      });
    },
    async saveRoute() {
      try {
        const token = localStorage.getItem("access_token");
        const headers = { Authorization: `Bearer ${token}` };
        if (this.isEditing) {
          await axios.put(`http://127.0.0.1:8000/api/v1/routes/${this.currentRoute.id}`, this.currentRoute, { headers });
          alert("Route updated successfully!");
        } else {
          await axios.post("http://127.0.0.1:8000/api/v1/routes/register", this.currentRoute, { headers });
          alert("Route added successfully!");
        }
        this.closeModal('routeModal');
        this.fetchRoutes();
      } catch (err) {
        console.error("Failed to save route:", err);
        alert(`Error: ${err.response?.data?.detail || "Failed to save route."}`);
      }
    },
    async deleteRoute(routeId) {
      if (!confirm("Are you sure you want to delete this route? This action cannot be undone.")) {
        return;
      }
      try {
        const token = localStorage.getItem("access_token");
        await axios.delete(`http://127.0.0.1:8000/api/v1/routes/${routeId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        alert("Route deleted successfully!");
        this.fetchRoutes();
      } catch (err) {
        console.error("Failed to delete route:", err);
        alert(`Error: ${err.response?.data?.detail || "Failed to delete route."}`);
      }
    },
    assignBus(route) {
      this.selectedRoute = route;
      this.selectedBusId = null;
      nextTick(() => {
        new bootstrap.Modal(this.$refs.assignBusModal).show();
      });
    },
    async saveBusAssignment() {
      if (!this.selectedBusId) {
        alert("Please select a bus to assign.");
        return;
      }
      try {
        const token = localStorage.getItem("access_token");
        await axios.post(`http://127.0.0.1:8000/api/v1/routes/assign-bus`, {
          route_id: this.selectedRoute.id,
          bus_id: this.selectedBusId,
        }, { headers: { Authorization: `Bearer ${token}` } });
        alert("Bus assigned successfully!");
        this.closeModal('assignBusModal');
      } catch (err) {
        console.error("Failed to assign bus:", err);
        alert(`Error: ${err.response?.data?.detail || "Failed to assign bus."}`);
      }
    },
    closeModal(modalRef) {
      const modal = bootstrap.Modal.getInstance(this.$refs[modalRef]);
      if (modal) {
        modal.hide();
      }
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
.btn-close-white {
  filter: invert(1) grayscale(100%) brightness(200%);
}
</style>