import React, { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";
import Cookies from 'js-cookie';

// RootPage สำหรับตรวจสอบ role และ redirect ไปหน้า home ตาม role
export default function RootPage() {
  const { isAuthenticated, role } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    const token = Cookies.get('access_token');

    // ถ้าไม่ login หรือไม่มี token ให้ redirect ไปหน้า login ตาม role ที่คาดหวัง
    if (!isAuthenticated || !token) {
      navigate("/login/person", { replace: true });
      return;
    }

    // ตรวจสอบ role และ redirect ไปหน้า home ที่เหมาะสม
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
      // ถ้า role ไม่ถูกต้อง ลบ token และ redirect ไป login
      Cookies.remove('access_token');
      navigate("/login/person", { replace: true });
    }
  }, [isAuthenticated, role, navigate]);

  // ไม่ render อะไร เนื่องจากเป็นหน้า redirect เท่านั้น
  return null;
}