import apiClient from './api';
import { API_ENDPOINTS } from '../utils/constants';

const authService = {
    // Login user
    login: async (credentials) => {
        try {
            const response = await apiClient.post(API_ENDPOINTS.LOGIN, credentials);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Signup user
    signup: async (userData) => {
        try {
            const response = await apiClient.post(API_ENDPOINTS.SIGNUP, userData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Logout user
    logout: async () => {
        try {
            const response = await apiClient.post(API_ENDPOINTS.LOGOUT);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Verify token
    verifyToken: async () => {
        try {
            const response = await apiClient.get(API_ENDPOINTS.VERIFY);
            return response.data;
        } catch (error) {
            throw error;
        }
    },
};

export default authService;
