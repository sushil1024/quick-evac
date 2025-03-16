/**
 * Get user's current location using browser's Geolocation API
 * 
 * @returns {Promise} - Resolves with coordinates or rejects with error message
 */
export const getCurrentLocation = () => {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject('Geolocation is not supported by your browser');
        return;
      }
      
      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          });
        },
        (error) => {
          let errorMessage = 'Unknown error';
          
          switch (error.code) {
            case error.PERMISSION_DENIED:
              errorMessage = 'Location permission denied. Please enable location services.';
              break;
            case error.POSITION_UNAVAILABLE:
              errorMessage = 'Location information is unavailable.';
              break;
            case error.TIMEOUT:
              errorMessage = 'The request to get user location timed out.';
              break;
            default:
              errorMessage = 'An unknown error occurred.';
          }
          
          reject(errorMessage);
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 0
        }
      );
    });
  };
  
  /**
   * Format a phone number for display
   * 
   * @param {string} phoneNumber - Phone number to format
   * @returns {string} - Formatted phone number
   */
  export const formatPhoneNumber = (phoneNumber) => {
    if (!phoneNumber) return '';
    
    // Remove all non-digit characters
    const cleaned = phoneNumber.replace(/\D/g, '');
    
    // Check if it's a valid US number (10 digits)
    if (cleaned.length === 10) {
      return `(${cleaned.substring(0, 3)}) ${cleaned.substring(3, 6)}-${cleaned.substring(6)}`;
    } else if (cleaned.length > 10) {
      // Handle international numbers
      return `+${cleaned.substring(0, cleaned.length - 10)} (${cleaned.substring(cleaned.length - 10, cleaned.length - 7)}) ${cleaned.substring(cleaned.length - 7, cleaned.length - 4)}-${cleaned.substring(cleaned.length - 4)}`;
    }
    
    // If not a standard format, return the cleaned number
    return cleaned;
  };
  
  /**
   * Validate a phone number
   * 
   * @param {string} phoneNumber - Phone number to validate
   * @returns {boolean} - Whether the phone number is valid
   */
  export const isValidPhoneNumber = (phoneNumber) => {
    if (!phoneNumber) return false;
    
    // Remove all non-digit characters
    const cleaned = phoneNumber.replace(/\D/g, '');
    
    // Check if it's a valid length (at least 10 digits)
    return cleaned.length >= 10;
  };