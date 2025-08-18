import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';

// ป้องกันการเข้าถึงหน้าที่ต้อง login และตรวจสอบ role
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, role } = useContext(AuthContext);

  // ถ้าไม่ login redirect ไปหน้า login ตาม role หรือ default ไป person login
  if (!isAuthenticated) {
    if (!role) {
      return <Navigate to="/login/person" replace />;
    }
    if (['system_admin', 'basetype_admin', 'hr_admin', 'organization_admin'].includes(role)) {
      return <Navigate to="/login/admin" replace />;
    } else if (role === 'person_user') {
      return <Navigate to="/login/person" replace />;
    } else if (role === 'organization_user') {
      return <Navigate to="/login/organization" replace />;
    }
  }

  // ถ้า login แล้วให้เข้าถึงหน้า
  return <>{children}</>;
};

export default ProtectedRoute;