import { useContext, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";
import Cookies from 'js-cookie';
import { getCurrentRole } from "../services/auth";
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

      // ถ้ามี token ให้ตรวจสอบความถูกต้องโดยใช้ /currentrole
      if (token) {
        try {
          const userRole = await getCurrentRole();
          let userData;
          if (['system_admin', 'basetype_admin', 'hr_admin', 'organization_admin'].includes(userRole)) {
            userData = await getAdminProfile();
          } else if (userRole === 'person_user') {
            userData = await getPersonProfile();
          } else if (userRole === 'organization_user') {
            userData = await getOrganizationProfile();
          } else {
            throw new Error('Invalid role');
          }
          // อัปเดต state ใน AuthContext
          setIsAuthenticated(true);
          setRole(userRole);
          setUser(userData);

          // Redirect ตาม role
          if (userRole === "system_admin") {
            navigate("/homes/system_admin", { replace: true });
          } else if (userRole === "basetype_admin") {
            navigate("/homes/basetype_admin", { replace: true });
          } else if (userRole === "hr_admin") {
            navigate("/homes/hr_admin", { replace: true });
          } else if (userRole === "organization_admin") {
            navigate("/homes/organization_admin", { replace: true });
          } else if (userRole === "organization_user") {
            navigate("/homes/organization_user", { replace: true });
          } else if (userRole === "person_user") {
            navigate("/homes/person_user", { replace: true });
          } else {
            throw new Error('Invalid role');
          }
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
      }

      isChecking.current = false;
    };

    checkAuthStatus();
  }, [isAuthenticated, role, navigate, setIsAuthenticated, setRole, setUser]);

  // ไม่ render อะไร เนื่องจากเป็นหน้า redirect เท่านั้น
  return null;
}