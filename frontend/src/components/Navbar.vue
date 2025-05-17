<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <router-link to="/" class="navbar-item brand-text">物業管理系統</router-link>
    </div>
    <div class="navbar-menu">
      <div class="navbar-start">
        <router-link to="/" class="navbar-item">首頁</router-link>
        <router-link to="/residents" class="navbar-item">住戶管理</router-link>
        <router-link to="/properties" class="navbar-item">物件管理</router-link>
        <router-link to="/payments" class="navbar-item">繳費管理</router-link>
        <router-link to="/potential-customers">潛在客戶管理</router-link>
        <router-link to="/maintenance" class="navbar-item">維修管理</router-link>
        <router-link to="/announcements" class="navbar-item">公告管理</router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
</script>

<style scoped>
.navbar {
  background-color: #f8f9fa;
  padding: 0.5rem 1rem;
  border-bottom: 1px solid #dee2e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand {
  display: flex;
  align-items: center;
}

.brand-text {
  font-size: 1.5rem;
  font-weight: bold;
  color: #343a40;
  text-decoration: none;
}

.navbar-menu {
  display: flex;
}

.navbar-start {
  display: flex;
  align-items: center;
}

.navbar-item {
  padding: 0.5rem 0.75rem;
  color: #495057;
  text-decoration: none;
}

.navbar-item:hover,
.navbar-item.router-link-exact-active {
  color: #007bff;
  background-color: #e9ecef;
  border-radius: 0.25rem;
}
</style>