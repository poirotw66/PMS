<template>
  <div>
    <h2>潛在客戶列表</h2>
    <table>
      <thead>
        <tr>
          <th>客戶姓名</th>
          <th>聯絡電話</th>
          <th>客戶需求</th>
          <th>客戶工作內容</th>
          <th>預計入住日期</th>
          <th>看房紀錄</th>
          <th>追蹤狀態</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="customer in potentialCustomers" :key="customer.id">
          <td>{{ customer.name }}</td>
          <td>{{ customer.phone }}</td>
          <td>{{ customer.needs }}</td>
          <td>{{ customer.job }}</td>
          <td>{{ customer.move_in_date }}</td>
          <td>{{ customer.viewing_records }}</td>
          <td>{{ customer.status }}</td>
          <td>
            <button @click="$emit('edit-customer', customer)">編輯</button>
            <button @click="deleteCustomer(customer.id)">刪除</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const potentialCustomers = ref([]);

const fetchCustomers = async () => {
  try {
    const response = await axios.get('http://localhost:8000/potential-customers');
    potentialCustomers.value = response.data;
    console.log('Fetched customers data structure:', response.data);
    // Add a log to check the id of each customer
    potentialCustomers.value.forEach(customer => {
      console.log('Customer ID:', customer.id);
    });
  } catch (error) {
    console.error('Error fetching potential customers:', error);
  } finally {
    console.log('Fetched customers:', potentialCustomers.value);
  }
};

const deleteCustomer = async (customerId) => {
  console.log('Attempting to delete customer with ID:', customerId); // Add this line
  if (customerId === undefined || customerId === null) {
    console.error('Cannot delete customer: customer ID is undefined or null.');
    return; // Stop execution if ID is invalid
  }
  try {
    await axios.delete(`http://localhost:8000/potential-customers/${customerId}`);
    potentialCustomers.value = potentialCustomers.value.filter(customer => customer.id !== customerId);
    console.log(`Customer with ID ${customerId} deleted successfully.`);
  } catch (error) {
    console.error(`Error deleting customer with ID ${customerId}:`, error);
  }
};

onMounted(() => {
  fetchCustomers();
});

import { defineExpose } from 'vue';
defineExpose({ fetchCustomers });
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
th {
  background-color: #f2f2f2;
}
</style>