<template>
  <nav class="navbar">
    <div class="container navbar-container">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-logo">
          <span class="logo-text">物業管理系統</span>
        </router-link>
      </div>
      <div class="navbar-menu">
        <div class="navbar-start">
          <router-link to="/" class="navbar-item">首頁</router-link>
          <router-link to="/residents" class="navbar-item">住戶管理</router-link>
          <router-link to="/properties" class="navbar-item">物件管理</router-link>
          <router-link to="/payments" class="navbar-item">繳費管理</router-link>
          <router-link to="/potential-customers" class="navbar-item">潛在客戶</router-link>
          <router-link to="/maintenance" class="navbar-item">維修管理</router-link>
          <router-link to="/announcements" class="navbar-item">公告管理</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
</script>

<style scoped>
.navbar {
  background-color: var(--primary-color);
  padding: var(--spacing-sm) 0;
  box-shadow: var(--shadow);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand {
  display: flex;
  align-items: center;
}

.navbar-logo {
  display: flex;
  align-items: center;
  text-decoration: none;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  margin-left: var(--spacing-sm);
}

.navbar-menu {
  display: flex;
}

.navbar-start {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.navbar-item {
  padding: var(--spacing-sm) var(--spacing-md);
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  transition: var(--transition);
  border-radius: var(--border-radius);
  margin: 0 2px;
}

.navbar-item:hover,
.navbar-item.router-link-exact-active {
  background-color: rgba(255, 255, 255, 0.15);
  color: white;
}

/* 響應式設計 */
@media (max-width: 768px) {
  .navbar-container {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .navbar-start {
    margin-top: var(--spacing-sm);
    flex-wrap: wrap;
  }
  
  .navbar-item {
    padding: var(--spacing-xs) var(--spacing-sm);
    margin: 2px;
  }
}
</style>