<template>
  <div class="resident-form">
    <h2>{{ resident ? '編輯承租人' : '新增承租人' }}</h2>
    <form @submit.prevent="save">
      <div>
        <label for="name">姓名:</label>
        <input type="text" id="name" v-model="formData.name" required>
      </div>
      <div>
        <label for="id_number">身份證字號:</label>
        <input type="text" id="id_number" v-model="formData.id_number" required>
      </div>
      <div>
        <label for="phone">連絡電話:</label>
        <input type="text" id="phone" v-model="formData.phone" required>
      </div>
      <div>
        <label for="email">電子郵件:</label>
        <input type="email" id="email" v-model="formData.email">
      </div>
      <div>
        <label for="property_id">物業 ID:</label>
        <input type="text" id="property_id" v-model="formData.property_id">
      </div>
      <div>
        <label for="contract_id">合約 ID:</label>
        <input type="text" id="contract_id" v-model="formData.contract_id">
      </div>
      <div>
        <label for="job">工作:</label>
        <input type="text" id="job" v-model="formData.job">
      </div>
      <div>
        <label for="emergency_contact_name">緊急聯絡人姓名:</label>
        <input type="text" id="emergency_contact_name" v-model="formData.emergency_contact_name">
      </div>
      <div>
        <label for="emergency_contact_phone">緊急聯絡人電話:</label>
        <input type="text" id="emergency_contact_phone" v-model="formData.emergency_contact_phone">
      </div>
      <div>
        <label for="emergency_contact_relationship">緊急聯絡人關係:</label>
        <input type="text" id="emergency_contact_relationship" v-model="formData.emergency_contact_relationship">
      </div>
      <button type="submit">儲存</button>
      <button type="button" @click="cancel">取消</button>
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
  margin-top: 1rem;
  padding: 1rem;
  border: 1px solid #ccc;
}

.resident-form h2 {
  margin-top: 0;
}

.resident-form div {
  margin-bottom: 10px;
}

.resident-form label {
  display: inline-block;
  width: 120px;
  margin-right: 10px;
}

.resident-form input {
  padding: 5px;
}

.resident-form button {
  margin-right: 10px;
}
</style>