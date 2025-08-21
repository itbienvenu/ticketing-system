<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card shadow-lg border-0 p-4" style="width: 380px; background: white; border-radius: 15px;">
      
      <!-- Title -->
      <div class="text-center mb-4">
        <h2 class="fw-bold text-primary">Ticketing System</h2>
        <p class="text-muted small">Login to access your dashboard</p>
      </div>

      <!-- Form -->
      <form @submit.prevent="login">
        <!-- Email -->
        <div class="mb-3">
          <label for="email" class="form-label fw-semibold text-dark">Email</label>
          <input
            v-model="email"
            type="email"
            id="email"
            class="form-control border-2 border-primary"
            placeholder="Enter your email"
            required
          >
        </div>

        <!-- Password -->
        <div class="mb-3">
          <label for="password" class="form-label fw-semibold text-dark">Password</label>
          <input
            v-model="password"
            type="password"
            id="password"
            class="form-control border-2 border-primary"
            placeholder="••••••••"
            required
          >
        </div>

        <!-- Remember -->
        <div class="form-check mb-3">
          <input v-model="remember" type="checkbox" class="form-check-input" id="rememberMe">
          <label class="form-check-label text-muted" for="rememberMe">Remember me</label>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          class="btn w-100 fw-bold text-white d-flex justify-content-center align-items-center"
          style="background: linear-gradient(90deg, #0d6efd, #6f42c1); border-radius: 10px;"
          :disabled="loading"
        >
          <span v-if="!loading">Login</span>
          <span v-else class="spinner-border spinner-border-sm text-white" role="status"></span>
        </button>

        <!-- Error Message -->
        <p v-if="errorMessage" class="text-danger mt-2">{{ errorMessage }}</p>
      </form>

    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import axios from "axios"
import { useRouter } from 'vue-router'

const email = ref("")
const password = ref("")
const remember = ref(false)
const errorMessage = ref("")
const loading = ref(false)

const router = useRouter()

async function login() {
  errorMessage.value = ""
  loading.value = true

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/v1/login/', {
      email: email.value,
      password: password.value
    }, {
      headers: { 'Content-Type': 'application/json' }
    })

    // console.log("Login response:", response.data)

    // Store token
    localStorage.setItem("access_token", response.data.access_token)
    localStorage.setItem("token_type", response.data.token_type)

    // Redirect to Home
    router.push('/home')

  } catch (error) {
    // console.error("Login error:", error)
    if (error.response && error.response.data) {
      // FastAPI returns 'detail' on errors
      errorMessage.value = error.response.data.detail || "An error occurred"
    } else {
      errorMessage.value = "An error occurred. Please try again."
    }

  } finally {
    loading.value = false
  }
}
</script>
