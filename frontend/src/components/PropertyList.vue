<template>
  <div class="property-list">
    <div class="page-title">
      <h1>物件管理</h1>
      <div class="actions">
        <button @click="$emit('add-property')" class="btn btn-success">
          <i class="fas fa-plus"></i> 新增物件
        </button>
      </div>
    </div>
    
    <div class="properties-container" v-if="properties && properties.length">
      <div v-for="property in properties" :key="property.id" class="property-card">
        <div class="property-header">
          <h3>{{ property.address }}</h3>
          <div class="property-meta">
            <span class="property-size">{{ property.size_sq_ft }} 坪</span>
          </div>
        </div>
        
        <div class="property-body">
          <div class="property-info">
            <p v-if="property.features" class="property-features">{{ property.features }}</p>
          </div>
          
          <div class="property-stats">
            <div class="stat-item">
              <span class="stat-label">資產數量</span>
              <span class="stat-value">{{ property.assets ? property.assets.length : 0 }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">維修請求</span>
              <span class="stat-value">{{ property.repair_requests ? property.repair_requests.length : 0 }}</span>
            </div>
          </div>
        </div>
        
        <div class="property-footer">
          <div class="property-actions">
            <button @click="$emit('view-property', property.id)" class="btn btn-info btn-sm">
              <i class="fas fa-eye"></i> 查看
            </button>
            <button @click="$emit('edit-property', property)" class="btn btn-warning btn-sm">
              <i class="fas fa-edit"></i> 編輯
            </button>
            <button @click="emitDeleteProperty(property.id)" class="btn btn-danger btn-sm">
              <i class="fas fa-trash"></i> 刪除
            </button>
          </div>
          
          <div class="property-management">
            <button @click="$emit('manage-assets', property.id)" class="btn btn-secondary btn-sm">
              <i class="fas fa-box"></i> 管理資產
            </button>
            <button @click="$emit('manage-repairs', property.id)" class="btn btn-secondary btn-sm">
              <i class="fas fa-tools"></i> 管理維修
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="empty-state">
      <div class="empty-icon">
        <i class="fas fa-home"></i>
      </div>
      <p>尚無物件資料</p>
      <button @click="$emit('add-property')" class="btn btn-primary">新增第一個物件</button>
    </div>
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
  if (confirm('確定要刪除此物件嗎？此操作無法撤銷。')) {
    emit('delete-property', propertyId);
  }
};
</script>

<style scoped>
.property-list {
  margin-bottom: var(--spacing-xl);
}

.properties-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--spacing-md);
}

.property-card {
  background-color: var(--bg-color);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: var(--transition);
  border: 1px solid var(--border-color);
  height: 100%;
}

.property-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.property-header {
  padding: var(--spacing-md);
  background-color: var(--primary-light);
  border-bottom: 1px solid var(--border-color);
}

.property-header h3 {
  margin: 0 0 var(--spacing-xs) 0;
  font-size: 1.2rem;
  color: var(--text-color);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.property-meta {
  display: flex;
  font-size: 0.9rem;
  color: var(--text-light);
}

.property-size {
  font-weight: 500;
  background-color: var(--bg-light);
  padding: 0.1rem 0.5rem;
  border-radius: 12px;
}

.property-body {
  padding: var(--spacing-md);
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.property-info {
  margin-bottom: var(--spacing-md);
}

.property-features {
  margin: 0;
  color: var(--text-light);
  font-size: 0.95rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.property-stats {
  display: flex;
  margin-top: auto;
  gap: var(--spacing-md);
}

.stat-item {
  flex: 1;
  text-align: center;
  background-color: var(--bg-light);
  padding: var(--spacing-sm);
  border-radius: var(--border-radius);
}

.stat-label {
  display: block;
  font-size: 0.8rem;
  color: var(--text-light);
  margin-bottom: var(--spacing-xs);
}

.stat-value {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--primary-color);
}

.property-footer {
  padding: var(--spacing-md);
  border-top: 1px solid var(--border-color);
  background-color: var(--bg-light);
}

.property-actions {
  display: flex;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-sm);
}

.property-management {
  display: flex;
  justify-content: space-between;
}

.empty-state {
  text-align: center;
  padding: var(--spacing-xl) 0;
  color: var(--text-lighter);
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-md);
  color: var(--border-color);
}

.empty-state p {
  margin-bottom: var(--spacing-md);
  font-size: 1.1rem;
}

/* 響應式設計 */
@media (max-width: 768px) {
  .properties-container {
    grid-template-columns: 1fr;
  }
  
  .property-management {
    flex-direction: column;
    gap: var(--spacing-xs);
  }
  
  .property-management button {
    width: 100%;
  }
}
</style>