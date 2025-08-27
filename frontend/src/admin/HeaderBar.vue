<template>
  <div class="d-flex justify-content-between align-items-center">
    <h2 class="text-primary">Welcome, {{ user.full_name || user.email }}</h2>
    <button class="btn btn-outline-secondary" @click="logout">Logout</button>
  </div>
</template>

<script setup>
/* eslint-disable */
import { defineProps } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({ user: Object })
const router = useRouter()

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('token_type')
  router.push('/')
}
</script>
