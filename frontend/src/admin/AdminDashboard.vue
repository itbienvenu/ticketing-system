<template>
  <div class="d-flex vh-100 bg-light">
    <AdminSidebar @navigate="activeTab = $event" />

    <div class="flex-grow-1 p-4">
      <HeaderBar :user="adminUser" />

      <div class="mt-4">
        <div v-if="activeTab === 'dashboard'">
          <DashboardOverview />
        </div>

        <div v-else-if="activeTab === 'routes'">
          <RoutesManagement />
        </div>

        <div v-else-if="activeTab === 'tickets'">
          <TicketsManagement />
        </div>

        <div v-else-if="activeTab === 'users'">
          <UsersManagement />
        </div>

        <div v-else-if="activeTab === 'buses'">
          <BusesManagement />
        </div>

        <div v-else>
          <p class="text-muted">Please select a section from the sidebar.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

import AdminSidebar from './AdminSidebar.vue';
import HeaderBar from './HeaderBar.vue';
import DashboardOverview from './DashboardOverview.vue';
import RoutesManagement from './RoutesManagement.vue';
import TicketsManagement from './TicketsManagement.vue';
import UsersManagement from './UsersManagement.vue';
import BusesManagement from './BusesManagement.vue';

const API_BASE = process.env.VUE_APP_API_BASE_URL;

const adminUser = ref({});
const activeTab = ref('dashboard');

const fetchAdminUser = async () => {
  try {
    const token = localStorage.getItem('access_token');
    const response = await axios.get(`${API_BASE}/me`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (response.data.role == 'admin') {
      adminUser.value = response.data;
    } else {
      console.error('Unauthorized access. User is not an admin.');
    }
  } catch (err) {
    console.error('Failed to fetch admin user', err);
  }
};

onMounted(() => {
  fetchAdminUser();
});
</script>

<style scoped>
/* Optional: If you want to use a specific purple */
:root {
  --sidebar-bg: #5D3FD3; /* A nice purple for the sidebar */
  --primary-color: #5D3FD3; /* For highlights and buttons */
}
</style>