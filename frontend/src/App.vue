<script setup>
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';
</script>

<template>
  <div id="app-container">
    <Navbar />
    <main class="main-content">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<style scoped>
#app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 1rem;
}

/* Keep existing styles if they are still relevant, or remove/modify as needed */
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  /* Adjust layout for larger screens if necessary */
  /* For example, you might want to ensure the main content area is well-defined */
  .main-content {
    /* max-width: 1200px; /* Example: limit content width */
    /* margin: 0 auto; /* Example: center content */
  }
}
</style>