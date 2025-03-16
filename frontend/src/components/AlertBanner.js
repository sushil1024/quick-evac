import React from 'react';
import { Alert, AlertTitle, Box, Collapse } from '@mui/material';

/**
 * Component to display alert messages
 * 
 * @param {Object} props - Component props
 * @param {string} props.message - Alert message to display
 * @param {string} props.severity - Alert severity ('error', 'warning', 'info', 'success')
 * @param {string} props.title - Optional alert title
 * @param {boolean} props.open - Whether the alert is visible
 * @param {function} props.onClose - Function to close the alert
 */
const AlertBanner = ({ message, severity = 'info', title, open, onClose }) => {
  return (
    <Box sx={{ width: '100%', maxWidth: 600, mx: 'auto', mt: 2 }}>
      <Collapse in={open}>
        <Alert 
          severity={severity} 
          onClose={onClose}
          sx={{ mb: 2 }}
        >
          {title && <AlertTitle>{title}</AlertTitle>}
          {message}
        </Alert>
      </Collapse>
    </Box>
  );
};

export default AlertBanner;