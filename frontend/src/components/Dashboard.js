import React from 'react';
import { Container, Typography, Box, Button, Avatar } from '@mui/material';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const { logout, isLoggedIn } = useAuth();
  const navigate = useNavigate();

  if (!isLoggedIn) {
    navigate('/');
    return null;
  }

  const storedUser = JSON.parse(
    localStorage.getItem('user') || '{}'
  );

  return (
    <Container 
      maxWidth={false} 
      sx={{ 
        minHeight: '100vh', 
        background: 'linear-gradient(135deg, #0a1929 0%, #102a43 100%)',
        pt: 10,
        color: 'white'
      }}
    >
      <Box sx={{ textAlign: 'center' }}>
        <Typography variant="h2" sx={{ mb: 4, fontWeight: 'bold', color: '#64b5f6' }}>
          Welcome to your Dashboard
        </Typography>
        <Typography variant="h5" sx={{ mb: 8, opacity: 0.8 }}>
          You are now securely logged in to LegalGPT.
        </Typography>
        <Box sx={{ display: 'flex', gap: 4, justifyContent: 'center' }}>
          <Button 
            variant="contained" 
            onClick={() => navigate('/local-law')}
            sx={{ backgroundColor: '#64b5f6', borderRadius: '20px', px: 4 }}
          >
            Go to Law Teller
          </Button>
          <Button 
            variant="contained" 
            onClick={() => navigate('/scholarship')}
            sx={{ backgroundColor: '#64b5f6', borderRadius: '20px', px: 4 }}
          >
            Go to Scholarship Checker
          </Button>
        </Box>

        {storedUser?.picture ? (
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2, mt: 10 }}>
            <Avatar 
              src={storedUser.picture}
              sx={{ width: 80, height: 80, boxShadow: '0 4px 20px rgba(100, 181, 246, 0.3)' }}
            />
            <Typography variant="h6" sx={{ color: '#64b5f6' }}>
              {storedUser.name}
            </Typography>
            <Button 
              variant="outlined" 
              onClick={logout}
              sx={{ color: '#f44336', borderColor: '#f44336', borderRadius: '20px', mt: 2 }}
            >
              Logout
            </Button>
          </Box>
        ) : (
          <Button 
            variant="outlined" 
            onClick={logout}
            sx={{ mt: 10, color: '#f44336', borderColor: '#f44336', borderRadius: '20px' }}
          >
            Logout
          </Button>
        )}
      </Box>
    </Container>
  );
};

export default Dashboard;
