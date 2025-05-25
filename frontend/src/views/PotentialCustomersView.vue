<template>
  <div class="potential-customers">
    <div class="page-title header-row">
      <h1>潛在客戶管理</h1>
      <button @click="showAddForm" class="btn btn-success">
        <i class="fas fa-user-plus"></i> 新增客戶
      </button>
    </div>
    <div v-if="showForm" class="customer-form-card card">
      <h2 class="form-title">{{ isEditing ? '編輯客戶' : '新增客戶' }}</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-row">
          <div class="form-group">
            <label for="name"><i class="fas fa-user"></i> 客戶姓名:</label>
            <input type="text" id="name" v-model="currentCustomer.name" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="phone"><i class="fas fa-phone"></i> 聯絡電話:</label>
            <input type="text" id="phone" v-model="currentCustomer.phone" class="form-control">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label for="needs"><i class="fas fa-list"></i> 客戶需求:</label>
            <textarea id="needs" v-model="currentCustomer.needs" class="form-control"></textarea>
          </div>
          <div class="form-group">
            <label for="job"><i class="fas fa-briefcase"></i> 客戶工作內容:</label>
            <input type="text" id="job" v-model="currentCustomer.job" class="form-control">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label for="move_in_date"><i class="fas fa-calendar-alt"></i> 預計入住日期:</label>
            <input type="date" id="move_in_date" v-model="currentCustomer.move_in_date" class="form-control">
          </div>
          <div class="form-group">
            <label for="viewing_records"><i class="fas fa-eye"></i> 看房紀錄:</label>
            <textarea id="viewing_records" v-model="currentCustomer.viewing_records" class="form-control"></textarea>
          </div>
          <div class="form-group">
            <label for="status"><i class="fas fa-flag"></i> 追蹤狀態:</label>
            <input type="text" id="status" v-model="currentCustomer.status" class="form-control">
          </div>
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">
            <i class="fas fa-save"></i> 儲存
          </button>
          <button type="button" @click="cancelForm" class="btn btn-secondary">
            <i class="fas fa-times"></i> 取消
          </button>
        </div>
      </form>
    </div>

    <PotentialCustomerList @edit-customer="editCustomer" @customer-deleted="handleCustomerDeleted" ref="customerListRef"/>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import PotentialCustomerList from '../components/PotentialCustomerList.vue';
import axios from 'axios'; // Import axios

const showForm = ref(false);
const isEditing = ref(false);
const currentCustomer = ref({
  id: null, // Add id field for editing
  name: '',
  phone: '',
  needs: '',
  job: '',
  move_in_date: '', // Added field
  viewing_records: '', // Added field
  status: '' // Added field
});

const customerListRef = ref(null);

const showAddForm = () => {
  isEditing.value = false;
  currentCustomer.value = {
    id: null,
    name: '',
    phone: '',
    needs: '',
    job: '',
    move_in_date: '', // Added field
    viewing_records: '', // Added field
    status: '' // Added field
  };
  showForm.value = true;
};

const editCustomer = (customer) => {
  isEditing.value = true;
    currentCustomer.value = { ...customer }; // Ensure all fields are mapped for editing
  showForm.value = true;
};

const cancelForm = () => {
  showForm.value = false;
};

const handleSubmit = async () => {
  try {
    if (isEditing.value) {
      // Update existing customer
      await axios.put(`http://localhost:8000/potential-customers/${currentCustomer.value.id}`, currentCustomer.value);
      console.log('Customer updated successfully:', currentCustomer.value);
    } else {
      // Add new customer
      // Prepare data for POST request, excluding 'id'
      const { id, ...customerData } = currentCustomer.value;
      await axios.post('http://localhost:8000/potential-customers/', customerData);
      console.log('Customer added successfully:', customerData);
    }
    // After submission, hide form and refresh list
    showForm.value = false;
    if (customerListRef.value && customerListRef.value.fetchCustomers) {
      customerListRef.value.fetchCustomers();
    }
  } catch (error) {
    console.error('Error submitting customer:', error);
    // Optionally show an error message to the user
  }
};

const handleCustomerDeleted = () => {
  // This method will be called by PotentialCustomerList after a customer is deleted
  // We might not need to do anything here if the list component handles its own refresh
  console.log('Customer deleted, refreshing list if needed.');
};

</script>

<style scoped>
.potential-customers {
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.page-title h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
}
.customer-form-card.card {
  background: var(--bg-color);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  padding: 2rem 1.5rem 1.5rem 1.5rem;
  margin-bottom: 2rem;
  animation: fadeIn 0.3s;
}
.form-title {
  margin-bottom: 1rem;
  color: var(--primary-color);
  font-size: 1.3rem;
  font-weight: 600;
}
.form-row {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}
.form-group {
  flex: 1;
  min-width: 220px;
  margin-bottom: var(--spacing-md);
}
.form-actions {
  display: flex;
  gap: var(--spacing-md);
  margin-top: 1rem;
}
.card {
  background: var(--bg-color);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: none; }
}
</style>