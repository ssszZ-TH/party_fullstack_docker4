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
import { getPersonProfile } from '../../services/profile';
import PersonIcon from '@mui/icons-material/Person';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import CommentIcon from '@mui/icons-material/Comment';
import EventIcon from '@mui/icons-material/Event';
import HomeIcon from '@mui/icons-material/Home';
import LogoutIcon from '@mui/icons-material/Logout';
import HeightIcon from '@mui/icons-material/Height';
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter';
import WcIcon from '@mui/icons-material/Wc';

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

// อินเทอร์เฟซสำหรับกำหนดโครงสร้างของข้อมูล person ที่ได้รับจาก API
interface Person {
  id: number;
  username: string;
  personal_id_number: string;
  first_name: string;
  middle_name: string | null;
  last_name: string;
  nick_name: string | null;
  birth_date: string;
  gender_type_id: number | null;
  marital_status_type_id: number | null;
  country_id: number | null;
  height: number;
  weight: number;
  ethnicity_type_id: number | null;
  income_range_id: number | null;
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

const PersonUserProfile: React.FC = () => {
  const [person, setPerson] = useState<Person | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated, logout, role } = useContext(AuthContext);
  const navigate = useNavigate();

  // useEffect สำหรับดึงข้อมูล person เมื่อ component ถูก mount
  // ตรวจสอบการยืนยันตัวตนและ role ก่อนเรียก API
  useEffect(() => {
    const fetchPerson = async () => {
      if (!isAuthenticated || role !== 'person_user') {
        setError('Please log in as Person User');
        setLoading(false);
        logout();
        navigate('/login/person');
        return;
      }

      try {
        const data = await getPersonProfile();
        setPerson(data);
        setLoading(false);
      } catch (err: any) {
        setLoading(false);
        if (err.message.includes('Unauthorized')) {
          setError('Invalid or expired token, please log in again');
          logout();
          navigate('/login/person');
        } else {
          setError(err.message || 'Unable to load profile');
        }
      }
    };

    fetchPerson();
  }, [isAuthenticated, logout, navigate, role]);

  // ฟังก์ชันสำหรับเปลี่ยนเส้นทางไปยังหน้า login
  const handleLoginRedirect = () => {
    navigate('/login/person');
  };

  // ฟังก์ชันสำหรับออกจากระบบและเปลี่ยนเส้นทางไปยังหน้า login
  const handleLogout = () => {
    logout();
    navigate('/login/person');
  };

  // ฟังก์ชันสำหรับกลับไปยังหน้า dashboard ของ Person User
  const handleBackToHome = () => {
    navigate('/homes/person_user');
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

  // แสดงข้อมูลโปรไฟล์เมื่อโหลดข้อมูล person สำเร็จ
  if (person) {
    return (
      <Container maxWidth="sm">
        <StyledPaper elevation={2}>
          <Typography variant="h5" align="center" gutterBottom>
            Person User Profile
          </Typography>
          <InfoBox>
            <List>
              <ListItem>
                <ListItemIcon>
                  <PersonIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Person ID"
                  secondary={person.id}
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
                  secondary={person.username || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <PersonIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Personal ID Number"
                  secondary={person.personal_id_number || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <PersonIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="First Name"
                  secondary={person.first_name || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <PersonIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Middle Name"
                  secondary={person.middle_name || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <PersonIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Last Name"
                  secondary={person.last_name || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <PersonIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Nick Name"
                  secondary={person.nick_name || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <EventIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Birth Date"
                  secondary={person.birth_date || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <WcIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Gender Type ID"
                  secondary={person.gender_type_id || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <PersonIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Marital Status Type ID"
                  secondary={person.marital_status_type_id || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <PersonIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Country ID"
                  secondary={person.country_id || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <HeightIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Height (cm)"
                  secondary={person.height || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <FitnessCenterIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Weight (kg)"
                  secondary={person.weight || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <PersonIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Ethnicity Type ID"
                  secondary={person.ethnicity_type_id || '-'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <PersonIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Income Range ID"
                  secondary={person.income_range_id || '-'}
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
                  secondary={person.comment || '-'}
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
                  secondary={formatDateTime(person.created_at)}
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
                  secondary={formatDateTime(person.updated_at)}
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

export default PersonUserProfile;