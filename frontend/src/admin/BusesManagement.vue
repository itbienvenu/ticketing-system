<template>
  <div class="p-4">
    <h3 class="text-purple mb-4">Buses Management</h3>

    <div class="d-flex justify-content-between align-items-center mb-3">
      <input
        v-model="search"
        type="text"
        class="form-control me-3"
        placeholder="Search by plate number..."
      />
      <button class="btn btn-purple" @click="openAddBusModal">
        <i class="fas fa-plus-circle me-2"></i> Add New Bus
      </button>
    </div>

    <div class="table-responsive">
      <table class="table table-striped table-hover">
        <thead class="bg-purple text-white">
          <tr>
            <th>Plate Number</th>
            <th>Capacity</th>
            <th class="text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="bus in filteredBuses" :key="bus.id">
            <td>{{ bus.plate_number }}</td>
            <td>{{ bus.seats }} seats</td>
            <td class="text-center">
              <div class="btn-group">
                <button class="btn btn-sm btn-outline-purple me-1" @click="editBus(bus)">
                  <i class="fas fa-edit"></i>
                  edit
                </button>
                <button class="btn btn-sm btn-outline-danger" @click="deleteBus(bus.id)">
                  <i class="fas fa-trash-alt"></i>
                  delete
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="filteredBuses.length === 0" class="alert alert-info text-center mt-3">
      No buses found matching your search.
    </div>

    <div class="modal fade" tabindex="-1" ref="busModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-purple text-white">
            <h5 class="modal-title">{{ isEditing ? 'Edit Bus' : 'Add New Bus' }}</h5>
            <button type="button" class="btn-close btn-close-white" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveBus">
              <div class="mb-3">
                <label for="plate_number" class="form-label">Plate Number</label>
                <input type="text" class="form-control" id="plate_number" v-model="currentBus.plate_number" required>
              </div>
              <div class="mb-3">
                <label for="capacity" class="form-label">Capacity</label>
                <input type="number" class="form-control" id="capacity" v-model.number="currentBus.seats" required>
              </div>
              <div class="d-flex justify-content-end">
                <button type="button" class="btn btn-secondary me-2" @click="closeModal">Cancel</button>
                <button type="submit" class="btn btn-purple">{{ isEditing ? 'Update' : 'Save' }}</button>
              </div>
            </form>
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
  name: "BusesManagement",
  data() {
    return {
      buses: [],
      currentBus: { id: null, plate_number: "", seats: 0 },
      isEditing: false,
      search: "",
    };
  },
  computed: {
    filteredBuses() {
      if (!this.search) return this.buses;
      const searchTerm = this.search.toLowerCase();
      return this.buses.filter((bus) =>
        bus.plate_number.toLowerCase().includes(searchTerm)
      );
    },
  },
  mounted() {
    this.fetchBuses();
  },
  methods: {
    async fetchBuses() {
      try {
        const token = localStorage.getItem("access_token");
        const res = await axios.get("http://127.0.0.1:8000/api/v1/buses/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.buses = res.data;
      } catch (err) {
        console.error("Error fetching buses:", err);
      }
    },
    openAddBusModal() {
      this.isEditing = false;
      this.currentBus = { id: null, plate_number: "", seats: 0 };
      nextTick(() => {
        new bootstrap.Modal(this.$refs.busModal).show();
      });
    },
    editBus(bus) {
      this.isEditing = true;
      this.currentBus = { ...bus };
      nextTick(() => {
        new bootstrap.Modal(this.$refs.busModal).show();
      });
    },
    async saveBus() {
      try {
        const token = localStorage.getItem("access_token");
        const headers = { Authorization: `Bearer ${token}` };
        if (this.isEditing) {
          await axios.patch(`http://127.0.0.1:8000/api/v1/buses/${this.currentBus.id}`, this.currentBus, { headers });
          alert("Bus updated successfully!");
        } else {
          await axios.post("http://127.0.0.1:8000/api/v1/buses/", this.currentBus, { headers });
          alert("Bus added successfully!");
        }
        this.closeModal();
        this.fetchBuses();
      } catch (err) {
        console.error("Failed to save bus:", err);
        alert(`Error: ${err.response?.data?.detail || "Failed to save bus."}`);
      }
    },
    async deleteBus(busId) {
      if (!confirm("Are you sure you want to delete this bus?")) {
        return;
      }
      try {
        const token = localStorage.getItem("access_token");
        await axios.delete(`http://127.0.0.1:8000/api/v1/buses/${busId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        alert("Bus deleted successfully!");
        this.fetchBuses();
      } catch (err) {
        console.error("Failed to delete bus:", err);
        alert(`Error: ${err.response?.data?.detail || "Failed to delete bus."}`);
      }
    },
    closeModal() {
      const modal = bootstrap.Modal.getInstance(this.$refs.busModal);
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