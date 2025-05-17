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
        <tr v-for="customer in potentialCustomers" :key="customer.name">
          <td>{{ customer.name }}</td>
          <td>{{ customer.phone }}</td>
          <td>{{ customer.requirements }}</td>
          <td>{{ customer.job }}</td>
          <td>{{ customer.move_in_date }}</td>
          <td>{{ customer.viewing_records }}</td>
          <td>{{ customer.status }}</td>
          <td>
            <button>編輯</button>
            <button>刪除</button>
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

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/potential-customers');
    potentialCustomers.value = response.data;
  } catch (error) {
    console.error('Error fetching potential customers:', error);
  }
});
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