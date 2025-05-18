<template>
  <div class="potential-customers">
    <h1>潛在客戶管理</h1>
    <!-- Future content for listing and managing potential customers -->
    <button @click="showAddForm">新增客戶</button>

    <div v-if="showForm">
      <h2>{{ isEditing ? '編輯客戶' : '新增客戶' }}</h2>
      <form @submit.prevent="handleSubmit">
        <div>
          <label for="name">客戶姓名:</label>
          <input type="text" id="name" v-model="currentCustomer.name" required>
        </div>
        <div>
          <label for="phone">聯絡電話:</label>
          <input type="text" id="phone" v-model="currentCustomer.phone">
        </div>
        <div>
          <label for="needs">客戶需求:</label>
          <textarea id="needs" v-model="currentCustomer.needs"></textarea>
        </div>
        <div>
          <label for="job">客戶工作內容:</label>
          <input type="text" id="job" v-model="currentCustomer.job">
        </div>
        <div>
          <label for="move_in_date">預計入住日期:</label>
          <input type="date" id="move_in_date" v-model="currentCustomer.move_in_date">
        </div>
        <div>
          <label for="viewing_records">看房紀錄:</label>
          <textarea id="viewing_records" v-model="currentCustomer.viewing_records"></textarea>
        </div>
        <div>
          <label for="status">追蹤狀態:</label>
          <input type="text" id="status" v-model="currentCustomer.status">
        </div>
        <button type="submit">儲存</button>
        <button type="button" @click="cancelForm">取消</button>
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
/* Component-specific styles will be added here later */
</style>