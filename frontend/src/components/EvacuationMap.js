import React, { useEffect, useRef } from 'react';
import { Box, Typography, Paper } from '@mui/material';

/**
 * Component to display a Google Maps with the evacuation route
 * 
 * @param {Object} props - Component props
 * @param {Object} props.locationData - Location data from API
 */
const EvacuationMap = ({ locationData }) => {
  const mapRef = useRef(null);
  const mapInstance = useRef(null);
  
  useEffect(() => {
    if (!locationData || !window.google || !window.google.maps) {
      return;
    }
    
    const { location, zone, evacuation } = locationData;
    
    // Initialize map
    if (!mapInstance.current) {
      mapInstance.current = new window.google.maps.Map(mapRef.current, {
        center: { lat: location.latitude, lng: location.longitude },
        zoom: 13,
        mapTypeId: 'roadmap',
        mapTypeControl: true,
        fullscreenControl: true,
      });
    }
    
    const map = mapInstance.current;
    
    // Clear existing markers and circles
    map.overlayMapTypes.clear();
    
    // Add marker for user location
    new window.google.maps.Marker({
      position: { lat: location.latitude, lng: location.longitude },
      map: map,
      title: 'Your Location',
      icon: {
        url: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
      },
    });
    
    // Add circle for danger zone if in one
    if (locationData.in_danger_zone && zone) {
      const zoneColors = {
        RED: '#ff0000',
        ORANGE: '#ff9800',
        GREEN: '#4caf50',
      };
      
      new window.google.maps.Circle({
        center: { lat: zone.latitude, lng: zone.longitude },
        radius: zone.radius * 1000, // Convert km to m
        map: map,
        fillColor: zoneColors[zone.type] || '#ff0000',
        fillOpacity: 0.3,
        strokeColor: zoneColors[zone.type] || '#ff0000',
        strokeWeight: 1,
      });
    }
    
    // Add safe zone marker and route if evacuation info is available
    if (evacuation && evacuation.safe_zone) {
      // Add marker for safe zone
      new window.google.maps.Marker({
        position: { 
          lat: evacuation.safe_zone.latitude, 
          lng: evacuation.safe_zone.longitude 
        },
        map: map,
        title: evacuation.safe_zone.name,
        icon: {
          url: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
        },
      });
      
      // Add circle for safe zone
      new window.google.maps.Circle({
        center: { 
          lat: evacuation.safe_zone.latitude, 
          lng: evacuation.safe_zone.longitude 
        },
        radius: evacuation.safe_zone.radius * 1000, // Convert km to m
        map: map,
        fillColor: '#4caf50',
        fillOpacity: 0.3,
        strokeColor: '#4caf50',
        strokeWeight: 1,
      });
      
      // Draw route if directions are available
      if (evacuation.directions) {
        const directionsService = new window.google.maps.DirectionsService();
        const directionsRenderer = new window.google.maps.DirectionsRenderer({
          map: map,
          suppressMarkers: true,
          polylineOptions: {
            strokeColor: '#4caf50',
            strokeWeight: 5,
          },
        });
        
        directionsService.route(
          {
            origin: { lat: location.latitude, lng: location.longitude },
            destination: { 
              lat: evacuation.safe_zone.latitude, 
              lng: evacuation.safe_zone.longitude 
            },
            travelMode: 'DRIVING',
          },
          (response, status) => {
            if (status === 'OK') {
              directionsRenderer.setDirections(response);
              
              // Adjust map bounds to show the entire route
              const bounds = new window.google.maps.LatLngBounds();
              bounds.extend({ lat: location.latitude, lng: location.longitude });
              bounds.extend({ 
                lat: evacuation.safe_zone.latitude, 
                lng: evacuation.safe_zone.longitude 
              });
              map.fitBounds(bounds);
            }
          }
        );
      }
    }
  }, [locationData]);
  
  if (!locationData) {
    return null;
  }
  
  return (
    <Paper elevation={3} sx={{ maxWidth: 600, mx: 'auto', mt: 4, overflow: 'hidden' }}>
      <Typography variant="h6" sx={{ p: 2, bgcolor: 'primary.main', color: 'white' }}>
        Evacuation Map
      </Typography>
      
      <Box
        ref={mapRef}
        sx={{
          width: '100%',
          height: 400,
          bgcolor: 'grey.300',
        }}
      />
      
      <Box sx={{ p: 2, bgcolor: 'grey.100' }}>
        <Typography variant="body2" color="text.secondary">
          {locationData.in_danger_zone ? 
            'Blue marker: Your location. Green marker: Nearest safe zone. Green line: Recommended evacuation route.' : 
            'You are in a safe location (blue marker).'}
        </Typography>
      </Box>
    </Paper>
  );
};

export default EvacuationMap;