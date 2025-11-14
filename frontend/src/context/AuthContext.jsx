import { createContext, useState, useEffect, useCallback } from 'react';
import PropTypes from 'prop-types';
import { STORAGE_KEYS } from '../utils/constants';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);

    // Initialize auth state from localStorage
    useEffect(() => {
        const initAuth = () => {
            try {
                const token = localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
                const storedUser = localStorage.getItem(STORAGE_KEYS.USER);

                if (token && storedUser) {
                    setUser(JSON.parse(storedUser));
                    setIsAuthenticated(true);
                }
            } catch (error) {
                console.error('Error initializing auth:', error);
                // Clear invalid data
                localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
                localStorage.removeItem(STORAGE_KEYS.USER);
            } finally {
                setLoading(false);
            }
        };

        initAuth();
    }, []);

    const login = useCallback((userData, token) => {
        try {
            localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, token);
            localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(userData));
            setUser(userData);
            setIsAuthenticated(true);
        } catch (error) {
            console.error('Error during login:', error);
            throw error;
        }
    }, []);

    const signup = useCallback((userData, token) => {
        try {
            localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, token);
            localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(userData));
            setUser(userData);
            setIsAuthenticated(true);
        } catch (error) {
            console.error('Error during signup:', error);
            throw error;
        }
    }, []);

    const logout = useCallback(() => {
        try {
            localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
            localStorage.removeItem(STORAGE_KEYS.USER);
            localStorage.removeItem(STORAGE_KEYS.ASSESSMENT_DRAFT);
            setUser(null);
            setIsAuthenticated(false);
        } catch (error) {
            console.error('Error during logout:', error);
        }
    }, []);

    const updateProfile = useCallback((updatedUserData) => {
        try {
            const updatedUser = { ...user, ...updatedUserData };
            localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(updatedUser));
            setUser(updatedUser);
        } catch (error) {
            console.error('Error updating profile:', error);
            throw error;
        }
    }, [user]);

    const value = {
        user,
        isAuthenticated,
        loading,
        login,
        signup,
        logout,
        updateProfile,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

AuthProvider.propTypes = {
    children: PropTypes.node.isRequired,
};
