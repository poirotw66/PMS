import axios from 'axios';

// 假設後端 API 的基礎 URL
// 在實際部署時，這應該從環境變數中讀取
const API_BASE_URL = 'http://localhost:8000'; // 請根據實際後端地址修改

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 承租人相關 API 呼叫
export const getResidents = async () => {
  try {
    const response = await api.get('/residents/');
    return response.data;
  } catch (error) {
    console.error('Error fetching residents:', error);
    throw error;
  }
};

export const addResident = async (residentData) => {
  try {
    const response = await api.post('/residents/', residentData);
    return response.data;
  } catch (error) {
    console.error('Error adding resident:', error);
    throw error;
  }
};

export const updateResident = async (id, residentData) => {
  try {
    const response = await api.put(`/residents/${id}`, residentData);
    return response.data;
  } catch (error) {
    console.error(`Error updating resident ${id}:`, error);
    throw error;
  }
};

export const deleteResident = async (id) => {
  try {
    const response = await api.delete(`/residents/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting resident ${id}:`, error);
    throw error;
  }
};

// 其他模組的 API 呼叫可以在這裡新增
// export const getProperties = async () => { ... };
// export const addProperty = async (propertyData) => { ... };

export default api;