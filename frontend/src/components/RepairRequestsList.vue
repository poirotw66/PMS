<template>
  <div class="repairs-list">
    <div class="page-title">
      <h1>維修請求管理</h1>
      <div class="actions">
        <button @click="$emit('back')" class="btn btn-secondary">
          <i class="fas fa-arrow-left"></i> 返回物件列表
        </button>
        <button @click="showRepairForm = true" class="btn btn-success">
          <i class="fas fa-plus"></i> 新增維修請求
        </button>
      </div>
    </div>

    <!-- 維修請求表單 -->
    <div class="card" v-if="showRepairForm">
      <RepairRequestForm 
        :repair="selectedRepair" 
        :propertyId="propertyId"
        @submit="saveRepair" 
        @cancel="cancelRepairForm" 
        :isEdit="!!selectedRepair?.id"
      />
    </div>

    <!-- 維修請求列表 -->
    <div v-else>
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>載入維修請求資料中...</p>
      </div>
      
      <div v-else-if="error" class="error-container">
        <div class="error-icon">
          <i class="fas fa-exclamation-triangle"></i>
        </div>
        <p>{{ error }}</p>
        <button @click="fetchRepairs" class="btn btn-primary">重新嘗試</button>
      </div>
      
      <div v-else-if="repairs.length === 0" class="empty-state">
        <div class="empty-icon">
          <i class="fas fa-tools"></i>
        </div>
        <p>此物件尚無維修請求紀錄</p>
        <button @click="showRepairForm = true" class="btn btn-primary">新增第一筆維修請求</button>
      </div>
      
      <div v-else class="repairs-container">
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>報修日期</th>
                <th>報修人</th>
                <th>維修項目</th>
                <th>維修廠商</th>
                <th>維修費用</th>
                <th>費用承擔方</th>
                <th>結案方式</th>
                <th>結案日期</th>
                <th>狀態</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="repair in repairs" :key="repair.id" :class="{ 'resolved-row': repair.resolution_date }">
                <td>{{ repair.request_date }}</td>
                <td>{{ repair.tenant_id || '未記錄' }}</td>
                <td class="repair-description">{{ repair.description }}</td>
                <td>{{ repair.repair_vendor || '未指定' }}</td>
                <td>{{ repair.repair_cost || '未登記' }}</td>
                <td>{{ repair.cost_bearer || '未指定' }}</td>
                <td>{{ repair.resolution_method || '尚未解決' }}</td>
                <td>{{ repair.resolution_date || '尚未結案' }}</td>
                <td>
                  <span class="status" :class="getStatusClass(repair)">
                    {{ repair.resolution_date ? '已結案' : '處理中' }}
                  </span>
                </td>
                <td class="actions">
                  <button @click="editRepair(repair)" class="btn btn-warning btn-sm">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button @click="confirmDelete(repair.id)" class="btn btn-danger btn-sm">
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
import { getRepairRequests, addRepairRequest, updateRepairRequest, deleteRepairRequest } from '@/services/api';
import RepairRequestForm from '@/components/RepairRequestForm.vue';

const props = defineProps({
  propertyId: {
    type: Number,
    required: true
  }
});

const emit = defineEmits(['back']);

// 狀態變數
const repairs = ref([]);
const loading = ref(false);
const error = ref(null);
const showRepairForm = ref(false);
const selectedRepair = ref(null);

// 監聽 propertyId 變更，重新載入維修請求
watch(() => props.propertyId, (newId) => {
  if (newId) {
    fetchRepairs();
  }
}, { immediate: true });

// 載入維修請求數據
async function fetchRepairs() {
  if (!props.propertyId) return;
  
  loading.value = true;
  error.value = null;
  try {
    repairs.value = await getRepairRequests(props.propertyId);
  } catch (err) {
    console.error(`無法獲取物件 ${props.propertyId} 的維修請求數據:`, err);
    error.value = '載入維修請求失敗，請稍後再試。';
  } finally {
    loading.value = false;
  }
}

// 編輯維修請求
function editRepair(repair) {
  selectedRepair.value = { ...repair };
  showRepairForm.value = true;
}

// 儲存維修請求（新增或更新）
async function saveRepair(repairData) {
  loading.value = true;
  error.value = null;
  try {
    if (selectedRepair.value && selectedRepair.value.id) {
      // 更新現有維修請求
      await updateRepairRequest(props.propertyId, selectedRepair.value.id, repairData);
    } else {
      // 新增維修請求
      await addRepairRequest(props.propertyId, { ...repairData, property_id: props.propertyId });
    }
    // 重新獲取所有維修請求
    await fetchRepairs();
    // 關閉表單
    cancelRepairForm();
  } catch (err) {
    console.error('保存維修請求失敗:', err);
    error.value = '保存維修請求失敗，請稍後再試。';
  } finally {
    loading.value = false;
  }
}

// 確認刪除維修請求
async function confirmDelete(repairId) {
  if (confirm('確定要刪除此維修請求紀錄嗎？此操作無法撤銷。')) {
    loading.value = true;
    error.value = null;
    try {
      await deleteRepairRequest(props.propertyId, repairId);
      await fetchRepairs();
    } catch (err) {
      console.error(`刪除維修請求 ${repairId} 失敗:`, err);
      error.value = '刪除維修請求失敗，請稍後再試。';
    } finally {
      loading.value = false;
    }
  }
}

// 取消維修請求表單
function cancelRepairForm() {
  showRepairForm.value = false;
  selectedRepair.value = null;
}

// 獲取狀態樣式
function getStatusClass(repair) {
  if (repair.resolution_date) {
    return 'status-success';
  } else {
    return 'status-warning';
  }
}
</script>

<style scoped>
.repairs-list {
  margin-bottom: var(--spacing-xl);
}

.table-responsive {
  overflow-x: auto;
  margin-bottom: var(--spacing-md);
}

.repair-description {
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.resolved-row {
  background-color: var(--secondary-light) !important;
}

.status {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: var(--border-radius);
  font-size: 0.75rem;
  font-weight: 500;
  text-align: center;
  min-width: 70px;
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
