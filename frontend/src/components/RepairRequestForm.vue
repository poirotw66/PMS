<template>
  <div class="repair-form">
    <h3>{{ isEdit ? '編輯維修請求' : '新增維修請求' }}</h3>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="tenant_id">報修人 ID *</label>
        <input 
          id="tenant_id" 
          v-model.number="formData.tenant_id" 
          type="number" 
          class="form-control" 
          required
          placeholder="請輸入承租人 ID"
        />
      </div>

      <div class="form-group">
        <label for="request_date">報修日期 *</label>
        <input 
          id="request_date" 
          v-model="formData.request_date" 
          type="date" 
          class="form-control"
          required
        />
      </div>

      <div class="form-group">
        <label for="description">維修項目/工作內容 *</label>
        <textarea 
          id="description" 
          v-model="formData.description" 
          class="form-control" 
          rows="3"
          required
          placeholder="請詳細描述損壞情況及需要進行的維修工作"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="repair_vendor">維修廠商/人員</label>
        <input 
          id="repair_vendor" 
          v-model="formData.repair_vendor" 
          type="text" 
          class="form-control"
          placeholder="請輸入執行維修的單位或人員名稱及聯絡方式"
        />
      </div>

      <div class="form-group">
        <label for="repair_cost">維修費用</label>
        <input 
          id="repair_cost" 
          v-model="formData.repair_cost" 
          type="text" 
          class="form-control"
          placeholder="請輸入該次維修所產生的總費用"
        />
      </div>

      <div class="form-group">
        <label for="cost_bearer">費用承擔方</label>
        <select
          id="cost_bearer"
          v-model="formData.cost_bearer"
          class="form-control"
        >
          <option value="房東">房東</option>
          <option value="承租人">承租人</option>
          <option value="共同分擔">共同分擔</option>
        </select>
      </div>

      <div class="form-group">
        <label for="resolution_method">結案方式 (修繕方式及費用)</label>
        <textarea 
          id="resolution_method" 
          v-model="formData.resolution_method" 
          class="form-control" 
          rows="2"
          placeholder="請輸入修繕方式及費用"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="resolution_date">結案日期</label>
        <input 
          id="resolution_date" 
          v-model="formData.resolution_date" 
          type="date" 
          class="form-control"
        />
      </div>

      <div class="form-group">
        <label for="remarks">備註</label>
        <textarea 
          id="remarks" 
          v-model="formData.remarks" 
          class="form-control" 
          rows="2"
          placeholder="可記錄維修後的使用狀況或保固資訊"
        ></textarea>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary">{{ isEdit ? '更新' : '新增' }}</button>
        <button type="button" class="btn btn-secondary" @click="cancelForm">取消</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from 'vue';

const props = defineProps({
  propertyId: {
    type: Number,
    required: true
  },
  request: {
    type: Object,
    default: () => ({
      property_id: null,
      tenant_id: null,
      request_date: new Date().toISOString().split('T')[0], // 預設為今天
      description: '',
      repair_vendor: '',
      repair_cost: '',
      cost_bearer: '房東',
      resolution_method: '',
      resolution_date: '',
      remarks: ''
    })
  },
  isEdit: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['submit', 'cancel']);

const formData = ref({
  property_id: null,
  tenant_id: null,
  request_date: new Date().toISOString().split('T')[0], // 預設為今天
  description: '',
  repair_vendor: '',
  repair_cost: '',
  cost_bearer: '房東',
  resolution_method: '',
  resolution_date: '',
  remarks: ''
});

// 當 request 變更時更新表單資料
watch(() => props.request, (newVal) => {
  if (newVal) {
    formData.value = { ...newVal };
  }
}, { immediate: true, deep: true });

// 當 propertyId 變更時更新表單的 property_id
watch(() => props.propertyId, (newVal) => {
  if (newVal) {
    formData.value.property_id = newVal;
  }
}, { immediate: true });

const handleSubmit = () => {
  emit('submit', { ...formData.value });
};

const cancelForm = () => {
  emit('cancel');
};
</script>

<style scoped>
.repair-form {
  padding: 1rem;
  background-color: #f9f9f9;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
}
</style>
