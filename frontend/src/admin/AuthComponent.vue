<template>
  <div class="p-4">
    <h3 class="text-purple mb-4">Authentication & Role Management</h3>

    <div class="row">
      <div class="col-md-6 mb-4">
        <div class="card shadow-sm h-100">
          <div class="card-header bg-purple text-white">
            <h5 class="card-title mb-0">Role Management</h5>
          </div>
          <div class="card-body">
            <div class="d-flex justify-content-between mb-3">
              <span class="fw-bold">Available Roles</span>
              <button class="btn btn-sm btn-purple" @click="openModal('role')">
                <i class="fas fa-plus-circle me-1"></i> New Role
              </button>
            </div>
            
            <input
              v-model="roleSearch"
              type="text"
              class="form-control form-control-sm mb-3"
              placeholder="Search roles..."
            />

            <div class="table-responsive">
              <table class="table table-striped table-sm">
                <thead>
                  <tr>
                    <th>Role Name</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="role in paginatedRoles" :key="role.id">
                    <td>{{ role.name }}</td>
                    <td>
                      <button class="btn btn-sm btn-outline-danger" @click="deleteRole(role.id)">
                        <i class="fas fa-trash-alt"></i>
                      </button>
                    </td>
                  </tr>
                  <tr v-if="paginatedRoles.length === 0">
                    <td colspan="2" class="text-center text-muted">No roles found.</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="d-flex justify-content-between align-items-center">
              <button
                class="btn btn-sm btn-outline-secondary"
                :disabled="roleCurrentPage === 1"
                @click="roleCurrentPage--"
              >
                Previous
              </button>
              <span class="text-muted">Page {{ roleCurrentPage }} of {{ roleTotalPages }}</span>
              <button
                class="btn btn-sm btn-outline-secondary"
                :disabled="roleCurrentPage === roleTotalPages"
                @click="roleCurrentPage++"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-6 mb-4">
        <div class="row h-100">
          <div class="col-12 mb-4">
            <div class="card shadow-sm h-100">
              <div class="card-header bg-purple text-white">
                <h5 class="card-title mb-0">Permission Management</h5>
              </div>
              <div class="card-body">
                <div class="d-flex justify-content-between mb-3">
                  <span class="fw-bold">Available Permissions</span>
                  <button class="btn btn-sm btn-purple" @click="openModal('permission')">
                    <i class="fas fa-plus-circle me-1"></i> New Permission
                  </button>
                </div>

                <input
                  v-model="permissionSearch"
                  type="text"
                  class="form-control form-control-sm mb-3"
                  placeholder="Search permissions..."
                />
                
                <div class="table-responsive">
                  <table class="table table-striped table-sm">
                    <thead>
                      <tr>
                        <th>Permission Name</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="permission in paginatedPermissions" :key="permission.id">
                        <td>{{ permission.name }}</td>
                        <td>
                          <button class="btn btn-sm btn-outline-danger" @click="deletePermission(permission.id)">
                            <i class="fas fa-trash-alt"></i>
                          </button>
                        </td>
                      </tr>
                      <tr v-if="paginatedPermissions.length === 0">
                        <td colspan="2" class="text-center text-muted">No permissions found.</td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                <div class="d-flex justify-content-between align-items-center">
                  <button
                    class="btn btn-sm btn-outline-secondary"
                    :disabled="permissionCurrentPage === 1"
                    @click="permissionCurrentPage--"
                  >
                    Previous
                  </button>
                  <span class="text-muted">Page {{ permissionCurrentPage }} of {{ permissionTotalPages }}</span>
                  <button
                    class="btn btn-sm btn-outline-secondary"
                    :disabled="permissionCurrentPage === permissionTotalPages"
                    @click="permissionCurrentPage++"
                  >
                    Next
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="col-12">
            <div class="card shadow-sm h-100">
              <div class="card-header bg-purple text-white">
                <h5 class="card-title mb-0">My Permissions</h5>
              </div>
              <div class="card-body">
                <ul class="list-group list-group-flush">
                  <li v-if="paginatedMyPermissions.length === 0" class="list-group-item text-muted text-center">
                    No permissions found for your account.
                  </li>
                  <li v-for="permission in paginatedMyPermissions" :key="permission.id" class="list-group-item">
                    <i class="fas fa-check-circle text-success me-2"></i> {{ permission.name }}
                  </li>
                </ul>
              </div>

              <div class="card-footer d-flex justify-content-between align-items-center bg-white border-top">
                <button
                  class="btn btn-sm btn-outline-secondary"
                  :disabled="myPermissionsCurrentPage === 1"
                  @click="myPermissionsCurrentPage--"
                >
                  Previous
                </button>
                <span class="text-muted">Page {{ myPermissionsCurrentPage }} of {{ myPermissionsTotalPages }}</span>
                <button
                  class="btn btn-sm btn-outline-secondary"
                  :disabled="myPermissionsCurrentPage === myPermissionsTotalPages"
                  @click="myPermissionsCurrentPage++"
                >
                  Next
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="card shadow-sm mt-4">
      <div class="card-header bg-purple text-white">
        <h5 class="card-title mb-0">Assign Permissions to Role</h5>
      </div>
      <div class="card-body">
        <form @submit.prevent="assignPermissionsToRole">
          <div class="mb-3">
            <label for="roleSelect" class="form-label">Select Role</label>
            <select class="form-select" id="roleSelect" v-model="selectedRoleId" required>
              <option value="">-- Choose a Role --</option>
              <option v-for="role in allRoles" :key="role.id" :value="role.id">{{ role.name }}</option>
            </select>
          </div>
          <div class="mb-3">
            <label for="permissionSelect" class="form-label">Select Permission</label>
            <select class="form-select" id="permissionSelect" v-model="selectedPermissionId" required>
              <option value="">-- Choose a Permission --</option>
              <option v-for="permission in allPermissions" :key="permission.id" :value="permission.id">{{ permission.name }}</option>
            </select>
          </div>
          <button type="submit" class="btn btn-purple" :disabled="!selectedRoleId || !selectedPermissionId">
            Assign Permission
          </button>
        </form>
      </div>
    </div>

    <div class="modal fade" tabindex="-1" ref="roleModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-purple text-white">
            <h5 class="modal-title">Create New Role</h5>
            <button type="button" class="btn-close btn-close-white" @click="closeModal('roleModal')"></button>
          </div>
          <form @submit.prevent="createRole">
            <div class="modal-body">
              <div class="mb-3">
                <label for="newRoleName" class="form-label">Role Name</label>
                <input type="text" class="form-control" id="newRoleName" v-model="newRoleName" required>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal('roleModal')">Cancel</button>
              <button type="submit" class="btn btn-purple">Create Role</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div class="modal fade" tabindex="-1" ref="permissionModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-purple text-white">
            <h5 class="modal-title">Create New Permission</h5>
            <button type="button" class="btn-close btn-close-white" @click="closeModal('permissionModal')"></button>
          </div>
          <form @submit.prevent="createPermission">
            <div class="modal-body">
              <div class="mb-3">
                <label for="newPermissionName" class="form-label">Permission Name</label>
                <input type="text" class="form-control" id="newPermissionName" v-model="newPermissionName" required>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal('permissionModal')">Cancel</button>
              <button type="submit" class="btn btn-purple">Create Permission</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, computed, watch } from 'vue';
import axios from 'axios';
import * as bootstrap from 'bootstrap';

const API_BASE = process.env.VUE_APP_API_BASE_URL;
const itemsPerPage = 5;

// State variables for data
const allRoles = ref([]);
const allPermissions = ref([]);
const myPermissions = ref([]);

// State for forms and modals
const newRoleName = ref('');
const newPermissionName = ref('');
const selectedRoleId = ref('');
const selectedPermissionId = ref('');

const roleModal = ref(null);
const permissionModal = ref(null);

// State for role table pagination and search
const roleSearch = ref('');
const roleCurrentPage = ref(1);

// State for permission table pagination and search
const permissionSearch = ref('');
const permissionCurrentPage = ref(1);

// State for 'My Permissions' box pagination
const myPermissionsCurrentPage = ref(1);

const getToken = () => localStorage.getItem('access_token');

// Computed properties for Role table
const filteredRoles = computed(() => {
  if (!roleSearch.value) return allRoles.value;
  const searchTerm = roleSearch.value.toLowerCase();
  return allRoles.value.filter(role => role.name.toLowerCase().includes(searchTerm));
});

const roleTotalPages = computed(() => {
  return Math.ceil(filteredRoles.value.length / itemsPerPage) || 1;
});

const paginatedRoles = computed(() => {
  const start = (roleCurrentPage.value - 1) * itemsPerPage;
  return filteredRoles.value.slice(start, start + itemsPerPage);
});

// Watcher to reset page on search change
watch(roleSearch, () => {
  roleCurrentPage.value = 1;
});

// Computed properties for Permission table
const filteredPermissions = computed(() => {
  if (!permissionSearch.value) return allPermissions.value;
  const searchTerm = permissionSearch.value.toLowerCase();
  return allPermissions.value.filter(permission => permission.name.toLowerCase().includes(searchTerm));
});

const permissionTotalPages = computed(() => {
  return Math.ceil(filteredPermissions.value.length / itemsPerPage) || 1;
});

const paginatedPermissions = computed(() => {
  const start = (permissionCurrentPage.value - 1) * itemsPerPage;
  return filteredPermissions.value.slice(start, start + itemsPerPage);
});

// Watcher to reset page on search change
watch(permissionSearch, () => {
  permissionCurrentPage.value = 1;
});

// Computed properties for 'My Permissions'
const myPermissionsTotalPages = computed(() => {
  return Math.ceil(myPermissions.value.length / itemsPerPage) || 1;
});

const paginatedMyPermissions = computed(() => {
  const start = (myPermissionsCurrentPage.value - 1) * itemsPerPage;
  return myPermissions.value.slice(start, start + itemsPerPage);
});


const fetchAllRoles = async () => {
  try {
    const token = getToken();
    const response = await axios.get(`${API_BASE}/auth/all_roles`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    allRoles.value = response.data;
  } catch (err) {
    console.error('Failed to fetch roles:', err);
  }
};

const fetchAllPermissions = async () => {
  try {
    const token = getToken();
    const response = await axios.get(`${API_BASE}/auth/get_permissions`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    allPermissions.value = response.data;
  } catch (err) {
    console.error('Failed to fetch permissions:', err);
  }
};

const fetchMyPermissions = async () => {
  try {
    const token = getToken();
    const response = await axios.get(`${API_BASE}/auth/my_permissions`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    myPermissions.value = response.data.permissions;
  } catch (err) {
    console.error('Failed to fetch my permissions:', err);
  }
};

const createRole = async () => {
  try {
    const token = getToken();
    await axios.post(
      `${API_BASE}/auth/create_role`,
      { name: newRoleName.value },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    alert('Role created successfully!');
    closeModal('roleModal');
    newRoleName.value = '';
    fetchAllRoles();
  } catch (err) {
    console.error('Failed to create role:', err);
    alert(`Error: ${err.response?.data?.detail || "Failed to create role."}`);
  }
};

const createPermission = async () => {
  try {
    const token = getToken();
    await axios.post(
      `${API_BASE}/auth/create_permission`,
      { name: newPermissionName.value },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    alert('Permission created successfully!');
    closeModal('permissionModal');
    newPermissionName.value = '';
    fetchAllPermissions();
  } catch (err) {
    console.error('Failed to create permission:', err);
    alert(`Error: ${err.response?.data?.detail || "Failed to create permission."}`);
  }
};

const assignPermissionsToRole = async () => {
  try {
    const token = getToken();
    await axios.post(
      `${API_BASE}/auth/assign_permissions`,
      { role_id: selectedRoleId.value, permission_id: selectedPermissionId.value },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    alert('Permission assigned successfully!');
    selectedRoleId.value = '';
    selectedPermissionId.value = '';
    fetchMyPermissions(); // Refresh my permissions after assignment
  } catch (err) {
    console.error('Failed to assign permission:', err);
    alert(`Error: ${err.response?.data?.detail || "Failed to assign permission."}`);
  }
};

const deleteRole = async (roleId) => {
  if (confirm('Are you sure you want to delete this role?')) {
    try {
      const token = getToken();
      await axios.delete(
        `${API_BASE}/auth/delete_role/${roleId}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('Role deleted successfully!');
      fetchAllRoles();
    } catch (err) {
      console.error('Failed to delete role:', err);
      alert(`Error: ${err.response?.data?.detail || "Failed to delete role."}`);
    }
  }
};

const deletePermission = async (permissionId) => {
  if (confirm('Are you sure you want to delete this permission?')) {
    try {
      const token = getToken();
      await axios.delete(
        `${API_BASE}/auth/delete_permission/${permissionId}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('Permission deleted successfully!');
      fetchAllPermissions();
    } catch (err) {
      console.error('Failed to delete permission:', err);
      alert(`Error: ${err.response?.data?.detail || "Failed to delete permission."}`);
    }
  }
};

const openModal = (type) => {
  nextTick(() => {
    if (type === 'role') {
      new bootstrap.Modal(roleModal.value).show();
    } else if (type === 'permission') {
      new bootstrap.Modal(permissionModal.value).show();
    }
  });
};

const closeModal = (modalRef) => {
  const modal = bootstrap.Modal.getInstance(modalRef === 'roleModal' ? roleModal.value : permissionModal.value);
  if (modal) {
    modal.hide();
  }
};

onMounted(() => {
  fetchAllRoles();
  fetchAllPermissions();
  fetchMyPermissions();
});
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