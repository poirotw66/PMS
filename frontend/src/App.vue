<script setup>
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';
</script>

<template>
  <div id="app">
    <Navbar />
    <main class="main-content">
      <div class="container">
        <router-view />
      </div>
    </main>
    <Footer />
  </div>
</template>

<style>
/* 全局樣式，不使用 scoped */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&display=swap');

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: var(--spacing-md) 0;
  background-color: var(--bg-light);
}

/* 共用的頁面標題樣式 */
.page-title {
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-sm);
  border-bottom: 2px solid var(--primary-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title h1 {
  margin-bottom: 0;
  color: var(--text-color);
}

/* 基本布局組件 */
.section {
  margin-bottom: var(--spacing-xl);
}

/* 響應式調整 */
@media (max-width: 768px) {
  .container {
    padding: 0 var(--spacing-sm);
  }
  
  .page-title {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .page-title .actions {
    margin-top: var(--spacing-sm);
  }
}
</style>