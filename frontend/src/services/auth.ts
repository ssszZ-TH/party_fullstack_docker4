import axios from 'axios';
import Cookies from 'js-cookie';

const BASE_URL = 'http://localhost:8080';

// บันทึก error สำหรับ debug
const logError = (method: string, error: any) => {
  console.error(`Error in ${method} request to ${BASE_URL}:`, {
    message: error.message,
    status: error.response?.status,
    data: error.response?.data,
  });
};

// สมัครสมาชิก admin
export async function register({ name, email, password, role }: { name: string; email: string; password: string; role: string }) {
  try {
    const res = await axios.post(`${BASE_URL}/auth/register`, { name, email, password, role }, {
      headers: { 'Content-Type': 'application/json' },
    });
    return res.data;
  } catch (error: any) {
    logError('register', error);
    throw new Error(error.response?.data?.message || 'Registration failed');
  }
}

// ล็อกอินสำหรับ admin
export async function adminLogin({ email, password }: { email: string; password: string }) {
  try {
    const res = await axios.post(`${BASE_URL}/auth/login`, { email, password }, {
      headers: { 'Content-Type': 'application/json' },
    });
    Cookies.set('access_token', res.data.access_token, { expires: 7, secure: true, sameSite: 'strict' });
    return res.data;
  } catch (error: any) {
    logError('adminLogin', error);
    throw new Error(error.response?.data?.message || 'Login failed');
  }
}

// ล็อกอินสำหรับ person_user
export async function personLogin({ username, password }: { username: string; password: string }) {
  try {
    const res = await axios.post(`${BASE_URL}/persons/login`, { username, password }, {
      headers: { 'Content-Type': 'application/json' },
    });
    Cookies.set('access_token', res.data.access_token, { expires: 7, secure: true, sameSite: 'strict' });
    return res.data;
  } catch (error: any) {
    logError('personLogin', error);
    throw new Error(error.response?.data?.message || 'Login failed');
  }
}

// ล็อกอินสำหรับ organization_user
export async function organizationLogin({ username, password }: { username: string; password: string }) {
  try {
    const res = await axios.post(`${BASE_URL}/organizations/login`, { username, password }, {
      headers: { 'Content-Type': 'application/json' },
    });
    Cookies.set('access_token', res.data.access_token, { expires: 7, secure: true, sameSite: 'strict' });
    return res.data;
  } catch (error: any) {
    logError('organizationLogin', error);
    throw new Error(error.response?.data?.message || 'Login failed');
  }
}