<template>
  <div class="property-list">
    <h2>物件列表</h2>
    <div class="property-actions">
      <button @click="$emit('add-property')" class="btn btn-success">新增物件</button>
    </div>
    <div class="properties-container" v-if="properties && properties.length">
      <div v-for="property in properties" :key="property.id" class="property-card">
        <div class="property-header">
          <h3>{{ property.address }}</h3>
          <div class="property-actions">
            <button @click="$emit('view-property', property.id)" class="btn btn-info">查看詳情</button>
            <button @click="$emit('edit-property', property)" class="btn btn-warning">編輯</button>
            <button @click="emitDeleteProperty(property.id)" class="btn btn-danger">刪除</button>
          </div>
        </div>
        <div class="property-body">
          <div class="property-info">
            <p><strong>物件坪數:</strong> {{ property.size_sq_ft }}</p>
            <p v-if="property.features"><strong>物件特色:</strong> {{ property.features }}</p>
          </div>
          <div class="property-assets" v-if="property.assets && property.assets.length">
            <h4>資產清單</h4>
            <ul>
              <li v-for="asset in property.assets" :key="asset.id">
                {{ asset.name }}
                <span v-if="asset.purchase_date">(購買日期: {{ asset.purchase_date }})</span>
              </li>
            </ul>
          </div>
          <div class="property-repairs" v-if="property.repair_requests && property.repair_requests.length">
            <h4>維修紀錄</h4>
            <ul>
              <li v-for="request in property.repair_requests" :key="request.id">
                {{ request.description }}
                <span v-if="request.request_date">(報修日期: {{ request.request_date }})</span>
                <span v-if="request.resolution_date" class="status-resolved">(已結案: {{ request.resolution_date }})</span>
                <span v-else class="status-pending">(待處理)</span>
              </li>
            </ul>
          </div>
        </div>
        <div class="property-footer">
          <button @click="$emit('manage-assets', property.id)" class="btn btn-secondary">管理資產</button>
          <button @click="$emit('manage-repairs', property.id)" class="btn btn-secondary">管理維修</button>
        </div>
      </div>
    </div>
    <p v-else>沒有物件資料。</p>
  </div>
</template>

<script setup>
// defineProps 已經是編譯器宏，不需要導入
const props = defineProps({
  properties: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits([
  'delete-property', 
  'edit-property', 
  'add-property', 
  'view-property',
  'manage-assets',
  'manage-repairs'
]); 

const emitDeleteProperty = (propertyId) => {
  if (confirm('確定要刪除此物件嗎？')) { // 添加確認提示
    emit('delete-property', propertyId); // 觸發事件並傳遞物件 ID
  }
};
</script>

<style scoped>
.property-list {
  margin-top: 1rem;
}

.property-actions {
  margin-bottom: 1rem;
  display: flex;
  justify-content: flex-end;
}

.properties-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.property-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.property-header {
  padding: 1rem;
  background-color: #f5f5f5;
  border-bottom: 1px solid #e0e0e0;
}

.property-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.property-header .property-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.property-body {
  padding: 1rem;
  flex-grow: 1;
}

.property-info p {
  margin: 0.5rem 0;
}

.property-assets, .property-repairs {
  margin-top: 1rem;
}

.property-assets h4, .property-repairs h4 {
  font-size: 1rem;
  margin-bottom: 0.5rem;
  color: #555;
}

.property-assets ul, .property-repairs ul {
  list-style: none;
  padding-left: 1rem;
}

.property-assets li, .property-repairs li {
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
}

.property-footer {
  padding: 1rem;
  border-top: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.btn-success {
  background-color: #4CAF50;
  color: white;
}

.btn-info {
  background-color: #2196F3;
  color: white;
}

.btn-warning {
  background-color: #FF9800;
  color: white;
}

.btn-danger {
  background-color: #F44336;
  color: white;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
}

.status-resolved {
  color: #4CAF50;
}

.status-pending {
  color: #FF9800;
}
</style>