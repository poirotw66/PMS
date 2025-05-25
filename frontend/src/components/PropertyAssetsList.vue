<template>
  <div class="assets-list">
    <div class="page-title">
      <h1>物件資產管理</h1>
      <div class="actions">
        <button @click="$emit('back')" class="btn btn-secondary">
          <i class="fas fa-arrow-left"></i> 返回物件列表
        </button>
        <button @click="showAssetForm = true" class="btn btn-success">
          <i class="fas fa-plus"></i> 新增資產
        </button>
      </div>
    </div>

    <!-- 資產表單 -->
    <div class="card" v-if="showAssetForm">
      <PropertyAssetForm 
        :asset="selectedAsset" 
        :propertyId="propertyId"
        @submit="saveAsset" 
        @cancel="cancelAssetForm" 
        :isEdit="!!selectedAsset?.id"
      />
    </div>

    <!-- 資產列表 -->
    <div v-else>
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>載入資產資料中...</p>
      </div>
      
      <div v-else-if="error" class="error-container">
        <div class="error-icon">
          <i class="fas fa-exclamation-triangle"></i>
        </div>
        <p>{{ error }}</p>
        <button @click="fetchAssets" class="btn btn-primary">重新嘗試</button>
      </div>
      
      <div v-else-if="assets.length === 0" class="empty-state">
        <div class="empty-icon">
          <i class="fas fa-box-open"></i>
        </div>
        <p>此物件尚無資產紀錄</p>
        <button @click="showAssetForm = true" class="btn btn-primary">新增第一筆資產</button>
      </div>
      
      <div v-else class="assets-container">
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>資產名稱/品牌/型號</th>
                <th>類型</th>
                <th>購買日期</th>
                <th>購買價格</th>
                <th>購買廠商/電話</th>
                <th>保固期間</th>
                <th>目前狀態</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="asset in assets" :key="asset.id">
                <td class="asset-name">{{ asset.name }}</td>
                <td>
                  <span class="badge" :class="getAssetTypeClass(asset.asset_type)">
                    {{ asset.asset_type || '未分類' }}
                  </span>
                </td>
                <td>{{ asset.purchase_date || '未登記' }}</td>
                <td>{{ asset.purchase_price || '未登記' }}</td>
                <td>{{ asset.purchase_vendor || '未登記' }}</td>
                <td>{{ asset.warranty_period || '未登記' }}</td>
                <td>
                  <span class="status" :class="getStatusClass(asset.current_status)">
                    {{ asset.current_status || '良好' }}
                  </span>
                </td>
                <td class="actions">
                  <button @click="editAsset(asset)" class="btn btn-warning btn-sm">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button @click="confirmDelete(asset.id)" class="btn btn-danger btn-sm">
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { getPropertyAssets, addPropertyAsset, updatePropertyAsset, deletePropertyAsset } from '@/services/api';
import PropertyAssetForm from '@/components/PropertyAssetForm.vue';

const props = defineProps({
  propertyId: {
    type: Number,
    required: true
  }
});

const emit = defineEmits(['back']);

// 狀態變數
const assets = ref([]);
const loading = ref(false);
const error = ref(null);
const showAssetForm = ref(false);
const selectedAsset = ref(null);

// 監聽 propertyId 變更，重新載入資產
watch(() => props.propertyId, (newId) => {
  if (newId) {
    fetchAssets();
  }
}, { immediate: true });

// 載入資產數據
async function fetchAssets() {
  if (!props.propertyId) return;
  
  loading.value = true;
  error.value = null;
  try {
    assets.value = await getPropertyAssets(props.propertyId);
  } catch (err) {
    console.error(`無法獲取物件 ${props.propertyId} 的資產數據:`, err);
    error.value = '載入資產失敗，請稍後再試。';
  } finally {
    loading.value = false;
  }
}

// 編輯資產
function editAsset(asset) {
  selectedAsset.value = { ...asset };
  showAssetForm.value = true;
}

// 儲存資產（新增或更新）
async function saveAsset(assetData) {
  loading.value = true;
  error.value = null;
  try {
    if (selectedAsset.value && selectedAsset.value.id) {
      // 更新現有資產
      await updatePropertyAsset(props.propertyId, selectedAsset.value.id, assetData);
    } else {
      // 新增資產
      await addPropertyAsset(props.propertyId, { ...assetData, property_id: props.propertyId });
    }
    // 重新獲取所有資產
    await fetchAssets();
    // 關閉表單
    cancelAssetForm();
  } catch (err) {
    console.error('保存資產失敗:', err);
    error.value = '保存資產失敗，請稍後再試。';
  } finally {
    loading.value = false;
  }
}

// 確認刪除資產
async function confirmDelete(assetId) {
  if (confirm('確定要刪除此資產紀錄嗎？此操作無法撤銷。')) {
    loading.value = true;
    error.value = null;
    try {
      await deletePropertyAsset(props.propertyId, assetId);
      await fetchAssets();
    } catch (err) {
      console.error(`刪除資產 ${assetId} 失敗:`, err);
      error.value = '刪除資產失敗，請稍後再試。';
    } finally {
      loading.value = false;
    }
  }
}

// 取消資產表單
function cancelAssetForm() {
  showAssetForm.value = false;
  selectedAsset.value = null;
}

// 根據資產類型返回對應的樣式類
function getAssetTypeClass(type) {
  switch(type) {
    case '家電類': return 'badge-primary';
    case '傢俱類': return 'badge-secondary';
    default: return 'badge-info';
  }
}

// 根據狀態返回對應的樣式類
function getStatusClass(status) {
  switch(status) {
    case '良好': return 'status-success';
    case '待修': return 'status-warning';
    case '已報廢': return 'status-danger';
    default: return 'status-info';
  }
}
</script>

<style scoped>
.assets-list {
  margin-bottom: var(--spacing-xl);
}

.table-responsive {
  overflow-x: auto;
  margin-bottom: var(--spacing-md);
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 50px;
  font-size: 0.75rem;
  font-weight: 500;
}

.badge-primary {
  background-color: var(--primary-light);
  color: var(--primary-dark);
}

.badge-secondary {
  background-color: var(--bg-dark);
  color: var(--text-light);
}

.badge-info {
  background-color: var(--bg-light);
  color: var(--text-light);
}

.asset-name {
  font-weight: 500;
}

.status {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: var(--border-radius);
  font-size: 0.75rem;
  font-weight: 500;
}

.status-success {
  background-color: var(--secondary-light);
  color: var(--secondary-dark);
}

.status-warning {
  background-color: #fff3cd;
  color: #856404;
}

.status-danger {
  background-color: #f8d7da;
  color: #721c24;
}

.status-info {
  background-color: var(--primary-light);
  color: var(--primary-dark);
}

.actions {
  display: flex;
  gap: var(--spacing-xs);
}

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
</style>
