<template>
  <div class="repair-form">
    <h3><i class="fas fa-tools"></i> {{ isEdit ? '編輯維修請求' : '新增維修請求' }}</h3>
    <form @submit.prevent="handleSubmit">
      <div class="form-row">
        <div class="form-group">
          <label for="tenant_id"><i class="fas fa-user"></i> 報修人 ID *</label>
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
          <label for="request_date"><i class="fas fa-calendar-day"></i> 報修日期 *</label>
          <input 
            id="request_date" 
            v-model="formData.request_date" 
            type="date" 
            class="form-control"
            required
          />
        </div>
      </div>

      <div class="form-group">
        <label for="description"><i class="fas fa-clipboard-list"></i> 維修項目/工作內容 *</label>
        <textarea 
          id="description" 
          v-model="formData.description" 
          class="form-control" 
          rows="3"
          required
          placeholder="請詳細描述損壞情況及需要進行的維修工作"
        ></textarea>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="repair_vendor"><i class="fas fa-hard-hat"></i> 維修廠商/人員</label>
          <input 
            id="repair_vendor" 
            v-model="formData.repair_vendor" 
            type="text" 
            class="form-control"
            placeholder="請輸入執行維修的單位或人員名稱及聯絡方式"
          />
        </div>

        <div class="form-group">
          <label for="repair_cost"><i class="fas fa-dollar-sign"></i> 維修費用</label>
          <div class="input-with-icon">
            <input 
              id="repair_cost" 
              v-model="formData.repair_cost" 
              type="text" 
              class="form-control"
              placeholder="請輸入該次維修所產生的總費用"
            />
            <span class="input-append">元</span>
          </div>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="cost_bearer"><i class="fas fa-money-check-alt"></i> 費用承擔方</label>
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
          <label for="resolution_date"><i class="fas fa-calendar-check"></i> 結案日期</label>
          <input 
            id="resolution_date" 
            v-model="formData.resolution_date" 
            type="date" 
            class="form-control"
          />
        </div>
      </div>

      <div class="form-group">
        <label for="resolution_method"><i class="fas fa-clipboard-check"></i> 結案方式 (修繕方式及費用)</label>
        <textarea 
          id="resolution_method" 
          v-model="formData.resolution_method" 
          class="form-control" 
          rows="2"
          placeholder="請輸入修繕方式及費用"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="remarks"><i class="fas fa-comment-dots"></i> 備註</label>
        <textarea 
          id="remarks" 
          v-model="formData.remarks" 
          class="form-control" 
          rows="2"
          placeholder="可記錄維修後的使用狀況或保固資訊"
        ></textarea>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary">
          <i class="fas fa-{{ isEdit ? 'save' : 'plus-circle' }}"></i> {{ isEdit ? '更新' : '新增' }}
        </button>
        <button type="button" class="btn btn-secondary" @click="cancelForm">
          <i class="fas fa-times"></i> 取消
        </button>
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
  padding: var(--spacing-md);
  background-color: var(--bg-color);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  margin-bottom: var(--spacing-md);
}

.form-group {
  margin-bottom: var(--spacing-md);
}

.form-group label {
  display: block;
  margin-bottom: var(--spacing-xs);
  font-weight: 500;
  color: var(--text-color);
}

.form-control {
  display: block;
  width: 100%;
  padding: var(--spacing-sm);
  font-size: 1rem;
  line-height: 1.5;
  color: var(--text-color);
  background-color: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  transition: var(--transition);
}

.form-control:focus {
  border-color: var(--primary-color);
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.form-group {
  flex: 1;
  min-width: 250px;
}

.input-with-icon {
  position: relative;
}

.input-append {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-light);
  font-size: 0.9rem;
}

.form-actions {
  display: flex;
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
}

/* Form utility classes */
::placeholder {
  color: var(--text-lighter);
  opacity: 0.7;
}
</style>
