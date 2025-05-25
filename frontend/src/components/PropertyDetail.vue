<template>
  <div class="property-detail">
    <div class="detail-header">
      <h2>物件詳情</h2>
      <div class="actions">
        <button @click="$emit('back')" class="btn btn-secondary">返回列表</button>
        <button @click="$emit('edit-property', property)" class="btn btn-warning">編輯物件</button>
      </div>
    </div>

    <div v-if="loading" class="loading">載入中...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="property" class="detail-content">
      <div class="detail-section">
        <h3>基本資訊</h3>
        <div class="detail-item">
          <span class="label">物件編號:</span>
          <span class="value">{{ property.id }}</span>
        </div>
        <div class="detail-item">
          <span class="label">物件地址:</span>
          <span class="value">{{ property.address }}</span>
        </div>
        <div class="detail-item">
          <span class="label">物件坪數:</span>
          <span class="value">{{ property.size_sq_ft }}</span>
        </div>
        <div class="detail-item">
          <span class="label">物件特色:</span>
          <span class="value">{{ property.features || '無特色描述' }}</span>
        </div>
      </div>

      <div class="detail-section">
        <div class="section-header">
          <h3>資產明細</h3>
          <button @click="$emit('manage-assets', property.id)" class="btn btn-primary btn-sm">管理資產</button>
        </div>
        <div v-if="property.assets && property.assets.length">
          <div class="asset-categories">
            <div class="category" v-if="filterAssetsByType('家電類').length > 0">
              <h4>家電類</h4>
              <div v-for="asset in filterAssetsByType('家電類')" :key="asset.id" class="asset-item">
                <div class="asset-name">{{ asset.name }}</div>
                <div class="asset-details">
                  <div v-if="asset.purchase_date"><span class="label">購買日期:</span> {{ asset.purchase_date }}</div>
                  <div v-if="asset.purchase_price"><span class="label">購買價格:</span> {{ asset.purchase_price }}</div>
                  <div v-if="asset.purchase_vendor"><span class="label">購買廠商:</span> {{ asset.purchase_vendor }}</div>
                  <div v-if="asset.warranty_period"><span class="label">保固期間:</span> {{ asset.warranty_period }}</div>
                  <div v-if="asset.current_status"><span class="label">目前狀態:</span> {{ asset.current_status }}</div>
                </div>
              </div>
            </div>

            <div class="category" v-if="filterAssetsByType('傢俱類').length > 0">
              <h4>傢俱類</h4>
              <div v-for="asset in filterAssetsByType('傢俱類')" :key="asset.id" class="asset-item">
                <div class="asset-name">{{ asset.name }}</div>
                <div class="asset-details">
                  <div v-if="asset.purchase_date"><span class="label">購買日期:</span> {{ asset.purchase_date }}</div>
                  <div v-if="asset.purchase_price"><span class="label">購買價格:</span> {{ asset.purchase_price }}</div>
                  <div v-if="asset.purchase_vendor"><span class="label">購買廠商:</span> {{ asset.purchase_vendor }}</div>
                  <div v-if="asset.warranty_period"><span class="label">保固期間:</span> {{ asset.warranty_period }}</div>
                  <div v-if="asset.current_status"><span class="label">目前狀態:</span> {{ asset.current_status }}</div>
                </div>
              </div>
            </div>

            <div class="category" v-if="filterAssetsByType('其他').length > 0">
              <h4>其他資產</h4>
              <div v-for="asset in filterAssetsByType('其他')" :key="asset.id" class="asset-item">
                <div class="asset-name">{{ asset.name }}</div>
                <div class="asset-details">
                  <div v-if="asset.purchase_date"><span class="label">購買日期:</span> {{ asset.purchase_date }}</div>
                  <div v-if="asset.purchase_price"><span class="label">購買價格:</span> {{ asset.purchase_price }}</div>
                  <div v-if="asset.purchase_vendor"><span class="label">購買廠商:</span> {{ asset.purchase_vendor }}</div>
                  <div v-if="asset.warranty_period"><span class="label">保固期間:</span> {{ asset.warranty_period }}</div>
                  <div v-if="asset.current_status"><span class="label">目前狀態:</span> {{ asset.current_status }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <p v-else>此物件尚無資產紀錄</p>
      </div>

      <div class="detail-section">
        <div class="section-header">
          <h3>維修紀錄</h3>
          <button @click="$emit('manage-repairs', property.id)" class="btn btn-primary btn-sm">管理維修</button>
        </div>
        <div v-if="property.repair_requests && property.repair_requests.length">
          <div v-for="repair in property.repair_requests" :key="repair.id" class="repair-item" :class="{ 'resolved': repair.resolution_date }">
            <div class="repair-header">
              <div class="repair-date">{{ repair.request_date }}</div>
              <div class="repair-status" :class="repair.resolution_date ? 'status-resolved' : 'status-pending'">
                {{ repair.resolution_date ? '已結案' : '處理中' }}
              </div>
            </div>
            <div class="repair-description">{{ repair.description }}</div>
            <div v-if="repair.repair_vendor" class="repair-detail">
              <span class="label">維修廠商/人員:</span> {{ repair.repair_vendor }}
            </div>
            <div v-if="repair.repair_cost" class="repair-detail">
              <span class="label">維修費用:</span> {{ repair.repair_cost }}
              <span v-if="repair.cost_bearer">({{ repair.cost_bearer }})</span>
            </div>
            <div v-if="repair.resolution_method" class="repair-detail">
              <span class="label">結案方式:</span> {{ repair.resolution_method }}
            </div>
            <div v-if="repair.resolution_date" class="repair-detail">
              <span class="label">結案日期:</span> {{ repair.resolution_date }}
            </div>
            <div v-if="repair.remarks" class="repair-detail">
              <span class="label">備註:</span> {{ repair.remarks }}
            </div>
          </div>
        </div>
        <p v-else>此物件尚無維修紀錄</p>
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
</script>

<style scoped>
.property-detail {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.detail-header h2 {
  margin: 0;
  color: #333;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.detail-section {
  margin-bottom: 2rem;
}

.detail-section h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #444;
  font-size: 1.2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h3 {
  margin: 0;
}

.detail-item {
  margin-bottom: 0.5rem;
  display: flex;
}

.label {
  font-weight: bold;
  color: #555;
  width: 100px;
  flex-shrink: 0;
}

.value {
  flex-grow: 1;
}

.asset-categories {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.category h4 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #555;
  font-size: 1rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
}

.asset-item {
  background-color: #f9f9f9;
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.asset-name {
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #333;
}

.asset-details {
  font-size: 0.9rem;
  color: #555;
}

.asset-details div {
  margin-bottom: 0.25rem;
}

.repair-item {
  background-color: #f9f9f9;
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1rem;
  border-left: 4px solid #FF9800;
}

.repair-item.resolved {
  border-left-color: #4CAF50;
  background-color: #f1f8e9;
}

.repair-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.repair-date {
  font-weight: bold;
}

.repair-status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}

.status-resolved {
  background-color: #4CAF50;
  color: white;
}

.status-pending {
  background-color: #FF9800;
  color: white;
}

.repair-description {
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.repair-detail {
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 0.25rem;
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

.btn-primary {
  background-color: #2196F3;
  color: white;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
}

.btn-warning {
  background-color: #FF9800;
  color: white;
}
</style>
