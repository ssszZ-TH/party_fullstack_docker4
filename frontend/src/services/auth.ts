import axios from 'axios';

// กำหนด URL ของ backend
const BACKEND_URL = 'http://localhost:8080';

// อินเทอร์เฟซสำหรับข้อมูลที่ใช้ในการ login
interface AdminLoginData {
  email: string;
  password: string;
}

interface PersonLoginData {
  username: string;
  password: string;
}

interface OrganizationLoginData {
  username: string;
  password: string;
}

// ฟังก์ชันสำหรับ admin login
export const adminLogin = async (data: AdminLoginData) => {
  const response = await axios.post(`${BACKEND_URL}/auth/login`, data);
  return {
    access_token: response.data.access_token,
    role: response.data.role || 'system_admin', // สมมติว่า API ส่ง role ใน token หรือกำหนด default
  };
};

// ฟังก์ชันสำหรับ person login
export const personLogin = async (data: PersonLoginData) => {
  const response = await axios.post(`${BACKEND_URL}/persons/login`, data);
  return {
    access_token: response.data.access_token,
    role: response.data.role || 'person_user', // สมมติว่า API ส่ง role ใน token หรือกำหนด default
  };
};

// ฟังก์ชันสำหรับ organization login
export const organizationLogin = async (data: OrganizationLoginData) => {
  const response = await axios.post(`${BACKEND_URL}/organizations/login`, data);
  return {
    access_token: response.data.access_token,
    role: response.data.role || 'organization_user', // สมมติว่า API ส่ง role ใน token หรือกำหนด default
  };
};

// ฟังก์ชันสำหรับดึง current role จาก endpoint /currentrole
export const getCurrentRole = async () => {
  const token = localStorage.getItem('access_token');
  const response = await axios.get(`${BACKEND_URL}/currentrole`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data.role;
};