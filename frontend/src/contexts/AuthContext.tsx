import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { getAdminProfile, getPersonProfile, getOrganizationProfile } from '../services/profile';

// อินเทอร์เฟซสำหรับ AuthContext
interface AuthContextType {
  isAuthenticated: boolean;
  role: string | null;
  user:
    | { id: number; name: string; email: string; role: string; created_at: string; updated_at: string | null }
    | { id: number; username: string; personal_id_number: string; first_name: string; middle_name: string | null; last_name: string; nick_name: string | null; birth_date: string; gender_type_id: number | null; marital_status_type_id: number | null; country_id: number | null; height: number; weight: number; ethnicity_type_id: number | null; income_range_id: number | null; comment: string; created_at: string; updated_at: string | null }
    | { id: number; federal_tax_id: string; name_en: string; name_th: string; organization_type_id: number | null; industry_type_id: number | null; employee_count_range_id: number | null; username: string; comment: string; created_at: string; updated_at: string | null }
    | null;
  login: (token: string) => void;
  logout: () => void;
  setIsAuthenticated: (value: boolean) => void;
  setRole: (role: string | null) => void;
  setUser: (user: AuthContextType['user']) => void;
}

export const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  role: null,
  user: null,
  login: () => {},
  logout: () => {},
  setIsAuthenticated: () => {},
  setRole: () => {},
  setUser: () => {},
});

// คอมโพเนนต์ AuthProvider
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // สถานะสำหรับ authentication, role และข้อมูลผู้ใช้
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(() => !!Cookies.get('access_token'));
  const [role, setRole] = useState<string | null>(null);
  const [user, setUser] = useState<AuthContextType['user']>(null);

  // ฟังก์ชันดึงข้อมูลผู้ใช้ตาม role
  const fetchUserData = async (token: string) => {
    try {
      let res;
      let userRole;
      try {
        res = await getAdminProfile();
        userRole = res.role;
      } catch (adminError) {
        try {
          res = await getPersonProfile();
          userRole = 'person_user';
        } catch (personError) {
          res = await getOrganizationProfile();
          userRole = 'organization_user';
        }
      }
      setUser(res);
      setRole(userRole);
      setIsAuthenticated(true);
      console.log('AuthContext: User data fetched:', res);
    } catch (error) {
      console.error('AuthContext: Error fetching user data:', error);
      setUser(null);
      setRole(null);
      setIsAuthenticated(false);
      Cookies.remove('access_token');
    }
  };

  // ตรวจสอบ token เมื่อ component mount
  useEffect(() => {
    const token = Cookies.get('access_token');
    if (token) {
      fetchUserData(token);
    } else {
      setUser(null);
      setRole(null);
      setIsAuthenticated(false);
    }
  }, []);

  // ฟังก์ชัน login เพื่อเก็บ token และดึงข้อมูลผู้ใช้
  const login = (token: string) => {
    Cookies.set('access_token', token, { expires: 7, secure: true, sameSite: 'strict' });
    fetchUserData(token);
  };

  // ฟังก์ชัน logout เพื่อลบ token และรีเซ็ตสถานะ
  const logout = () => {
    Cookies.remove('access_token');
    setUser(null);
    setRole(null);
    setIsAuthenticated(false);
    console.log('AuthContext: Logout successful');
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, role, user, login, logout, setIsAuthenticated, setRole, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};