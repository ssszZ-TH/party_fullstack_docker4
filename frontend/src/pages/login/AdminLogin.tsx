import React, { useState, useContext } from 'react';
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
import { adminLogin } from '../../services/auth';

// Style for Paper component to ensure a clean and responsive design
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

const AdminLogin: React.FC = () => {
  // State for managing form
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const { login, isAuthenticated, role } = useContext(AuthContext);

  // Redirect based on role after login
  React.useEffect(() => {
    if (isAuthenticated && role) {
      if (['system_admin', 'basetype_admin', 'hr_admin', 'organization_admin'].includes(role)) {
        navigate(`/homes/${role}`, { replace: true });
      }
    }
  }, [isAuthenticated, role, navigate]);

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const { access_token } = await adminLogin({ email, password });
      Cookies.set('access_token', access_token, { expires: 7, secure: true, sameSite: 'strict' });
      login(access_token);
    } catch (err: any) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  // Redirect to other login pages
  const handlePersonLoginRedirect = () => {
    navigate('/login/person');
  };

  const handleOrganizationLoginRedirect = () => {
    navigate('/login/organization');
  };

  return (
    <Container maxWidth="xs">
      <StyledPaper elevation={6}>
        <Typography variant="h5" align="center" gutterBottom>
          Admin Sign In
        </Typography>
        {error && (
          <Alert severity="error" sx={{ mb: 2, width: '100%' }}>
            {error}
          </Alert>
        )}
        <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
          <TextField
            label="Email"
            type="email"
            fullWidth
            margin="normal"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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
            onClick={handlePersonLoginRedirect}
            disabled={loading}
          >
            Go to Person Sign In
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

export default AdminLogin;