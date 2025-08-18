import React, { useContext, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";
import Cookies from 'js-cookie';
import { getAdminProfile, getPersonProfile, getOrganizationProfile } from "../services/profile";

// RootPage สำหรับตรวจสอบ role และ redirect ไปหน้า home ตาม role
export default function RootPage() {
  const { isAuthenticated, role, setIsAuthenticated, setRole, setUser } = useContext(AuthContext);
  const navigate = useNavigate();
  const isChecking = useRef(false); // ป้องกันการเรียกซ้ำใน useEffect

  useEffect(() => {
    const checkAuthStatus = async () => {
      // ถ้ากำลังตรวจสอบอยู่ ให้ข้ามไป
      if (isChecking.current) return;
      isChecking.current = true;

      const token = Cookies.get('access_token');

      // ถ้ามี token ให้ตรวจสอบความถูกต้อง
      if (token) {
        try {
          let userData;
          let userRole;
          try {
            userData = await getAdminProfile();
            userRole = userData.role;
          } catch (adminError) {
            try {
              userData = await getPersonProfile();
              userRole = 'person_user';
            } catch (personError) {
              userData = await getOrganizationProfile();
              userRole = 'organization_user';
            }
          }
          // อัปเดต state ใน AuthContext
          setIsAuthenticated(true);
          setRole(userRole);
          setUser(userData);
        } catch (error) {
          console.error('Failed to fetch user data:', error);
          Cookies.remove('access_token');
          setIsAuthenticated(false);
          setRole(null);
          setUser(null);
          navigate("/login/person", { replace: true });
          isChecking.current = false;
          return;
        }
      } else {
        // ถ้าไม่มี token
        setIsAuthenticated(false);
        setRole(null);
        setUser(null);
        navigate("/login/person", { replace: true });
        isChecking.current = false;
        return;
      }

      // Redirect ตาม role
      if (role === "system_admin") {
        navigate("/homes/system_admin", { replace: true });
      } else if (role === "basetype_admin") {
        navigate("/homes/basetype_admin", { replace: true });
      } else if (role === "hr_admin") {
        navigate("/homes/hr_admin", { replace: true });
      } else if (role === "organization_admin") {
        navigate("/homes/organization_admin", { replace: true });
      } else if (role === "organization_user") {
        navigate("/homes/organization_user", { replace: true });
      } else if (role === "person_user") {
        navigate("/homes/person_user", { replace: true });
      } else {
        // ถ้า role ยังไม่ถูกตั้งค่า รอการอัปเดตจาก API
        isChecking.current = false;
        return;
      }

      isChecking.current = false;
    };

    checkAuthStatus();
  }, [isAuthenticated, role, navigate, setIsAuthenticated, setRole, setUser]);

  // ไม่ render อะไร เนื่องจากเป็นหน้า redirect เท่านั้น
  return null;
}