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

// 物件管理相關 API 呼叫
export const getProperties = async () => {
  try {
    const response = await api.get('/properties/');
    return response.data;
  } catch (error) {
    console.error('Error fetching properties:', error);
    throw error;
  }
};

export const getPropertyById = async (id) => {
  try {
    const response = await api.get(`/properties/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching property ${id}:`, error);
    throw error;
  }
};

export const addProperty = async (propertyData) => {
  try {
    const response = await api.post('/properties/', propertyData);
    return response.data;
  } catch (error) {
    console.error('Error adding property:', error);
    throw error;
  }
};

export const updateProperty = async (id, propertyData) => {
  try {
    const response = await api.put(`/properties/${id}`, propertyData);
    return response.data;
  } catch (error) {
    console.error(`Error updating property ${id}:`, error);
    throw error;
  }
};

export const deleteProperty = async (id) => {
  try {
    const response = await api.delete(`/properties/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting property ${id}:`, error);
    throw error;
  }
};

// 物件資產相關 API 呼叫
export const getPropertyAssets = async (propertyId) => {
  try {
    const response = await api.get(`/properties/${propertyId}/assets/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching assets for property ${propertyId}:`, error);
    throw error;
  }
};

export const addPropertyAsset = async (propertyId, assetData) => {
  // 確保資產類型和狀態有預設值
  const data = {
    ...assetData,
    asset_type: assetData.asset_type || '家電類',
    current_status: assetData.current_status || '良好'
  };
  
  try {
    const response = await api.post(`/properties/${propertyId}/assets/`, data);
    return response.data;
  } catch (error) {
    console.error(`Error adding asset to property ${propertyId}:`, error);
    throw error;
  }
};

export const updatePropertyAsset = async (propertyId, assetId, assetData) => {
  try {
    const response = await api.put(`/properties/${propertyId}/assets/${assetId}`, assetData);
    return response.data;
  } catch (error) {
    console.error(`Error updating asset ${assetId} for property ${propertyId}:`, error);
    throw error;
  }
};

export const deletePropertyAsset = async (propertyId, assetId) => {
  try {
    const response = await api.delete(`/properties/${propertyId}/assets/${assetId}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting asset ${assetId} for property ${propertyId}:`, error);
    throw error;
  }
};

// 維修請求相關 API 呼叫
export const getRepairRequests = async (propertyId) => {
  try {
    const response = await api.get(`/properties/${propertyId}/repair-requests/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching repair requests for property ${propertyId}:`, error);
    throw error;
  }
};

export const addRepairRequest = async (propertyId, requestData) => {
  // 確保費用承擔方有預設值
  const data = {
    ...requestData,
    cost_bearer: requestData.cost_bearer || '房東',
  };
  
  try {
    const response = await api.post(`/properties/${propertyId}/repair-requests/`, data);
    return response.data;
  } catch (error) {
    console.error(`Error adding repair request to property ${propertyId}:`, error);
    throw error;
  }
};

export const updateRepairRequest = async (propertyId, requestId, requestData) => {
  try {
    const response = await api.put(`/properties/${propertyId}/repair-requests/${requestId}`, requestData);
    return response.data;
  } catch (error) {
    console.error(`Error updating repair request ${requestId} for property ${propertyId}:`, error);
    throw error;
  }
};

export const deleteRepairRequest = async (propertyId, requestId) => {
  try {
    const response = await api.delete(`/properties/${propertyId}/repair-requests/${requestId}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting repair request ${requestId} for property ${propertyId}:`, error);
    throw error;
  }
};

export default api;