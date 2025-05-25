<template>
  <div class="property-form">
    <h3><i class="fas fa-building"></i> {{ isEdit ? '編輯物件' : '新增物件' }}</h3>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="address"><i class="fas fa-map-marker-alt"></i> 物件地址 *</label>
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
        <label for="size_sq_ft"><i class="fas fa-ruler-combined"></i> 物件坪數 *</label>
        <div class="input-with-icon">
          <input 
            id="size_sq_ft" 
            v-model="formData.size_sq_ft" 
            type="text" 
            class="form-control" 
            required
            placeholder="請輸入物件坪數，可包括主建物、附屬建物等細項面積"
          />
          <span class="input-append">坪</span>
        </div>
      </div>

      <div class="form-group">
        <label for="features"><i class="fas fa-list-ul"></i> 物件特色</label>
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

.form-text {
  display: block;
  margin-top: var(--spacing-xs);
  font-size: 0.85rem;
}

.text-muted {
  color: var(--text-light);
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
