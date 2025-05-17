<template>
  <div class="maintenance-view">
    <h1>維修管理</h1>
    <p>這裡是維修管理頁面。</p>
    <!-- 維修請求列表、新增請求、更新狀態等功能將在此實現 -->
  </div>
</template>

<script setup>
// import { ref, onMounted } from 'vue';
// import api from '@/services/api'; // 假設有一個 API 服務

// const maintenanceRequests = ref([]);

// onMounted(async () => {
//   try {
//     // const response = await api.getMaintenanceRequests();
//     // maintenanceRequests.value = response.data;
//   } catch (error) {
//     console.error('無法獲取維修請求資料:', error);
//   }
// });
</script>

<style scoped>
.maintenance-view {
  padding: 1rem;
}
</style>