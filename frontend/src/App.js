import React, { useState } from 'react';
import { 
  Container, 
  Box, 
  AppBar, 
  Toolbar, 
  Typography, 
  useTheme 
} from '@mui/material';
import PhoneForm from './components/PhoneForm';
import LocationDisplay from './components/LocationDisplay';
import AlertBanner from './components/AlertBanner';
import EvacuationMap from './components/EvacuationMap';
import { getCurrentLocation } from './services/location';
import { locationApi } from './services/api';

function App() {
  const theme = useTheme();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [locationData, setLocationData] = useState(null);
  const [phoneNumber, setPhoneNumber] = useState('');
  
  const handleSubmit = async (phoneNumber) => {
    setPhoneNumber(phoneNumber);
    setLoading(true);
    setError(null);
    
    try {
      // Get user's current location
      const coordinates = await getCurrentLocation();
      
      // Check if the location is in a danger zone
      const response = await locationApi.checkLocation({
        phone_number: phoneNumber,
        ...coordinates
      });
      
      setLocationData(response.data);
      
    } catch (err) {
      console.error('Error:', err);
      
      // Set appropriate error message
      if (typeof err === 'string') {
        setError(err);
      } else if (err.response && err.response.data) {
        setError(err.response.data.message || 'An error occurred while processing your request.');
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };
  
  const handleReset = () => {
    setLocationData(null);
    setPhoneNumber('');
    setError(null);
  };
  
  const handleCloseError = () => {
    setError(null);
  };
  
  return (
    <Box sx={{ flexGrow: 1, minHeight: '100vh', bgcolor: 'background.default' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Quick Evac
          </Typography>
        </Toolbar>
      </AppBar>
      
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Box sx={{ my: 4, textAlign: 'center' }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Emergency Evacuation Management
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph>
            Check if you're in a danger zone and receive evacuation instructions via SMS.
          </Typography>
        </Box>
        
        <AlertBanner 
          message={error} 
          severity="error" 
          title="Error" 
          open={!!error}
          onClose={handleCloseError}
        />
        
        {!locationData ? (
          <PhoneForm onSubmit={handleSubmit} loading={loading} />
        ) : (
          <>
            <LocationDisplay 
              locationData={locationData} 
              phoneNumber={phoneNumber} 
              onReset={handleReset} 
            />
            
            <EvacuationMap locationData={locationData} />
          </>
        )}
        
        <Box sx={{ mt: 8, mb: 4, textAlign: 'center' }}>
          <Typography variant="body2" color="text.secondary">
            © {new Date().getFullYear()} Quick Evac - Empowering Efficient Evacuation Management
          </Typography>
        </Box>
      </Container>
    </Box>
  );
}

export default App;