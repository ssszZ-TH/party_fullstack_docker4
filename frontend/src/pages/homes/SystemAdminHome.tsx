import React, { useContext, useEffect } from "react";
import { Link as RouterLink, useNavigate } from "react-router-dom";
import {
  Box,
  Container,
  Typography,
  Avatar,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
} from "@mui/material";
import {
  Person as PersonIcon,
  Settings as SettingsIcon,
  Info as AboutIcon,
  Storage as DatabaseIcon,
  School as TutorialIcon,
} from "@mui/icons-material";
import { useTheme } from "@mui/material/styles";
import { AuthContext } from "../../contexts/AuthContext";
import { getAdminProfile } from "../../services/profile";
import Cookies from 'js-cookie';

// Services data for system_admin
const services = [
  {
    title: "Admin Management",
    items: [
      { name: "Manage Organization Admins", path: "/v1/organization_admins" },
      { name: "Manage HR Admins", path: "/v1/hr_admins" },
      { name: "Manage Basetype Admins", path: "/v1/basetype_admins" },
    ],
  },
  {
    title: "Organization",
    items: [
      { name: "Organization Menu", path: "/v1/organizationmenu" },
      { name: "Organization", path: "/v1/organization" },
    ],
  },
];

// Navigation items
const navItems = [
  { name: "Profile", icon: <PersonIcon />, path: "/profiles/system_admin" },
  { name: "Settings", icon: <SettingsIcon />, path: "/v1/settings" },
  { name: "About", icon: <AboutIcon />, path: "/v1/about" },
  { name: "Database", icon: <DatabaseIcon />, path: "/v1/database" },
  { name: "Tutorial", icon: <TutorialIcon />, path: "/v1/tutorial" },
];

export default function SystemAdminHome() {
  const { isAuthenticated, logout, role } = useContext(AuthContext);
  const navigate = useNavigate();
  const theme = useTheme();

  // ตรวจสอบ token และ role
  useEffect(() => {
    const checkTokenValidity = async () => {
      // ตรวจสอบว่า isAuthenticated และ role ถูกต้อง
      if (!isAuthenticated || role !== "system_admin") {
        logout();
        navigate("/login/admin", { replace: true });
        return;
      }

      // ตรวจสอบว่ามี token ใน cookie
      const token = Cookies.get('access_token');
      if (!token) {
        console.error('No access token found in cookies');
        logout();
        navigate("/login/admin", { replace: true });
        return;
      }

      try {
        await getAdminProfile(); // เรียก API เพื่อตรวจสอบ token
      } catch (err: any) {
        console.error('Token validation failed:', err.message);
        logout();
        navigate("/login/admin", { replace: true });
      }
    };
    checkTokenValidity();
  }, [isAuthenticated, role, logout, navigate]);

  // แสดง grid ของ services
  const renderServiceGrid = (serviceItems: { name: string; path: string }[]) => (
    <Box
      sx={{
        display: "flex",
        flexWrap: "wrap",
        gap: "12px",
        justifyContent: "flex-start",
      }}
    >
      {serviceItems.map((service) => (
        <Box
          key={service.path}
          component={RouterLink}
          to={service.path}
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            width: "110px",
            height: "110px",
            textDecoration: "none",
            transition: "transform 0.2s",
            "&:hover": { transform: "scale(1.05)" },
          }}
        >
          <Avatar
            src={`/home_thumbnail/${service.name.toLowerCase().replace(/\s+/g, "_")}.png`}
            sx={{ width: 60, height: 60, mb: 0.5, borderRadius: "10%" }}
          />
          <Typography
            variant="body2"
            align="center"
            color="text.primary"
            sx={{
              fontWeight: 500,
              fontSize: "0.75rem",
              lineHeight: 1.2,
              height: "28px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              width: "100%",
              overflow: "hidden",
              textOverflow: "ellipsis",
            }}
          >
            {service.name}
          </Typography>
        </Box>
      ))}
    </Box>
  );

  return (
    <Box sx={{ display: "flex", minHeight: "100vh" }}>
      <Box
        sx={{
          width: 240,
          position: "fixed",
          height: "100vh",
          bgcolor: "primary.light",
          boxShadow: 3,
          zIndex: 10,
        }}
      >
        <Box sx={{ p: 2, textAlign: "center" }}>
          <img
            src="/sphere_wire_frame.svg"
            alt="Logo"
            style={{ width: "100%", objectFit: "contain" }}
          />
        </Box>
        <Divider />
        <List>
          {navItems.map((item) => (
            <ListItem key={item.name} disablePadding>
              <ListItemButton
                component={RouterLink}
                to={item.path}
                sx={{ "&:hover": { bgcolor: theme.palette.action.hover } }}
              >
                <ListItemIcon sx={{ minWidth: 40 }}>{item.icon}</ListItemIcon>
                <ListItemText primary={item.name} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Box>
      <Box
        component="main"
        sx={{ flexGrow: 1, ml: 30, position: "relative" }}
      >
        <img
          src="/sphere_wire_frame.svg"
          alt="Background"
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            height: "100vh",
            objectFit: "cover",
            zIndex: -1,
            opacity: 0.2,
          }}
        />
        <Container maxWidth="lg" sx={{ py: 4 }}>
          <Box sx={{ textAlign: "center", mb: 4 }}>
            <Typography variant="h4" gutterBottom>
              System Admin Dashboard
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              Manage all admin roles and organizational data
            </Typography>
          </Box>
          {services.map((section) => (
            <Box key={section.title}>
              {renderServiceGrid(section.items)}
              <hr style={{ margin: "20px 0" }} />
            </Box>
          ))}
        </Container>
      </Box>
    </Box>
  );
}