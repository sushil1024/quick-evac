import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Location API endpoints
export const locationApi = {
  /**
   * Check if a location is in a danger zone
   * 
   * @param {Object} data - Location data
   * @param {string} data.phone_number - User's phone number
   * @param {number} data.latitude - User's latitude
   * @param {number} data.longitude - User's longitude
   * @returns {Promise} - API response
   */
  checkLocation: (data) => api.post('/location/check', data),
};

// Zones API endpoints
export const zonesApi = {
  /**
   * Get all zones or filter by type
   * 
   * @param {string} type - Optional zone type filter (RED, ORANGE, GREEN)
   * @returns {Promise} - API response
   */
  getZones: (type) => api.get(`/zone${type ? `?type=${type}` : ''}`),
  
  /**
   * Get a zone by ID
   * 
   * @param {number} id - Zone ID
   * @returns {Promise} - API response
   */
  getZone: (id) => api.get(`/zone/${id}`),
  
  /**
   * Create a new zone
   * 
   * @param {Object} data - Zone data
   * @returns {Promise} - API response
   */
  createZone: (data) => api.post('/zone', data),
  
  /**
   * Update an existing zone
   * 
   * @param {number} id - Zone ID
   * @param {Object} data - Updated zone data
   * @returns {Promise} - API response
   */
  updateZone: (id, data) => api.put(`/zone/${id}`, data),
  
  /**
   * Delete a zone
   * 
   * @param {number} id - Zone ID
   * @returns {Promise} - API response
   */
  deleteZone: (id) => api.delete(`/zone/${id}`),
};

export default api;