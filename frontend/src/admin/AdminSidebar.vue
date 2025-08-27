<template>
  <div class="sidebar bg-purple text-white p-4 d-flex flex-column" style="width: 250px;">
    <h4>Admin Panel ⚙️</h4>
    <ul class="nav flex-column mt-4">
      <li class="nav-item">
        <a href="#" class="nav-link text-white" @click.prevent="$emit('navigate', 'dashboard')">
          <i class="fas fa-chart-line me-2"></i> Dashboard
        </a>
      </li>
      <li class="nav-item">
        <a href="#" class="nav-link text-white" @click.prevent="$emit('navigate', 'routes')">
          <i class="fas fa-road me-2"></i> Routes
        </a>
      </li>
      <li class="nav-item">
        <a href="#" class="nav-link text-white" @click.prevent="$emit('navigate', 'tickets')">
          <i class="fas fa-ticket-alt me-2"></i> Tickets
        </a>
      </li>
      <li class="nav-item">
        <a href="#" class="nav-link text-white" @click.prevent="$emit('navigate', 'users')">
          <i class="fas fa-users me-2"></i> Users
        </a>
      </li>
      <li class="nav-item">
        <a href="#" class="nav-link text-white" @click.prevent="$emit('navigate', 'buses')">
          <i class="fas fa-bus me-2"></i> Buses
        </a>
      </li>
    </ul>
  </div>
</template>

<script setup>

</script>

<style scoped>
.sidebar {
  background-color: #5D3FD3; 
  transition: background-color 0.3s ease;
}

.nav-link {
  border-radius: 5px;
  margin-bottom: 5px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.nav-link:hover {
  background-color: #7A5AC9; 
  transform: translateX(5px); 
}
</style>