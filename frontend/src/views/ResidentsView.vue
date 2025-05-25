<template>
  <div class="residents-view">
    <!-- <div class="header-row"> -->
    <div class="page-title">
      <h1>承租人管理</h1>
      <!-- 新增承租人按鈕 -->
      <button @click="addResident" class="btn btn-success">
        <i class="fas fa-user-plus"></i> 新增承租人
      </button>
    </div>
    <!-- 新增/編輯承租人表單或彈窗 -->
    <ResidentForm v-if="showForm" :resident="currentResident" @save="saveResident" @cancel="cancelForm" />
    <!-- 承租人列表 -->
    <table>
      <thead>
        <tr>
          <th>物業 ID</th>
          <th>合約 ID</th>
          <th>姓名</th>
          <th>身份證字號</th>
          <th>連絡電話</th>
          <th>工作</th>
          <th>緊急聯絡人</th>
          <th>緊急聯絡電話</th>
          <th>關係</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <!-- 這裡將顯示承租人資料 -->
        <tr v-for="resident in residents" :key="resident.id">
          <td>{{ resident.property_id }}</td>
          <td>{{ resident.contract_id }}</td>
          <td>{{ resident.name }}</td>
          <td>{{ resident.id_number }}</td>
          <td>{{ resident.phone }}</td>
          <td>{{ resident.job }}</td>
          <td>{{ resident.emergency_contact_name }}</td>
          <td>{{ resident.emergency_contact_phone }}</td>
          <td>{{ resident.emergency_contact_relationship }}</td>
          <td>
            <button @click="editResident(resident.id)" class="btn btn-warning btn-sm">
              <i class="fas fa-edit"></i> 編輯
            </button>
            <button @click="deleteResident(resident.id)" class="btn btn-danger btn-sm">
              <i class="fas fa-trash"></i> 刪除
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import ResidentForm from '@/components/ResidentForm.vue';
import { getResidents, addResident as apiAddResident, updateResident as apiUpdateResident, deleteResident as apiDeleteResident } from '@/services/api'; // 引入 API 服務

const residents = ref([]);
const showForm = ref(false);
const currentResident = ref(null);

const fetchResidents = async () => {
  try {
    const response = await fetch('http://localhost:8000/residents/');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    residents.value = await response.json();
  } catch (error) {
    console.error('Error fetching residents:', error);
  }
};

onMounted(() => {
  fetchResidents();
});

const addResident = () => {
  console.log('新增承租人');
  showForm.value = true;
  currentResident.value = null;
};

const editResident = (id) => {
  console.log('編輯承租人:', id);
  showForm.value = true;
  currentResident.value = residents.value.find(r => r.id === id);
};

const deleteResident = async (id) => {
  console.log('刪除承租人:', id);
  if (confirm('確定要刪除此承租人嗎？')) {
    try {
      await apiDeleteResident(id);
      fetchResidents(); // 刪除成功後重新載入列表
    } catch (error) {
      console.error('刪除承租人失敗:', error);
    }
  }
};

const saveResident = async (residentData) => {
  console.log('儲存承租人:', residentData);
  try {
    if (residentData.id) {
      // 編輯現有承租人
      await apiUpdateResident(residentData.id, residentData);
    } else {
      // 新增承租人
      await apiAddResident(residentData);
    }
    showForm.value = false;
    currentResident.value = null;
    fetchResidents(); // 儲存成功後重新載入列表
  } catch (error) {
    console.error('儲存承租人失敗:', error);
  }
};

const cancelForm = () => {
  showForm.value = false;
  currentResident.value = null;
};
</script>

<style scoped>
.residents-view {
  padding: 1rem;
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

button {
  margin-right: 5px;
}
</style>