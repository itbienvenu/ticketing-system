<template>
  <div class="p-4">
    <h3 class="text-purple mb-4">Users Management</h3>

    <!-- Actions and Search -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <input
        v-model="search"
        type="text"
        class="form-control me-3"
        placeholder="Search by name or email..."
      />
      <button class="btn btn-purple" @click="openAddUserModal">
        <i class="fas fa-plus-circle me-2"></i> Add New User
      </button>
    </div>

    <!-- Users Table -->
    <div class="table-responsive">
      <table class="table table-striped table-hover">
        <thead class="bg-purple text-white">
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th class="text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td>
              <span>{{
                showFull[user.id] ? user.id : user.id.slice(0, 5) + "..."
              }}</span>
              <button
                @click="toggleShow(user.id)"
                class="btn btn-sm btn-outline-secondary"
              >
                <i
                  :class="showFull[user.id] ? 'fas fa-eye-slash' : 'fas fa-eye'"
                ></i>
              </button>
            </td>

            <td>{{ user.full_name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
            <td class="text-center">
              <div class="btn-group">
                <button
                  class="btn btn-sm btn-outline-purple me-1"
                  @click="editUser(user)"
                >
                  <i class="fas fa-edit"></i>
                </button>
                <button
                  class="btn btn-sm btn-outline-danger"
                  @click="deleteUser(user.id)"
                >
                  <i class="fas fa-trash-alt"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- No users found message -->
    <div
      v-if="filteredUsers.length === 0"
      class="alert alert-info text-center mt-3"
    >
      No users found matching your search.
    </div>

    <!-- Add/Edit User Modal -->
    <div class="modal fade" tabindex="-1" ref="userModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-purple text-white">
            <h5 class="modal-title">
              {{ isEditing ? "Edit User" : "Add New User" }}
            </h5>
            <button
              type="button"
              class="btn-close btn-close-white"
              @click="closeModal"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveUser">
              <div class="mb-3">
                <label for="name" class="form-label">Full Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="name"
                  v-model="currentUser.full_name"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="email" class="form-label">Email Address</label>
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  v-model="currentUser.email"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="email" class="form-label">Phone Number</label>
                <input
                  type="text"
                  class="form-control"
                  id="phone"
                  v-model="currentUser.phone_number"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="password"
                  v-model="currentUser.password"
                  :required="!isEditing"
                />
                <small v-if="isEditing" class="text-muted"
                  >Leave blank to keep current password.</small
                >
              </div>
              <div class="mb-3">
                <label for="email" class="form-label">Role</label>
                <input
                  type="text"
                  class="form-control"
                  id="role"
                  v-model="currentUser.role"
                  required
                />
              </div>
              <div class="d-flex justify-content-end">
                <button
                  type="button"
                  class="btn btn-secondary me-2"
                  @click="closeModal"
                >
                  Cancel
                </button>
                <button type="submit" class="btn btn-purple">
                  {{ isEditing ? "Update" : "Save" }}
                </button>
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
const API_BASE = process.env.VUE_APP_API_BASE_URL;

export default {
  name: "UsersManagement",
  data() {
    return {
      users: [],
      currentUser: {
        id: null,
        full_name: "",
        email: "",
        phone_number: "",
        password: "",
        role: "",
      },
      isEditing: false,
      search: "",
      showFull: {},
    };
  },
  computed: {
    filteredUsers() {
      if (!this.search) return this.users;
      const searchTerm = this.search.toLowerCase();
      return this.users.filter(
        (user) =>
          user.full_name.toLowerCase().includes(searchTerm) ||
          user.email.toLowerCase().includes(searchTerm)
      );
    },
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    toggleShow(id) {
      this.showFull[id] = !this.showFull[id];
    },
    async fetchUsers() {
      try {
        const token = localStorage.getItem("access_token");
        const res = await axios.get(`${API_BASE}/users`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.users = res.data;
      } catch (err) {
        console.error("Error fetching users:", err);
      }
    },
    openAddUserModal() {
      this.isEditing = false;
      this.currentUser = {
        id: null,
        full_name: "",
        email: "",
        phone_number: "",
        password: "",
        role: "",
      };
      nextTick(() => {
        new bootstrap.Modal(this.$refs.userModal).show();
      });
    },
    editUser(user) {
      this.isEditing = true;
      this.currentUser = { ...user, password: "" }; 
      nextTick(() => {
        new bootstrap.Modal(this.$refs.userModal).show();
      });
    },
    async saveUser() {
      try {
        const token = localStorage.getItem("access_token");
        const headers = { Authorization: `Bearer ${token}` };
        const payload = {
          full_name: this.currentUser.full_name,
          email: this.currentUser.email,
          phone_number: this.currentUser.phone_number,
          role: this.currentUser.role,
        };
        // Only include password if it's a new user or a password has been entered
        if (this.currentUser.password) {
          payload.password = this.currentUser.password;
        }

        if (this.isEditing) {
          await axios.patch(`${API_BASE}/users/${this.currentUser.id}`, payload, {
            headers,
          });
          console.log(payload)
          alert("User updated successfully!");
        } else {
          await axios.post(
            `${API_BASE}/register`,
            { ...payload, password: this.currentUser.password },
            { headers }
          );
          alert("User added successfully!");
        }
        this.closeModal();
        this.fetchUsers();
      } catch (err) {
        console.error("Failed to save user:", err);
        alert(`Error: ${err.response?.data?.detail || "Failed to save user."}`);
      }
    },
    async deleteUser(userId) {
      if (
        !confirm(
          "Are you sure you want to delete this user? This action is permanent."
        )
      ) {
        return;
      }
      try {
        const token = localStorage.getItem("access_token");
        await axios.delete(`${API_BASE}/users/${userId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        alert("User deleted successfully!");
        this.fetchUsers();
      } catch (err) {
        console.error("Failed to delete user:", err);
        alert(
          `Error: ${err.response?.data?.detail || "Failed to delete user."}`
        );
      }
    },
    closeModal() {
      const modal = bootstrap.Modal.getInstance(this.$refs.userModal);
      if (modal) {
        modal.hide();
      }
    },
  },
};
</script>

<style scoped>
td {
  text-align: left;
}
.text-purple {
  color: #5d3fd3;
}
.bg-purple {
  background-color: #5d3fd3 !important;
}
.btn-purple {
  background-color: #5d3fd3;
  color: white;
  border-color: #5d3fd3;
}
.btn-purple:hover {
  background-color: #7a5ac9;
  border-color: #7a5ac9;
}
.btn-outline-purple {
  color: #5d3fd3;
  border-color: #5d3fd3;
}
.btn-outline-purple:hover {
  background-color: #5d3fd3;
  color: white;
}
.btn-close-white {
  filter: invert(1) grayscale(100%) brightness(200%);
}
</style>