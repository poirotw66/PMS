<template>
  <div class="property-form">
    <h3>{{ isEdit ? '編輯物件' : '新增物件' }}</h3>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="address">物件地址 *</label>
        <input 
          id="address" 
          v-model="formData.address" 
          type="text" 
          class="form-control" 
          required
          placeholder="請輸入完整物件地址，包括縣市、鄉鎮市區、街道名稱、門牌號碼、樓層及戶號"
        />
      </div>

      <div class="form-group">
        <label for="size_sq_ft">物件坪數 *</label>
        <input 
          id="size_sq_ft" 
          v-model="formData.size_sq_ft" 
          type="text" 
          class="form-control" 
          required
          placeholder="請輸入物件坪數，可包括主建物、附屬建物等細項面積"
        />
      </div>

      <div class="form-group">
        <label for="features">物件特色</label>
        <textarea 
          id="features" 
          v-model="formData.features" 
          class="form-control" 
          rows="3"
          placeholder="請描述物件特色，如內部格局、位置樓層、其他設施等"
        ></textarea>
        <small class="form-text text-muted">
          可包括：內部格局(陽台、房間數量、衛浴數量、廚房)、位置樓層(樓層、電梯、景觀)、
          其他設施(停車位、社區公共設施、寵物政策)等
        </small>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary">{{ isEdit ? '更新' : '新增' }}</button>
        <button type="button" class="btn btn-secondary" @click="cancelForm">取消</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, watch, computed, defineProps, defineEmits } from 'vue';

const props = defineProps({
  property: {
    type: Object,
    default: () => null
  }
});

const emit = defineEmits(['save', 'cancel']);

const formData = ref({
  address: '',
  size_sq_ft: '',
  features: ''
});

// 當 property 變更時更新表單資料
watch(() => props.property, (newVal) => {
  if (newVal) {
    formData.value = { ...newVal };
  } else {
    // 如果是新增物件，重置表單
    formData.value = {
      address: '',
      size_sq_ft: '',
      features: ''
    };
  }
}, { immediate: true, deep: true });

const isEdit = computed(() => !!props.property?.id);

const handleSubmit = () => {
  emit('save', { ...formData.value });
};

const cancelForm = () => {
  emit('cancel');
};
</script>

<style scoped>
.property-form {
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

.form-text {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.85rem;
}

.text-muted {
  color: #6c757d;
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
