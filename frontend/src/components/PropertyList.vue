<template>
  <div class="property-list">
    <h2>物件列表</h2>
    <ul v-if="properties && properties.length">
      <li v-for="property in properties" :key="property.id">
        {{ property.address }} - {{ property.size_sq_ft }}
        <!-- TODO: Add more property details and actions -->
      </li>
    </ul>
    <p v-else>沒有物件資料。</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  properties: {
    type: Array,
    default: () => []
  }
});
</script>

<style scoped>
.property-list {
  margin-top: 1rem;
}

.property-list ul {
  list-style: none;
  padding: 0;
}

.property-list li {
  background-color: #f9f9f9;
  border: 1px solid #eee;
  margin-bottom: 0.5rem;
  padding: 0.5rem;
}
</style>