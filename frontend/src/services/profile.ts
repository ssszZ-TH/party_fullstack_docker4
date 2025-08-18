import axios from 'axios';
import Cookies from 'js-cookie';

// กำหนด BASE_URL สำหรับ API endpoint
const BASE_URL = 'http://localhost:8080';

// ฟังก์ชันสำหรับ log error เพื่อแสดงรายละเอียดข้อผิดพลาดใน console
const logError = (method: string, url: string, error: any, token?: string) => {
  console.error(`Error in ${method} request to ${url}:`, {
    message: error.message,
    status: error.response?.status,
    data: error.response?.data,
    token: token || 'No token provided',
    stack: error.stack,
  });
};

// ฟังก์ชันดึง access_token จาก cookie
const getAuthHeaders = () => {
  const token = Cookies.get('access_token');
  if (!token) {
    throw new Error('No access token found');
  }
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };
};

// ฟังก์ชันสำหรับดึงข้อมูลโปรไฟล์ admin
export async function getAdminProfile() {
  try {
    const res = await axios.get(`${BASE_URL}/users/me`, {
      headers: getAuthHeaders(),
      validateStatus: (status) => status >= 200 && status < 300,
    });
    return res.data;
  } catch (error: any) {
    logError('getAdminProfile', `${BASE_URL}/users/me`, error, Cookies.get('access_token'));
    if (error.response?.status === 401) {
      throw new Error('Unauthorized: Invalid or expired token');
    }
    throw error;
  }
}

// ฟังก์ชันสำหรับดึงข้อมูลโปรไฟล์ person
export async function getPersonProfile() {
  try {
    const res = await axios.get(`${BASE_URL}/persons/me`, {
      headers: getAuthHeaders(),
      validateStatus: (status) => status >= 200 && status < 300,
    });
    return res.data;
  } catch (error: any) {
    logError('getPersonProfile', `${BASE_URL}/persons/me`, error, Cookies.get('access_token'));
    if (error.response?.status === 401) {
      throw new Error('Unauthorized: Invalid or expired token');
    }
    throw error;
  }
}

// ฟังก์ชันสำหรับดึงข้อมูลโปรไฟล์ organization
export async function getOrganizationProfile() {
  try {
    const res = await axios.get(`${BASE_URL}/organizations/me`, {
      headers: getAuthHeaders(),
      validateStatus: (status) => status >= 200 && status < 300,
    });
    return res.data;
  } catch (error: any) {
    logError('getOrganizationProfile', `${BASE_URL}/organizations/me`, error, Cookies.get('access_token'));
    if (error.response?.status === 401) {
      throw new Error('Unauthorized: Invalid or expired token');
    }
    throw error;
  }
}