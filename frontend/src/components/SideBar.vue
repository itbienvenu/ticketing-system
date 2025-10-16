const API_BASE = process.env.VUE_APP_API_BASE_URL;
<template>
  <div class="bg-primary text-white p-3" style="width: 220px; min-height: 100vh;">
    <h4 class="text-center mb-4" style="color: #fff;">Ticketing</h4>
    <ul class="nav flex-column">
      <li class="nav-item mb-2">
        <a class="nav-link text-white" href="#">Dashboard</a>
      </li>
      <li class="nav-item mb-2">
        <router-link class="nav-link text-white" to="/routes">Routes</router-link>
      </li>
      <li class="nav-item mb-2">
        <a class="nav-link text-white" href="#">Settings</a>
      </li>
    </ul>
  </div>
</template>
