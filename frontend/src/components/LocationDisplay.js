import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Button
} from '@mui/material';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import WarningIcon from '@mui/icons-material/Warning';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import DirectionsIcon from '@mui/icons-material/Directions';
import { formatPhoneNumber } from '../services/location';

/**
 * Component to display user location information and evacuation details
 * 
 * @param {Object} props - Component props
 * @param {Object} props.locationData - Location data from API
 * @param {string} props.phoneNumber - User's phone number
 * @param {function} props.onReset - Function to reset the form
 */
const LocationDisplay = ({ locationData, phoneNumber, onReset }) => {
  if (!locationData) return null;
  
  const { location, in_danger_zone, zone, evacuation } = locationData;
  
  // Determine zone color and icon
  const getZoneInfo = () => {
    if (!in_danger_zone) {
      return {
        color: 'success',
        icon: <CheckCircleIcon />,
        label: 'Safe Zone',
        message: 'You are not in a danger zone.'
      };
    }
    
    switch (zone.type) {
      case 'RED':
        return {
          color: 'error',
          icon: <WarningIcon />,
          label: 'High Danger Zone',
          message: 'Immediate evacuation required!'
        };
      case 'ORANGE':
        return {
          color: 'warning',
          icon: <WarningIcon />,
          label: 'Medium Danger Zone',
          message: 'Prepare for possible evacuation.'
        };
      case 'GREEN':
        return {
          color: 'success',
          icon: <CheckCircleIcon />,
          label: 'Safe Zone',
          message: 'No evacuation necessary.'
        };
      default:
        return {
          color: 'info',
          icon: <LocationOnIcon />,
          label: 'Unknown Zone',
          message: 'Status unknown.'
        };
    }
  };
  
  const zoneInfo = getZoneInfo();
  
  return (
    <Card elevation={3} sx={{ maxWidth: 600, mx: 'auto', mt: 4 }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h5" component="div">
            Location Status
          </Typography>
          <Chip 
            icon={zoneInfo.icon} 
            label={zoneInfo.label} 
            color={zoneInfo.color} 
            variant="filled" 
          />
        </Box>
        
        <Typography variant="body1" color="text.secondary" gutterBottom>
          Phone: {formatPhoneNumber(phoneNumber)}
        </Typography>
        
        <Box sx={{ my: 2 }}>
          <Typography variant="body1" component="div" sx={{ display: 'flex', alignItems: 'center' }}>
            <LocationOnIcon sx={{ mr: 1 }} color="primary" />
            {location.address || `Latitude: ${location.latitude.toFixed(6)}, Longitude: ${location.longitude.toFixed(6)}`}
          </Typography>
        </Box>
        
        <Typography variant="h6" color={zoneInfo.color} sx={{ mt: 3, fontWeight: 'bold' }}>
          {zoneInfo.message}
        </Typography>
        
        {in_danger_zone && zone && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="body1">
              You are in {zone.name} ({zone.type} zone).
            </Typography>
            
            {zone.description && (
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                {zone.description}
              </Typography>
            )}
          </Box>
        )}
        
        {evacuation && (
          <>
            <Divider sx={{ my: 3 }} />
            
            <Typography variant="h6" sx={{ mb: 2 }}>
              Evacuation Information
            </Typography>
            
            <Typography variant="body1" gutterBottom>
              Nearest safe zone: {evacuation.safe_zone.name} ({evacuation.distance.toFixed(2)} km away)
            </Typography>
            
            {evacuation.directions && (
              <>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                  Route: {evacuation.directions.distance}, approximately {evacuation.directions.duration}
                </Typography>
                
                <List dense sx={{ mt: 1 }}>
                  {evacuation.directions.steps.slice(0, 3).map((step, index) => (
                    <ListItem key={index}>
                      <ListItemIcon sx={{ minWidth: 36 }}>
                        <DirectionsIcon color="primary" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText 
                        primary={<div dangerouslySetInnerHTML={{ __html: step.instruction }} />}
                        secondary={`${step.distance}, ${step.duration}`} 
                      />
                    </ListItem>
                  ))}
                </List>
                
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1, fontStyle: 'italic' }}>
                  An SMS with evacuation details has been sent to your phone.
                </Typography>
              </>
            )}
          </>
        )}
        
        <Box sx={{ mt: 4, textAlign: 'center' }}>
          <Button 
            variant="outlined" 
            color="primary" 
            onClick={onReset}
          >
            Check Another Location
          </Button>
        </Box>
        </CardContent>
    </Card>
    );
};
export default LocationDisplay;