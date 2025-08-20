import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Box,
  CircularProgress,
  Alert,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  IconButton,
  Button,
  Typography,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { AuthContext } from '../../contexts/AuthContext';
import { getAdminProfile } from '../../services/profile';
import EmailIcon from '@mui/icons-material/Email';
import PersonIcon from '@mui/icons-material/Person';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import HomeIcon from '@mui/icons-material/Home';
import LogoutIcon from '@mui/icons-material/Logout';
import EventIcon from '@mui/icons-material/Event';

// ฟังก์ชันสำหรับแปลง timestamp เป็นรูปแบบวันที่และเวลาที่มนุษย์อ่านได้ในเขตเวลา GMT+7
// ถ้า timestamp เป็น null จะคืนค่า '-' เพื่อระบุว่าไม่มีการอัปเดต
const formatDateTime = (timestamp: string | null): string => {
  if (!timestamp) return '-';
  const date = new Date(timestamp);
  return date.toLocaleString('en-US', {
    timeZone: 'Asia/Bangkok',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true,
  });
};

// อินเทอร์เฟซสำหรับกำหนดโครงสร้างของข้อมูลผู้ใช้ที่ได้รับจาก API
interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  created_at: string;
  updated_at: string | null;
}

// สไตล์สำหรับ Paper component เพื่อกำหนดลักษณะการแสดงผลของกล่องโปรไฟล์
const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  marginTop: theme.spacing(4),
  marginBottom: theme.spacing(4),
  borderRadius: theme.shape.borderRadius,
  boxShadow: theme.shadows[2],
  background: theme.palette.background.paper,
  [theme.breakpoints.down('sm')]: {
    padding: theme.spacing(2),
    marginTop: theme.spacing(2),
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
  },
}));

// สไตล์สำหรับ Box ที่ใช้จัดวางข้อมูลโปรไฟล์และปุ่มควบคุม
const InfoBox = styled(Box)(({ theme }) => ({
  width: '100%',
  marginBottom: theme.spacing(2),
}));

// สไตล์สำหรับ Box ที่จัดวางปุ่ม Home และ Logout
const ButtonBox = styled(Box)(({ theme }) => ({
  display: 'flex',
  justifyContent: 'center',
  gap: theme.spacing(2),
  marginTop: theme.spacing(2),
}));

const HrAdminProfile: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated, logout, role } = useContext(AuthContext);
  const navigate = useNavigate();

  // useEffect สำหรับดึงข้อมูลผู้ใช้เมื่อ component ถูก mount
  // ตรวจสอบการยืนยันตัวตนและ role ก่อนเรียก API
  useEffect(() => {
    const fetchUser = async () => {
      if (!isAuthenticated || role !== 'hr_admin') {
        setError('Please log in as HR Admin');
        setLoading(false);
        logout();
        navigate('/login/admin');
        return;
      }

      try {
        const data = await getAdminProfile();
        setUser(data);
        setLoading(false);
      } catch (err: any) {
        setLoading(false);
        if (err.message.includes('Unauthorized')) {
          setError('Invalid or expired token, please log in again');
          logout();
          navigate('/login/admin');
        } else {
          setError(err.message || 'Unable to load profile');
        }
      }
    };

    fetchUser();
  }, [isAuthenticated, logout, navigate, role]);

  // ฟังก์ชันสำหรับเปลี่ยนเส้นทางไปยังหน้า login
  const handleLoginRedirect = () => {
    navigate('/login/admin');
  };

  // ฟังก์ชันสำหรับออกจากระบบและเปลี่ยนเส้นทางไปยังหน้า login
  const handleLogout = () => {
    logout();
    navigate('/login/admin');
  };

  // ฟังก์ชันสำหรับกลับไปยังหน้า dashboard ของ HR Admin
  const handleBackToHome = () => {
    navigate('/homes/hr_admin');
  };

  // แสดงหน้า loading ขณะรอข้อมูลจาก API
  if (loading) {
    return (
      <Container maxWidth="sm">
        <StyledPaper elevation={2}>
          <Box display="flex" justifyContent="center" py={4}>
            <CircularProgress color="primary" />
          </Box>
        </StyledPaper>
      </Container>
    );
  }

  // แสดงข้อความเมื่อผู้ใช้ไม่ได้ login หรือ token ไม่ถูกต้อง
  if (!isAuthenticated || error?.includes('Invalid or expired token')) {
    return (
      <Container maxWidth="sm">
        <StyledPaper elevation={2}>
          <Typography variant="h6" align="center" gutterBottom>
            You are not logged in
          </Typography>
          {error && (
            <Alert severity="error" sx={{ width: '100%', m: 2 }}>
              {error}
            </Alert>
          )}
          <Button
            fullWidth
            variant="contained"
            color="primary"
            onClick={handleLoginRedirect}
            sx={{ mt: 2 }}
          >
            Go to Login
          </Button>
        </StyledPaper>
      </Container>
    );
  }

  // แสดงข้อผิดพลาดอื่นๆ ที่เกิดขึ้นระหว่างการโหลดข้อมูล
  if (error) {
    return (
      <Container maxWidth="sm">
        <StyledPaper elevation={2}>
          <Alert severity="error" sx={{ width: '100%', m: 2 }}>
            {error}
          </Alert>
        </StyledPaper>
      </Container>
    );
  }

  // แสดงข้อมูลโปรไฟล์เมื่อโหลดข้อมูลผู้ใช้สำเร็จ
  if (user) {
    return (
      <Container maxWidth="sm">
        <StyledPaper elevation={2}>
          <Typography variant="h5" align="center" gutterBottom>
            HR Admin Profile
          </Typography>
          <InfoBox>
            <List>
              <ListItem>
                <ListItemIcon>
                  <PersonIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="User ID"
                  secondary={user.id}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <PersonIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Name"
                  secondary={user.name}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <EmailIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Email"
                  secondary={user.email}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <AdminPanelSettingsIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Role"
                  secondary={user.role || 'HR Admin'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <EventIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Created At"
                  secondary={formatDateTime(user.created_at)}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <EventIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Updated At"
                  secondary={formatDateTime(user.updated_at)}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
            </List>
          </InfoBox>
          <ButtonBox>
            <IconButton
              color="primary"
              onClick={handleBackToHome}
              aria-label="Back to Home"
            >
              <HomeIcon />
            </IconButton>
            <IconButton
              color="secondary"
              onClick={handleLogout}
              aria-label="Logout"
            >
              <LogoutIcon />
            </IconButton>
          </ButtonBox>
        </StyledPaper>
      </Container>
    );
  }

  return null;
};

export default HrAdminProfile;