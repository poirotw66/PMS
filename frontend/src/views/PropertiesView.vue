<template>
  <div class="properties-view">
    <h1>物件管理</h1>
    <p>這裡是物件管理頁面。</p>
    <PropertyList :properties="properties" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api'; // 假設有一個 API 服務
import PropertyList from '@/components/PropertyList.vue';

const properties = ref([]);

onMounted(async () => {
  try {
    const response = await api.get('/properties'); // 假設 API 端點是 /properties
    properties.value = response.data;
  } catch (error) {
    console.error('無法獲取物件資料:', error);
  }
});
</script>

<style scoped>
.properties-view {
  padding: 1rem;
}
</style>