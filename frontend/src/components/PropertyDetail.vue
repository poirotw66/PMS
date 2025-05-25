<template>
  <div class="property-detail">
    <div class="page-title">
      <h1>物件詳情</h1>
      <div class="actions">
        <button @click="$emit('back')" class="btn btn-secondary">
          <i class="fas fa-arrow-left"></i> 返回列表
        </button>
        <button @click="$emit('edit-property', property)" class="btn btn-warning">
          <i class="fas fa-edit"></i> 編輯物件
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>載入物件詳情中...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <div class="error-icon">
        <i class="fas fa-exclamation-triangle"></i>
      </div>
      <p>{{ error }}</p>
      <button @click="fetchPropertyDetails" class="btn btn-primary">重新嘗試</button>
    </div>

    <div v-else-if="property" class="detail-content">
      <!-- 基本資訊卡片 -->
      <div class="card detail-card">
        <div class="card-header">
          <h3><i class="fas fa-info-circle"></i> 基本資訊</h3>
        </div>
        <div class="card-body">
          <div class="property-address">
            <i class="fas fa-map-marker-alt address-icon"></i>
            <span>{{ property.address }}</span>
          </div>
          
          <div class="property-meta">
            <div class="meta-item">
              <i class="fas fa-id-card"></i>
              <span class="meta-label">物件編號:</span>
              <span class="meta-value">{{ property.id }}</span>
            </div>
            
            <div class="meta-item">
              <i class="fas fa-expand"></i>
              <span class="meta-label">物件坪數:</span>
              <span class="meta-value">{{ property.size_sq_ft }} 坪</span>
            </div>
          </div>
          
          <div class="property-features" v-if="property.features">
            <h4>物件特色</h4>
            <p>{{ property.features }}</p>
          </div>
        </div>
      </div>

      <!-- 資產明細卡片 -->
      <div class="card detail-card">
        <div class="card-header">
          <h3><i class="fas fa-box"></i> 資產明細</h3>
          <button @click="$emit('manage-assets', property.id)" class="btn btn-primary btn-sm">
            <i class="fas fa-cog"></i> 管理資產
          </button>
        </div>
        <div class="card-body">
          <div v-if="property.assets && property.assets.length">
            <div class="asset-tabs">
              <div 
                class="tab-item" 
                v-for="type in assetTypes" 
                :key="type.id"
                :class="{ 'active': activeAssetTab === type.id }"
                @click="activeAssetTab = type.id"
              >
                <i :class="type.icon"></i> {{ type.name }}
                <span class="count">{{ filterAssetsByType(type.id).length }}</span>
              </div>
            </div>
            
            <div class="asset-list">
              <div v-if="filterAssetsByType(activeAssetTab).length > 0">
                <div v-for="asset in filterAssetsByType(activeAssetTab)" :key="asset.id" class="asset-card">
                  <div class="asset-header">
                    <h4>{{ asset.name }}</h4>
                    <span class="asset-status" :class="getAssetStatusClass(asset.current_status)">
                      {{ asset.current_status || '良好' }}
                    </span>
                  </div>
                  <div class="asset-details">
                    <div class="asset-detail-item" v-if="asset.purchase_date">
                      <i class="fas fa-calendar"></i>
                      <span>購買日期: {{ asset.purchase_date }}</span>
                    </div>
                    <div class="asset-detail-item" v-if="asset.purchase_price">
                      <i class="fas fa-tag"></i>
                      <span>購買價格: {{ asset.purchase_price }}</span>
                    </div>
                    <div class="asset-detail-item" v-if="asset.purchase_vendor">
                      <i class="fas fa-store"></i>
                      <span>購買廠商: {{ asset.purchase_vendor }}</span>
                    </div>
                    <div class="asset-detail-item" v-if="asset.warranty_period">
                      <i class="fas fa-shield-alt"></i>
                      <span>保固期間: {{ asset.warranty_period }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="empty-asset-type">
                <p>此物件沒有 {{ getAssetTypeName(activeAssetTab) }} 資產</p>
              </div>
            </div>
          </div>
          <div v-else class="empty-state">
            <div class="empty-icon">
              <i class="fas fa-box-open"></i>
            </div>
            <p>此物件尚無資產紀錄</p>
            <button @click="$emit('manage-assets', property.id)" class="btn btn-primary">新增資產</button>
          </div>
        </div>
      </div>

      <!-- 維修紀錄卡片 -->
      <div class="card detail-card">
        <div class="card-header">
          <h3><i class="fas fa-tools"></i> 維修紀錄</h3>
          <button @click="$emit('manage-repairs', property.id)" class="btn btn-primary btn-sm">
            <i class="fas fa-cog"></i> 管理維修
          </button>
        </div>
        <div class="card-body">
          <div v-if="property.repair_requests && property.repair_requests.length">
            <div class="repair-timeline">
              <div 
                v-for="repair in property.repair_requests" 
                :key="repair.id" 
                class="repair-card"
                :class="{ 'resolved': repair.resolution_date }"
              >
                <div class="repair-date">
                  <span class="date">{{ formatDate(repair.request_date) }}</span>
                  <span class="time-badge">{{ getTimeSince(repair.request_date) }}</span>
                </div>
                
                <div class="repair-content">
                  <div class="repair-header">
                    <h4 class="repair-title">{{ repair.description }}</h4>
                    <span class="repair-status" :class="repair.resolution_date ? 'status-success' : 'status-warning'">
                      {{ repair.resolution_date ? '已結案' : '處理中' }}
                    </span>
                  </div>
                  
                  <div class="repair-details">
                    <div class="repair-detail-item" v-if="repair.repair_vendor">
                      <i class="fas fa-user-cog"></i>
                      <span>維修廠商/人員: {{ repair.repair_vendor }}</span>
                    </div>
                    <div class="repair-detail-item" v-if="repair.repair_cost">
                      <i class="fas fa-dollar-sign"></i>
                      <span>維修費用: {{ repair.repair_cost }}</span>
                      <span v-if="repair.cost_bearer" class="cost-bearer">({{ repair.cost_bearer }})</span>
                    </div>
                    <div class="repair-detail-item" v-if="repair.resolution_method">
                      <i class="fas fa-check-circle"></i>
                      <span>結案方式: {{ repair.resolution_method }}</span>
                    </div>
                    <div class="repair-detail-item" v-if="repair.resolution_date">
                      <i class="fas fa-calendar-check"></i>
                      <span>結案日期: {{ repair.resolution_date }}</span>
                    </div>
                    <div class="repair-detail-item" v-if="repair.remarks">
                      <i class="fas fa-comment"></i>
                      <span>備註: {{ repair.remarks }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="empty-state">
            <div class="empty-icon">
              <i class="fas fa-tools"></i>
            </div>
            <p>此物件尚無維修紀錄</p>
            <button @click="$emit('manage-repairs', property.id)" class="btn btn-primary">新增維修請求</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { getPropertyById } from '@/services/api';

const props = defineProps({
  propertyId: {
    type: Number,
    required: true
  }
});

const emit = defineEmits(['back', 'edit-property', 'manage-assets', 'manage-repairs']);

// 狀態變數
const property = ref(null);
const loading = ref(false);
const error = ref(null);
const activeAssetTab = ref('家電類');

// 資產類型定義
const assetTypes = [
  { id: '家電類', name: '家電類', icon: 'fas fa-tv' },
  { id: '傢俱類', name: '傢俱類', icon: 'fas fa-couch' },
  { id: '其他', name: '其他資產', icon: 'fas fa-box' }
];

// 監聽 propertyId 變更，重新載入物件詳情
watch(() => props.propertyId, (newId) => {
  if (newId) {
    fetchPropertyDetails();
  }
}, { immediate: true });

// 載入物件詳情
async function fetchPropertyDetails() {
  if (!props.propertyId) return;
  
  loading.value = true;
  error.value = null;
  try {
    property.value = await getPropertyById(props.propertyId);
  } catch (err) {
    console.error(`無法獲取物件 ${props.propertyId} 的詳情:`, err);
    error.value = '載入物件詳情失敗，請稍後再試。';
  } finally {
    loading.value = false;
  }
}

// 篩選資產依類型
const filterAssetsByType = (type) => {
  if (!property.value?.assets) return [];
  
  if (type === '其他') {
    return property.value.assets.filter(asset => 
      !asset.asset_type || (asset.asset_type !== '家電類' && asset.asset_type !== '傢俱類')
    );
  }
  
  return property.value.assets.filter(asset => asset.asset_type === type);
};

// 取得資產類型名稱
const getAssetTypeName = (typeId) => {
  const type = assetTypes.find(t => t.id === typeId);
  return type ? type.name : typeId;
};

// 取得資產狀態樣式類
const getAssetStatusClass = (status) => {
  switch(status) {
    case '良好': return 'status-success';
    case '待修': return 'status-warning';
    case '已報廢': return 'status-danger';
    default: return 'status-info';
  }
};

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-TW', { year: 'numeric', month: '2-digit', day: '2-digit' });
};

// 計算時間差
const getTimeSince = (dateString) => {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  const now = new Date();
  const diffInDays = Math.floor((now - date) / (1000 * 60 * 60 * 24));
  
  if (diffInDays === 0) return '今天';
  if (diffInDays === 1) return '昨天';
  if (diffInDays < 30) return `${diffInDays} 天前`;
  if (diffInDays < 365) return `${Math.floor(diffInDays / 30)} 個月前`;
  return `${Math.floor(diffInDays / 365)} 年前`;
};
</script>

<style scoped>
.property-detail {
  margin-bottom: var(--spacing-xl);
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.detail-card {
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  color: var(--text-color);
}

.card-header h3 i {
  color: var(--primary-color);
}

/* 基本資訊樣式 */
.property-address {
  font-size: 1.25rem;
  margin-bottom: var(--spacing-md);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.address-icon {
  color: var(--primary-color);
}

.property-meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.meta-item i {
  color: var(--primary-color);
}

.meta-label {
  font-weight: 500;
  color: var(--text-light);
}

.meta-value {
  font-weight: 600;
}

.property-features {
  background-color: var(--bg-light);
  padding: var(--spacing-md);
  border-radius: var(--border-radius);
  margin-top: var(--spacing-md);
}

.property-features h4 {
  margin-top: 0;
  margin-bottom: var(--spacing-sm);
  color: var(--text-color);
  font-size: 1rem;
}

.property-features p {
  margin: 0;
  line-height: 1.5;
  color: var(--text-light);
}

/* 資產標籤頁樣式 */
.asset-tabs {
  display: flex;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
}

.tab-item {
  padding: var(--spacing-sm) var(--spacing-md);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  border-bottom: 2px solid transparent;
  transition: var(--transition);
}

.tab-item:hover {
  background-color: var(--bg-light);
}

.tab-item.active {
  border-bottom-color: var(--primary-color);
  color: var(--primary-color);
  font-weight: 500;
}

.count {
  background-color: var(--bg-light);
  color: var(--text-light);
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.asset-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: var(--spacing-md);
}

.asset-card {
  background-color: var(--bg-light);
  border-radius: var(--border-radius);
  overflow: hidden;
  border: 1px solid var(--border-color);
  transition: var(--transition);
}

.asset-card:hover {
  box-shadow: var(--shadow);
  transform: translateY(-2px);
}

.asset-header {
  padding: var(--spacing-sm) var(--spacing-md);
  background-color: var(--bg-color);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.asset-header h4 {
  margin: 0;
  font-size: 1rem;
}

.asset-status {
  font-size: 0.75rem;
  padding: 0.15rem 0.5rem;
  border-radius: 50px;
  font-weight: 500;
}

.asset-details {
  padding: var(--spacing-md);
}

.asset-detail-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-xs);
  font-size: 0.9rem;
  color: var(--text-light);
}

.asset-detail-item i {
  color: var(--primary-color);
  width: 16px;
  text-align: center;
}

.empty-asset-type {
  grid-column: 1 / -1;
  text-align: center;
  padding: var(--spacing-md);
  color: var(--text-lighter);
  background-color: var(--bg-light);
  border-radius: var(--border-radius);
}

/* 維修紀錄樣式 */
.repair-timeline {
  position: relative;
  padding-left: var(--spacing-xl);
}

.repair-timeline::before {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  left: 8px;
  width: 2px;
  background-color: var(--border-color);
}

.repair-card {
  position: relative;
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-md);
}

.repair-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: -25px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background-color: var(--warning-color);
  border: 2px solid var(--bg-color);
  z-index: 1;
}

.repair-card.resolved::before {
  background-color: var(--success-color);
}

.repair-date {
  margin-bottom: var(--spacing-xs);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.date {
  font-weight: 500;
}

.time-badge {
  font-size: 0.75rem;
  color: var(--text-lighter);
}

.repair-content {
  background-color: var(--bg-light);
  border-radius: var(--border-radius);
  padding: var(--spacing-md);
  border: 1px solid var(--border-color);
}

.repair-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-sm);
}

.repair-title {
  margin: 0;
  font-size: 1rem;
}

.repair-status {
  font-size: 0.75rem;
  padding: 0.15rem 0.5rem;
  border-radius: 50px;
  font-weight: 500;
}

.repair-detail-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-xs);
  font-size: 0.9rem;
  color: var(--text-light);
}

.repair-detail-item i {
  color: var(--primary-color);
  width: 16px;
  text-align: center;
}

.cost-bearer {
  margin-left: var(--spacing-xs);
  font-size: 0.8rem;
  color: var(--text-lighter);
}

/* 空狀態樣式 */
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

/* 加載和錯誤狀態 */
.loading-container {
  text-align: center;
  padding: var(--spacing-xl) 0;
}

.loading-spinner {
  display: inline-block;
  width: 50px;
  height: 50px;
  border: 4px solid var(--bg-dark);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s ease-in-out infinite;
  margin-bottom: var(--spacing-md);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-container {
  text-align: center;
  padding: var(--spacing-xl) 0;
  color: var(--danger-color);
}

.error-icon {
  font-size: 2.5rem;
  margin-bottom: var(--spacing-md);
}

/* 響應式設計 */
@media (max-width: 768px) {
  .property-meta {
    flex-direction: column;
    gap: var(--spacing-sm);
  }
  
  .asset-list {
    grid-template-columns: 1fr;
  }
  
  .repair-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-xs);
  }
}
</style>
