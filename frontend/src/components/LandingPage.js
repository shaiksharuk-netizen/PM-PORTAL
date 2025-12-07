import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';
import './LandingPage.css';

const LandingPage = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [checkingSession, setCheckingSession] = useState(true);
  const { loginWithGoogle, setUser, setSessionId, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  // Check for existing session cookie on mount (from backend redirect)
  // Also handle email/token query parameters from landing page
  useEffect(() => {
    const checkSessionCookie = async () => {
      try {
        // If user is already authenticated (from localStorage), redirect to home
        if (isAuthenticated) {
          navigate('/home');
          setCheckingSession(false);
          return;
        }

        // Step 1: Check for email and token query parameters (from landing page)
        const urlParams = new URLSearchParams(location.search);
        const email = urlParams.get('email');
        const token = urlParams.get('token');

        if (email && token) {
          console.log('[LANDING] Email and token found in URL, validating with backend...');
          try {
            // Call backend root endpoint to validate token and create session
            const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
            const backendResponse = await axios.get(
              `${apiUrl}/`,
              {
                params: { email, token, format: 'json' },
                withCredentials: true // Important for cookies
              }
            );

            if (backendResponse.data?.success && backendResponse.data?.session_id && backendResponse.data?.user) {
              // Backend validated token and created session, use it
              setUser(backendResponse.data.user);
              setSessionId(backendResponse.data.session_id);
              localStorage.setItem('user', JSON.stringify(backendResponse.data.user));
              localStorage.setItem('sessionId', backendResponse.data.session_id);
              
              // Clear any existing workspace selection
              localStorage.removeItem('selectedWorkspace');
              // Clear chatbot session flags to ensure it shows on new login
              sessionStorage.removeItem('hasShownFullscreenChat');
              sessionStorage.removeItem('lastShownFullscreenChatUserId');
              
              // Clear URL parameters to prevent back button issues
              window.history.replaceState({}, document.title, '/');
              
              // Redirect to home page
              navigate('/home');
              setCheckingSession(false);
              return;
            } else {
              // Token validation failed
              const errorMsg = backendResponse.data?.message || 'Token validation failed';
              console.error('[LANDING] Token validation failed:', errorMsg);
              setError(errorMsg);
              setCheckingSession(false);
              return;
            }
          } catch (backendError) {
            // Backend call failed
            const errorMsg = backendError.response?.data?.message || backendError.message || 'Failed to validate token';
            console.error('[LANDING] Backend validation error:', errorMsg);
            setError(errorMsg);
            setCheckingSession(false);
            return;
          }
        }

        // Step 2: Check if we have a valid session cookie (from backend redirect or previous login)
        try {
          const sessionCheck = await axios.get(
            `${process.env.REACT_APP_API_URL}/api/auth/session`,
            { withCredentials: true }
          );
          
          if (sessionCheck.data?.success && sessionCheck.data?.session_id && sessionCheck.data?.user) {
            // Session cookie exists from backend redirect, use it to log in
            setUser(sessionCheck.data.user);
            setSessionId(sessionCheck.data.session_id);
            localStorage.setItem('user', JSON.stringify(sessionCheck.data.user));
            localStorage.setItem('sessionId', sessionCheck.data.session_id);
            
            // Clear any existing workspace selection
            localStorage.removeItem('selectedWorkspace');
            // Clear chatbot session flags to ensure it shows on new login
            sessionStorage.removeItem('hasShownFullscreenChat');
            sessionStorage.removeItem('lastShownFullscreenChatUserId');
            
            // Redirect to home page
            navigate('/home');
            setCheckingSession(false);
            return;
          }
        } catch (sessionError) {
          // No valid session cookie, show login page
          console.log('No existing session cookie, showing login page...');
        }
      } catch (error) {
        console.error('Error checking session:', error);
      } finally {
        setCheckingSession(false);
      }
    };

    checkSessionCookie();
  }, [isAuthenticated, navigate, setUser, setSessionId, location]);

  const handleGoogleLogin = async () => {
    setLoading(true);
    setError('');

    try {
      const result = await loginWithGoogle();
      if (result && result.success === false) {
        setError(result.message || 'Google OAuth failed. Please try again.');
        setLoading(false);
      }
      // If successful, loginWithGoogle will redirect to Google OAuth
      // Don't set loading to false here as we're redirecting
    } catch (error) {
      setError('An unexpected error occurred. Please try again.');
      setLoading(false);
    }
  };

  // Show loading state while checking for session cookie
  if (checkingSession) {
    return (
      <div className="landing-page">
        <div className="main-content" style={{ textAlign: 'center' }}>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="landing-page">
      <header className="top-bar">
        <img src="/forsys-logo.png" alt="Forsys Logo" className="forsys-logo" />
      </header>

      <div className="main-content">
        <h1 className="main-heading">Welcome to PM Portal</h1>
        <p className="sub-text">
          Engage, plan, and collaborate effectively with your team using the PM portal built for Forsys employees.
        </p>

        <button
          className="google-login-btn"
          onClick={handleGoogleLogin}
          disabled={loading}
        >
          <img
            src="https://developers.google.com/identity/images/g-logo.png"
            alt="Google"
            className="google-icon-img"
          />
          {loading ? 'Logging in...' : 'Login with Google'}
        </button>

        {error && <div className="error-message">{error}</div>}
      </div>
    </div>
  );
};

export default LandingPage;
