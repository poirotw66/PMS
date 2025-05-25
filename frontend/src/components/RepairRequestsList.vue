<template>
  <div class="repairs-list">
    <h3>維修請求列表</h3>
    <div class="repair-actions">
      <button @click="showRepairForm = true" class="btn btn-success">新增維修請求</button>
      <button @click="$emit('back')" class="btn btn-secondary">返回列表</button>
    </div>

    <!-- 維修請求表單 -->
    <RepairRequestForm 
      v-if="showRepairForm" 
      :repair="selectedRepair" 
      :propertyId="propertyId"
      @submit="saveRepair" 
      @cancel="cancelRepairForm" 
      :isEdit="!!selectedRepair?.id"
    />

    <!-- 維修請求列表 -->
    <div v-else>
      <table v-if="repairs.length" class="repairs-table">
        <thead>
          <tr>
            <th>報修日期</th>
            <th>報修人ID</th>
            <th>維修項目/工作內容</th>
            <th>維修廠商/人員</th>
            <th>維修費用</th>
            <th>費用承擔方</th>
            <th>結案方式</th>
            <th>結案日期</th>
            <th>狀態</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="repair in repairs" :key="repair.id" :class="{ 'resolved': repair.resolution_date }">
            <td>{{ repair.request_date }}</td>
            <td>{{ repair.tenant_id }}</td>
            <td>{{ repair.description }}</td>
            <td>{{ repair.repair_vendor || '未指定' }}</td>
            <td>{{ repair.repair_cost || '未登記' }}</td>
            <td>{{ repair.cost_bearer || '未指定' }}</td>
            <td>{{ repair.resolution_method || '尚未解決' }}</td>
            <td>{{ repair.resolution_date || '尚未結案' }}</td>
            <td>
              <span class="status" :class="repair.resolution_date ? 'resolved' : 'pending'">
                {{ repair.resolution_date ? '已結案' : '處理中' }}
              </span>
            </td>
            <td class="actions">
              <button @click="editRepair(repair)" class="btn btn-warning btn-sm">編輯</button>
              <button @click="confirmDelete(repair.id)" class="btn btn-danger btn-sm">刪除</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>此物件尚無維修請求紀錄。</p>
      <div v-if="loading" class="loading">載入中...</div>
      <div v-if="error" class="error">{{ error }}</div>
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
  if (confirm('確定要刪除此維修請求紀錄嗎？')) {
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
</script>

<style scoped>
.repairs-list {
  margin-top: 1rem;
}

.repair-actions {
  margin-bottom: 1rem;
  display: flex;
  justify-content: flex-end;
}

.repairs-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.repairs-table th, .repairs-table td {
  border: 1px solid #ddd;
  padding: 0.5rem;
  text-align: left;
}

.repairs-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.repairs-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.repairs-table tr.resolved {
  background-color: #e8f5e9;
}

.status {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}

.status.resolved {
  background-color: #4CAF50;
  color: white;
}

.status.pending {
  background-color: #FF9800;
  color: white;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.8rem;
}

.btn-success {
  background-color: #4CAF50;
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
</style>
