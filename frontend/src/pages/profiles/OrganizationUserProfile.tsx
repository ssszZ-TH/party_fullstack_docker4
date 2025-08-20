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
import { getOrganizationProfile } from '../../services/profile';
import BusinessIcon from '@mui/icons-material/Business';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import CommentIcon from '@mui/icons-material/Comment';
import EventIcon from '@mui/icons-material/Event';
import HomeIcon from '@mui/icons-material/Home';
import LogoutIcon from '@mui/icons-material/Logout';

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

// อินเทอร์เฟซสำหรับกำหนดโครงสร้างของข้อมูล organization ที่ได้รับจาก API
interface Organization {
  id: number;
  federal_tax_id: string;
  name_en: string;
  name_th: string;
  organization_type_id: number | null;
  industry_type_id: number | null;
  employee_count_range_id: number | null;
  username: string;
  comment: string;
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

// สไตล์สำหรับ Box ที่ใช้จัดวางข้อมูลและปุ่มควบคุม
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

const OrganizationUserProfile: React.FC = () => {
  const [organization, setOrganization] = useState<Organization | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated, logout, role } = useContext(AuthContext);
  const navigate = useNavigate();

  // useEffect สำหรับดึงข้อมูล organization เมื่อ component ถูก mount
  // ตรวจสอบการยืนยันตัวตนและ role ก่อนเรียก API
  useEffect(() => {
    const fetchOrganization = async () => {
      if (!isAuthenticated || role !== 'organization_user') {
        setError('Please log in as Organization User');
        setLoading(false);
        logout();
        navigate('/login/organization');
        return;
      }

      try {
        const data = await getOrganizationProfile();
        setOrganization(data);
        setLoading(false);
      } catch (err: any) {
        setLoading(false);
        if (err.message.includes('Unauthorized')) {
          setError('Invalid or expired token, please log in again');
          logout();
          navigate('/login/organization');
        } else {
          setError(err.message || 'Unable to load profile');
        }
      }
    };

    fetchOrganization();
  }, [isAuthenticated, logout, navigate, role]);

  // ฟังก์ชันสำหรับเปลี่ยนเส้นทางไปยังหน้า login
  const handleLoginRedirect = () => {
    navigate('/login/organization');
  };

  // ฟังก์ชันสำหรับออกจากระบบและเปลี่ยนเส้นทางไปยังหน้า login
  const handleLogout = () => {
    logout();
    navigate('/login/organization');
  };

  // ฟังก์ชันสำหรับกลับไปยังหน้า dashboard ของ Organization User
  const handleBackToHome = () => {
    navigate('/homes/organization_user');
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

  // แสดงข้อมูลโปรไฟล์เมื่อโหลดข้อมูล organization สำเร็จ
  if (organization) {
    return (
      <Container maxWidth="sm">
        <StyledPaper elevation={2}>
          <Typography variant="h5" align="center" gutterBottom>
            Organization User Profile
          </Typography>
          <InfoBox>
            <List>
              <ListItem>
                <ListItemIcon>
                  <BusinessIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Organization ID"
                  secondary={organization.id}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <BusinessIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Federal Tax ID"
                  secondary={organization.federal_tax_id || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <BusinessIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Name (English)"
                  secondary={organization.name_en || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <BusinessIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Name (Thai)"
                  secondary={organization.name_th || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <BusinessIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Organization Type ID"
                  secondary={organization.organization_type_id || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <BusinessIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Industry Type ID"
                  secondary={organization.industry_type_id || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <BusinessIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Employee Count Range ID"
                  secondary={organization.employee_count_range_id || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <AccountCircleIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Username"
                  secondary={organization.username || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <CommentIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Comment"
                  secondary={organization.comment || '-'}
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
                  secondary={formatDateTime(organization.created_at)}
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
                  secondary={formatDateTime(organization.updated_at)}
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

export default OrganizationUserProfile;