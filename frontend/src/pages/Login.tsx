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
import { AuthContext } from '../contexts/AuthContext';
import { login as apiLogin } from '../services/auth';

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

const Login: React.FC = () => {
  // State for managing form, error, and loading
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Use navigate for redirection
  const navigate = useNavigate();

  // Use AuthContext for login and authentication check
  const { login, isAuthenticated } = useContext(AuthContext);

  // Redirect if already logged in
  React.useEffect(() => {
    if (isAuthenticated) {
      navigate('/', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Call login service with payload
      const { access_token } = await apiLogin({ email, password });
      // Update state with access_token
      login(access_token);
    } catch (err: any) {
      // Set error from service or default message
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  // Redirect to Admin Login page
  const handleAdminLoginRedirect = () => {
    navigate('/admin-login');
  };

  return (
    <Container maxWidth="xs">
      <StyledPaper elevation={6}>
        {/* Page title */}
        <Typography variant="h5" align="center" gutterBottom>
          Sign In
        </Typography>

        {/* Display error if any */}
        {error && (
          <Alert severity="error" sx={{ mb: 2, width: '100%' }}>
            {error}
          </Alert>
        )}

        {/* Login form */}
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
            autoComplete="username" // เพิ่ม autocomplete สำหรับ email
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
            autoComplete="current-password" // เพิ่ม autocomplete สำหรับ password
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
            sx={{ mb: 2 }}
            onClick={handleAdminLoginRedirect}
            disabled={loading}
          >
            Sign In as Admin
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

export default Login;