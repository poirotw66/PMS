<template>
  <div class="properties-view">
    
    <!-- 顯示物件表單或資產/維修管理組件 -->
    <PropertyForm 
      v-if="showPropertyForm" 
      :property="selectedProperty" 
      @save="saveProperty"
      @cancel="cancelEdit"
    />
    <PropertyAssetsList 
      v-else-if="showAssetsList" 
      :propertyId="selectedPropertyId"
      @back="backToProperties"
    />
    <RepairRequestsList 
      v-else-if="showRepairsList" 
      :propertyId="selectedPropertyId"
      @back="backToProperties"
    />
    <PropertyDetail 
      v-else-if="showPropertyDetail" 
      :propertyId="selectedPropertyId"
      @back="backToProperties"
    />
    
    <!-- 默認顯示物件列表 -->
    <PropertyList 
      v-else 
      :properties="properties" 
      @add-property="addNewProperty"
      @edit-property="editProperty"
      @delete-property="deleteProperty"
      @view-property="viewProperty"
      @manage-assets="manageAssets"
      @manage-repairs="manageRepairs"
    />
    
    <!-- 加載中和錯誤提示 -->
    <div v-if="loading" class="loading">載入中...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getProperties, addProperty, updateProperty, deleteProperty as apiDeleteProperty } from '@/services/api';
import PropertyList from '@/components/PropertyList.vue';
import PropertyForm from '@/components/PropertyForm.vue';
import PropertyAssetsList from '@/components/PropertyAssetsList.vue';
import RepairRequestsList from '@/components/RepairRequestsList.vue';
import PropertyDetail from '@/components/PropertyDetail.vue';

// 狀態變數
const properties = ref([]);
const loading = ref(false);
const error = ref(null);
const showPropertyForm = ref(false);
const showAssetsList = ref(false);
const showRepairsList = ref(false);
const showPropertyDetail = ref(false);
const selectedProperty = ref(null);
const selectedPropertyId = ref(null);

// 初始化載入物件數據
onMounted(async () => {
  await fetchProperties();
});

// 獲取所有物件
async function fetchProperties() {
  loading.value = true;
  error.value = null;
  try {
    properties.value = await getProperties();
  } catch (err) {
    console.error('無法獲取物件數據:', err);
    error.value = '載入物件失敗，請稍後再試。';
  } finally {
    loading.value = false;
  }
}

// 新增物件
function addNewProperty() {
  selectedProperty.value = null;
  showPropertyForm.value = true;
  showAssetsList.value = false;
  showRepairsList.value = false;
  showPropertyDetail.value = false;
}

// 編輯物件
function editProperty(property) {
  selectedProperty.value = { ...property };
  showPropertyForm.value = true;
  showAssetsList.value = false;
  showRepairsList.value = false;
  showPropertyDetail.value = false;
}

// 查看物件詳情
function viewProperty(propertyId) {
  selectedPropertyId.value = propertyId;
  showPropertyDetail.value = true;
  showPropertyForm.value = false;
  showAssetsList.value = false;
  showRepairsList.value = false;
}

// 管理資產
function manageAssets(propertyId) {
  selectedPropertyId.value = propertyId;
  showAssetsList.value = true;
  showPropertyForm.value = false;
  showRepairsList.value = false;
  showPropertyDetail.value = false;
}

// 管理維修請求
function manageRepairs(propertyId) {
  selectedPropertyId.value = propertyId;
  showRepairsList.value = true;
  showPropertyForm.value = false;
  showAssetsList.value = false;
  showPropertyDetail.value = false;
}

// 保存物件（新增或更新）
async function saveProperty(propertyData) {
  loading.value = true;
  error.value = null;
  try {
    if (selectedProperty.value && selectedProperty.value.id) {
      // 更新現有物件
      await updateProperty(selectedProperty.value.id, propertyData);
    } else {
      // 新增物件
      await addProperty(propertyData);
    }
    // 重新獲取所有物件
    await fetchProperties();
    // 返回物件列表
    cancelEdit();
  } catch (err) {
    console.error('保存物件失敗:', err);
    error.value = '保存物件失敗，請稍後再試。';
  } finally {
    loading.value = false;
  }
}

// 刪除物件
async function deleteProperty(propertyId) {
  loading.value = true;
  error.value = null;
  try {
    await apiDeleteProperty(propertyId);
    await fetchProperties();
  } catch (err) {
    console.error(`刪除物件 ${propertyId} 失敗:`, err);
    error.value = '刪除物件失敗，請稍後再試。';
  } finally {
    loading.value = false;
  }
}

// 取消編輯並返回物件列表
function cancelEdit() {
  showPropertyForm.value = false;
  showAssetsList.value = false;
  showRepairsList.value = false;
  showPropertyDetail.value = false;
  selectedProperty.value = null;
  selectedPropertyId.value = null;
}

// 返回物件列表
function backToProperties() {
  cancelEdit();
}
</script>

<style scoped>
.properties-view {
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.loading {
  text-align: center;
  padding: 1rem;
  color: #666;
}

.error {
  background-color: #ffebee;
  color: #c62828;
  padding: 0.8rem;
  border-radius: 4px;
  margin: 1rem 0;
  border-left: 4px solid #c62828;
}
</style>