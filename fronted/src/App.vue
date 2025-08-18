<template>
  <div id="app">
    <div style="display: flex; justify-content: center; gap: 40px; margin-top: 40px;">
      <LoginView />
      <RegisterView />
    </div>
  </div>
</template>

<script>
import LoginView from './router/views/LoginView.vue'
import RegisterView from './router/views/RegisterView.vue'

export default {
  name: 'App',
  components: {
    LoginView,
    RegisterView
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0;
}
</style>
