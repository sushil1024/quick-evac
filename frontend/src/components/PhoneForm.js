import React, { useState } from 'react';
import { 
  Box, 
  Button, 
  TextField, 
  Typography, 
  Paper, 
  CircularProgress
} from '@mui/material';
import PhoneIcon from '@mui/icons-material/Phone';
import { isValidPhoneNumber } from '../services/location';

/**
 * Phone number input form component
 * 
 * @param {Object} props - Component props
 * @param {function} props.onSubmit - Function called when form is submitted
 * @param {boolean} props.loading - Whether form is in loading state
 */
const PhoneForm = ({ onSubmit, loading }) => {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const value = e.target.value;
    setPhoneNumber(value);
    
    // Clear error when user types
    if (error) {
      setError('');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validate phone number
    if (!isValidPhoneNumber(phoneNumber)) {
      setError('Please enter a valid phone number');
      return;
    }
    
    // Call submit handler with cleaned phone number
    const cleanedNumber = phoneNumber.replace(/\D/g, '');
    onSubmit(cleanedNumber);
  };

  return (
    <Paper elevation={3} sx={{ p: 4, maxWidth: 400, mx: 'auto', mt: 4 }}>
      <Box component="form" onSubmit={handleSubmit} noValidate>
        <Typography variant="h5" align="center" gutterBottom>
          Quick Evac
        </Typography>
        
        <Typography variant="body1" align="center" color="textSecondary" paragraph>
          Enter your phone number to receive evacuation alerts if you're in a danger zone.
        </Typography>
        
        <TextField
          margin="normal"
          required
          fullWidth
          id="phone"
          label="Phone Number"
          name="phone"
          autoComplete="tel"
          autoFocus
          value={phoneNumber}
          onChange={handleChange}
          error={!!error}
          helperText={error}
          InputProps={{
            startAdornment: <PhoneIcon sx={{ mr: 1, color: 'action.active' }} />,
          }}
          placeholder="(123) 456-7890"
          disabled={loading}
        />
        
        <Button
          type="submit"
          fullWidth
          variant="contained"
          color="primary"
          sx={{ mt: 3, mb: 2 }}
          disabled={loading}
        >
          {loading ? (
            <CircularProgress size={24} color="inherit" />
          ) : (
            'Check My Location'
          )}
        </Button>
      </Box>
    </Paper>
  );
};

export default PhoneForm;