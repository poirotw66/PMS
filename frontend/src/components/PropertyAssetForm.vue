<template>
  <div class="asset-form">
    <h3><i class="fas fa-box"></i> {{ isEdit ? '編輯資產' : '新增資產' }}</h3>
    <form @submit.prevent="handleSubmit">
      <div class="form-row">
        <div class="form-group form-group-large">
          <label for="name"><i class="fas fa-tag"></i> 資產名稱/品牌/型號 *</label>
          <input 
            id="name" 
            v-model="formData.name" 
            type="text" 
            class="form-control" 
            required
            placeholder="請輸入資產名稱、品牌及型號，例如：國際牌冷氣 CS-K28BA2"
          />
          <small class="form-text text-muted">
            家電類：洗衣機、冰箱、電視、冷氣機、熱水器等<br>
            傢俱類：書桌、椅子、衣櫃、床架、床墊、沙發等
          </small>
        </div>

        <div class="form-group">
          <label for="asset_type"><i class="fas fa-th-list"></i> 資產類型</label>
          <select
            id="asset_type"
            v-model="formData.asset_type"
            class="form-control"
          >
            <option value="家電類">家電類</option>
            <option value="傢俱類">傢俱類</option>
            <option value="其他">其他</option>
          </select>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="purchase_date"><i class="fas fa-calendar-alt"></i> 購買日期</label>
          <input 
            id="purchase_date" 
            v-model="formData.purchase_date" 
            type="date" 
            class="form-control"
            placeholder="YYYY-MM-DD"
          />
        </div>

        <div class="form-group">
          <label for="purchase_price"><i class="fas fa-dollar-sign"></i> 購買價格</label>
          <div class="input-with-icon">
            <input 
              id="purchase_price" 
              v-model="formData.purchase_price" 
              type="text" 
              class="form-control"
              placeholder="請輸入購買價格"
            />
            <span class="input-append">元</span>
          </div>
        </div>
      </div>

      <div class="form-group">
        <label for="purchase_vendor"><i class="fas fa-store"></i> 購買廠商/電話</label>
        <input 
          id="purchase_vendor" 
          v-model="formData.purchase_vendor" 
          type="text" 
          class="form-control"
          placeholder="請輸入購買廠商名稱及聯絡電話"
        />
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="warranty_period"><i class="fas fa-shield-alt"></i> 保固期間</label>
          <input 
            id="warranty_period" 
            v-model="formData.warranty_period" 
            type="text" 
            class="form-control"
            placeholder="例如：1年、2年、終身"
          />
        </div>

        <div class="form-group">
          <label for="current_status"><i class="fas fa-info-circle"></i> 目前狀態</label>
          <select
            id="current_status"
            v-model="formData.current_status"
            class="form-control"
          >
            <option value="良好">良好</option>
            <option value="待修">待修</option>
            <option value="已報廢">已報廢</option>
          </select>
        </div>
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
  asset: {
    type: Object,
    default: () => ({
      property_id: null,
      name: '',
      asset_type: '家電類',
      purchase_date: '',
      purchase_price: '',
      purchase_vendor: '',
      warranty_period: '',
      current_status: '良好'
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
  name: '',
  asset_type: '家電類',
  purchase_date: '',
  purchase_price: '',
  purchase_vendor: '',
  warranty_period: '',
  current_status: '良好'
});

// 當 asset 變更時更新表單資料
watch(() => props.asset, (newVal) => {
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
.asset-form {
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

.form-group-large {
  flex: 2;
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
