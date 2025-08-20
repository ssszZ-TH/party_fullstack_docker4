import React, { useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Link,
  Alert,
  CircularProgress,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import Cookies from 'js-cookie';
import { AuthContext } from '../../contexts/AuthContext';
import { personLogin } from '../../services/auth';

// สไตล์สำหรับ Paper component เพื่อกำหนดลักษณะการแสดงผลของฟอร์ม login
// รองรับการ responsive สำหรับหน้าจอขนาดเล็ก
const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  marginTop: theme.spacing(8),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  [theme.breakpoints.down('sm')]: {
    padding: theme.spacing(2),
    marginTop: theme.spacing(2),
  },
}));

const PersonLogin: React.FC = () => {
  // State สำหรับจัดการข้อมูลฟอร์มและสถานะการทำงาน
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const { login, isAuthenticated, role } = useContext(AuthContext);

  // useEffect สำหรับตรวจสอบสถานะการ login และ role หลังจาก login สำเร็จ
  // ถ้า isAuthenticated เป็น true และ role เป็น person_user จะ redirect ไปหน้า home
  useEffect(() => {
    if (isAuthenticated && role === 'person_user') {
      navigate('/homes/person_user', { replace: true });
    }
  }, [isAuthenticated, role, navigate]);

  // ฟังก์ชันสำหรับจัดการการ submit ฟอร์ม login
  // เรียก API personLogin และบันทึก token ลงใน Cookies
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const { access_token } = await personLogin({ username, password });
      Cookies.set('access_token', access_token, { expires: 7, secure: true, sameSite: 'strict' });
      login(access_token, 'person_user');
    } catch (err: any) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  // ฟังก์ชันสำหรับเปลี่ยนเส้นทางไปยังหน้า login อื่นๆ
  const handleAdminLoginRedirect = () => {
    navigate('/login/admin');
  };

  const handleOrganizationLoginRedirect = () => {
    navigate('/login/organization');
  };

  return (
    <Container maxWidth="xs">
      <StyledPaper elevation={6}>
        <Typography variant="h5" align="center" gutterBottom>
          Person Sign In
        </Typography>
        {error && (
          <Alert severity="error" sx={{ mb: 2, width: '100%' }}>
            {error}
          </Alert>
        )}
        <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
          <TextField
            label="Username"
            type="text"
            fullWidth
            margin="normal"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            disabled={loading}
            autoComplete="username"
          />
          <TextField
            label="Password"
            type="password"
            fullWidth
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
            autoComplete="current-password"
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Sign In'}
          </Button>
          <Button
            fullWidth
            variant="outlined"
            sx={{ mb: 1 }}
            onClick={handleAdminLoginRedirect}
            disabled={loading}
          >
            Go to Admin Sign In
          </Button>
          <Button
            fullWidth
            variant="outlined"
            sx={{ mb: 2 }}
            onClick={handleOrganizationLoginRedirect}
            disabled={loading}
          >
            Go to Organization Sign In
          </Button>
          <Link
            href="/register"
            variant="body2"
            sx={{ display: 'block', textAlign: 'center' }}
          >
            Don’t have an account? Sign Up
          </Link>
        </Box>
      </StyledPaper>
    </Container>
  );
};

export default PersonLogin;