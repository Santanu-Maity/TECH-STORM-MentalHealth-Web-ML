import apiClient from './api';
import { API_ENDPOINTS } from '../utils/constants';

const assessmentService = {
    // Submit assessment for prediction
    submitAssessment: async (assessmentData) => {
        try {
            const response = await apiClient.post(API_ENDPOINTS.PREDICT, assessmentData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Get user's assessment history
    getAssessments: async () => {
        try {
            const response = await apiClient.get(API_ENDPOINTS.ASSESSMENTS);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Get specific assessment
    getAssessmentById: async (id) => {
        try {
            const response = await apiClient.get(`${API_ENDPOINTS.ASSESSMENTS}/${id}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Save assessment with result
    saveAssessment: async (assessmentData) => {
        try {
            const response = await apiClient.post(API_ENDPOINTS.ASSESSMENTS, assessmentData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },
};

export default assessmentService;
