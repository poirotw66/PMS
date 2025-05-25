<template>
  <div class="assets-list">
    <h3>資產列表</h3>
    <div class="asset-actions">
      <button @click="showAssetForm = true" class="btn btn-success">新增資產</button>
      <button @click="$emit('back')" class="btn btn-secondary">返回列表</button>
    </div>

    <!-- 資產表單 -->
    <PropertyAssetForm 
      v-if="showAssetForm" 
      :asset="selectedAsset" 
      @submit="saveAsset" 
      @cancel="cancelAssetForm" 
      :isEdit="!!selectedAsset?.id"
    />

    <!-- 資產列表 -->
    <div v-else>
      <table v-if="assets.length" class="assets-table">
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
            <td>{{ asset.name }}</td>
            <td>{{ asset.asset_type || '未分類' }}</td>
            <td>{{ asset.purchase_date || '未登記' }}</td>
            <td>{{ asset.purchase_price || '未登記' }}</td>
            <td>{{ asset.purchase_vendor || '未登記' }}</td>
            <td>{{ asset.warranty_period || '未登記' }}</td>
            <td>{{ asset.current_status || '良好' }}</td>
            <td class="actions">
              <button @click="editAsset(asset)" class="btn btn-warning btn-sm">編輯</button>
              <button @click="confirmDelete(asset.id)" class="btn btn-danger btn-sm">刪除</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>此物件尚無資產紀錄。</p>
      <div v-if="loading" class="loading">載入中...</div>
      <div v-if="error" class="error">{{ error }}</div>
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
  if (confirm('確定要刪除此資產紀錄嗎？')) {
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
</script>

<style scoped>
.assets-list {
  margin-top: 1rem;
}

.asset-actions {
  margin-bottom: 1rem;
  display: flex;
  justify-content: flex-end;
}

.assets-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.assets-table th, .assets-table td {
  border: 1px solid #ddd;
  padding: 0.5rem;
  text-align: left;
}

.assets-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.assets-table tr:nth-child(even) {
  background-color: #f9f9f9;
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

.loading {
  text-align: center;
  padding: 1rem;
}

.error {
  color: #F44336;
  text-align: center;
  padding: 1rem;
}
</style>
