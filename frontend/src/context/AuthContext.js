import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

// API Base URL from environment variable
const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      setIsLoggedIn(true);
      // Optional: Fetch user profile with token
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      setIsLoggedIn(false);
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [token]);

  const login = async (email, password) => {
    try {
      const formData = new FormData();
      formData.append('username', email); // backend expects 'username' for OAuth2 password flow
      formData.append('password', password);

      const response = await axios.post(`${API_BASE_URL}/api/auth/login`, formData);
      
      if (response.status === 200) {
        const { access_token } = response.data;
        localStorage.setItem('token', access_token);
        setToken(access_token);
        setIsLoggedIn(true);
        return { success: true };
      }
    } catch (error) {
      console.error('Login failed:', error);
      return { success: false, error: error.response?.data?.detail || 'Login failed' };
    }
  };

  const loginWithGoogle = (access_token, userData) => {
    try {
      localStorage.setItem('token', access_token);
      setToken(access_token);
      setUser(userData);
      setIsLoggedIn(true);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      return { success: true };
    } catch (error) {
      console.error('Google login failed:', error);
      return { success: false, error: 'Google login failed' };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setIsLoggedIn(false);
    setUser(null);
  };

  const register = async (email, password) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/auth/register`, {
        email,
        password
      });
      if (response.status === 200) {
        return { success: true };
      }
    } catch (error) {
      console.error('Registration failed:', error);
      return { success: false, error: error.response?.data?.detail || 'Registration failed' };
    }
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, user, login, loginWithGoogle, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
