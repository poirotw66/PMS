<template>
  <div class="asset-form">
    <h3>{{ isEdit ? '編輯資產' : '新增資產' }}</h3>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="name">資產名稱/品牌/型號 *</label>
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
        <label for="asset_type">資產類型</label>
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

      <div class="form-group">
        <label for="purchase_date">購買日期</label>
        <input 
          id="purchase_date" 
          v-model="formData.purchase_date" 
          type="date" 
          class="form-control"
          placeholder="YYYY-MM-DD"
        />
      </div>

      <div class="form-group">
        <label for="purchase_price">購買價格</label>
        <input 
          id="purchase_price" 
          v-model="formData.purchase_price" 
          type="text" 
          class="form-control"
          placeholder="請輸入購買價格，例如：15000元"
        />
      </div>

      <div class="form-group">
        <label for="purchase_vendor">購買廠商/電話</label>
        <input 
          id="purchase_vendor" 
          v-model="formData.purchase_vendor" 
          type="text" 
          class="form-control"
          placeholder="請輸入購買廠商名稱及聯絡電話"
        />
      </div>

      <div class="form-group">
        <label for="warranty_period">保固期間</label>
        <input 
          id="warranty_period" 
          v-model="formData.warranty_period" 
          type="text" 
          class="form-control"
          placeholder="例如：1年、2年、終身"
        />
      </div>

      <div class="form-group">
        <label for="current_status">目前狀態</label>
        <input 
          id="current_status" 
          v-model="formData.current_status" 
          type="text" 
          class="form-control"
          placeholder="請描述資產目前的使用狀態，例如：良好、待修、已報廢"
        />
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
