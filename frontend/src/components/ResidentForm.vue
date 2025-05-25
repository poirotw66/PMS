<template>
  <div class="resident-form">
    <h3><i class="fas fa-user-alt"></i> {{ resident ? '編輯承租人' : '新增承租人' }}</h3>
    <form @submit.prevent="save">
      <div class="form-row">
        <div class="form-group form-group-large">
          <label for="name"><i class="fas fa-user"></i> 姓名:</label>
          <input type="text" id="name" v-model="formData.name" class="form-control" required placeholder="請輸入承租人姓名">
        </div>
        <div class="form-group">
          <label for="id_number"><i class="fas fa-id-card"></i> 身份證字號:</label>
          <input type="text" id="id_number" v-model="formData.id_number" class="form-control" required placeholder="請輸入身份證字號">
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="phone"><i class="fas fa-phone"></i> 連絡電話:</label>
          <input type="text" id="phone" v-model="formData.phone" class="form-control" required placeholder="請輸入聯絡電話">
        </div>
        <div class="form-group">
          <label for="email"><i class="fas fa-envelope"></i> 電子郵件:</label>
          <input type="email" id="email" v-model="formData.email" class="form-control" placeholder="請輸入電子郵件">
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="property_id"><i class="fas fa-building"></i> 物業 ID:</label>
          <input type="text" id="property_id" v-model="formData.property_id" class="form-control" placeholder="請輸入物業 ID">
        </div>
        <div class="form-group">
          <label for="contract_id"><i class="fas fa-file-contract"></i> 合約 ID:</label>
          <input type="text" id="contract_id" v-model="formData.contract_id" class="form-control" placeholder="請輸入合約 ID">
        </div>
      </div>
      
      <div class="form-group">
        <label for="job"><i class="fas fa-briefcase"></i> 工作:</label>
        <input type="text" id="job" v-model="formData.job" class="form-control" placeholder="請輸入職業資訊">
      </div>
      
      <fieldset class="form-section">
        <legend><i class="fas fa-first-aid"></i> 緊急聯絡人資訊</legend>
        <div class="form-row">
          <div class="form-group">
            <label for="emergency_contact_name">緊急聯絡人姓名:</label>
            <input type="text" id="emergency_contact_name" v-model="formData.emergency_contact_name" class="form-control" placeholder="請輸入緊急聯絡人姓名">
          </div>
          <div class="form-group">
            <label for="emergency_contact_phone">緊急聯絡人電話:</label>
            <input type="text" id="emergency_contact_phone" v-model="formData.emergency_contact_phone" class="form-control" placeholder="請輸入緊急聯絡人電話">
          </div>
        </div>
        <div class="form-group">
          <label for="emergency_contact_relationship">緊急聯絡人關係:</label>
          <input type="text" id="emergency_contact_relationship" v-model="formData.emergency_contact_relationship" class="form-control" placeholder="請輸入與緊急聯絡人的關係">
        </div>
      </fieldset>
      
      <div class="form-actions">
        <button type="submit" class="btn btn-primary">
          <i class="fas fa-save"></i> 儲存
        </button>
        <button type="button" class="btn btn-secondary" @click="cancel">
          <i class="fas fa-times"></i> 取消
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  resident: { // 如果有 resident prop，表示是編輯模式
    type: Object,
    default: null
  }
});

const emit = defineEmits(['save', 'cancel']);

const formData = ref({
  name: '',
  id_number: '', // 將 idNumber 改為 id_number
  phone: '',
  email: '', // 新增 email 欄位
  job: '',
  emergency_contact_name: '',
  emergency_contact_phone: '',
  emergency_contact_relationship: '',
  property_id: '', // 新增 property_id 欄位
  contract_id: '' // 新增 contract_id 欄位
});

// 當 resident prop 改變時，更新表單資料 (用於編輯模式)
watch(() => props.resident, (newResident) => {
  if (newResident) {
    formData.value = { ...newResident };
  } else {
    // 重置表單 (用於新增模式)
    formData.value = {
      name: '',
      id_number: '', // 將 idNumber 改為 id_number
      phone: '',
      email: '', // 新增 email 欄位
      job: '',
      emergency_contact_name: '',
      emergency_contact_phone: '',
      emergency_contact_relationship: '',
  property_id: '', // 新增 property_id 欄位
  contract_id: '' // 新增 contract_id 欄位
    };
  }
}, { immediate: true });

const save = () => {
  emit('save', formData.value);
};

const cancel = () => {
  emit('cancel');
};
</script>

<style scoped>
.resident-form {
  padding: var(--spacing-md);
  background-color: var(--bg-color);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  margin-bottom: var(--spacing-md);
}

.form-group {
  margin-bottom: var(--spacing-md);
  flex: 1;
  min-width: 250px;
}

.form-group-large {
  flex: 2;
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-md);
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

.form-section {
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.form-section legend {
  padding: 0 var(--spacing-sm);
  font-weight: 500;
  color: var(--primary-color);
}

.form-actions {
  display: flex;
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5em;
  padding: 0.6em 1.5em;
  border: none;
  border-radius: 24px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(52, 152, 219, 0.08);
  transition: background 0.2s, color 0.2s, box-shadow 0.2s, transform 0.15s;
}

.btn-primary {
  background: linear-gradient(90deg, var(--primary-color) 60%, var(--primary-dark) 100%);
  color: #fff;
}
.btn-primary:hover {
  background: linear-gradient(90deg, var(--primary-dark) 60%, var(--primary-color) 100%);
  box-shadow: 0 4px 16px rgba(52, 152, 219, 0.18);
  transform: translateY(-2px) scale(1.03);
}

.btn-secondary {
  background: linear-gradient(90deg, var(--bg-light) 60%, var(--bg-dark) 100%);
  color: var(--text-color);
  border: 1px solid var(--border-color);
}
.btn-secondary:hover {
  background: var(--bg-dark);
  color: var(--primary-color);
  box-shadow: 0 2px 8px rgba(52, 152, 219, 0.10);
  transform: translateY(-1px) scale(1.02);
}

.btn i {
  font-size: 1.1em;
  margin-right: 0.3em;
}

/* Form utility classes */
::placeholder {
  color: var(--text-lighter);
  opacity: 0.7;
}
</style>