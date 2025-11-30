# Email-Based Automatic Login Implementation Prompt

## Objective
Implement automatic user login using email address as a URL parameter. When a user accesses the application with an email parameter, they should be automatically authenticated and logged in, then redirected to the home page with the chatbot interface.

## Requirements
1. Backend API endpoint that accepts email as a query parameter
2. Frontend React route that handles email-based login
3. Automatic session creation and cookie setting
4. Seamless redirect to home page after authentication

---

## Step 1: Backend Implementation

### File: `backend/services/auth_service.py`

**Add this method to the `AuthService` class (after the `validate_session` method):**

```python
def login_by_email(self, email: str, name: str = None, db: Session = None) -> LoginResponse:
    """Login user by email address directly (for development/testing purposes).
    
    This method:
    1. Finds or creates a user by email
    2. Creates a new session
    3. Returns session info
    
    Note: This bypasses Google OAuth verification. Use only for trusted environments.
    """
    if not email:
        return LoginResponse(
            success=False,
            session_id="",
            user=None,
            message="Email is required."
        )
    
    if not db:
        return LoginResponse(
            success=False,
            session_id="",
            user=None,
            message="Database session is required."
        )
    
    try:
        email = email.strip().lower()
        
        # Try to find user by email first
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            # User doesn't exist, create new user
            # Generate a unique google_id for email-based users (format: email_xxx)
            google_id = f"email_{uuid.uuid4().hex[:16]}"
            
            # Extract name from email if not provided (e.g., john.doe@example.com -> John Doe)
            if not name:
                email_parts = email.split('@')[0]
                name = email_parts.replace('.', ' ').replace('_', ' ').title()
            
            user = User(
                email=email,
                name=name,
                google_id=google_id
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"✅ [AUTH-SERVICE] Created new user by email: {email}")
        else:
            print(f"✅ [AUTH-SERVICE] Found existing user by email: {email}")
            # Update name if provided and different
            if name and user.name != name:
                user.name = name
                db.commit()
                db.refresh(user)
        
        # Create a new session for this user
        session_id = f"session_{uuid.uuid4()}"
        session = UserSession(
            id=session_id,
            user_id=user.id,
            is_active=True,
            expires_at=datetime.now() + timedelta(hours=24)
        )
        db.add(session)
        db.commit()
        
        print(f"✅ [AUTH-SERVICE] Created session for user: {email} (session_id: {session_id})")
        
        return LoginResponse(
            success=True,
            session_id=session_id,
            user={
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "google_id": user.google_id
            },
            message="Login successful by email"
        )
    except Exception as exc:
        db.rollback()
        print(f"❌ [AUTH-SERVICE] Email login error: {str(exc)}")
        return LoginResponse(
            success=False,
            session_id="",
            user=None,
            message=f"Email login failed: {str(exc)}"
        )
```

---

### File: `backend/main.py`

**Add this endpoint (after the `/api/auth/logout` endpoint):**

```python
@app.get("/api/auth/login-by-email")
async def login_by_email(
    request: Request,
    email: str = None, 
    name: str = None, 
    redirect: str = None,
    format: str = None,  # 'json' to force JSON response
    db: Session = Depends(get_db)
):
    """Login user directly by email address (for development/testing).
    
    This endpoint accepts email as a query parameter and automatically:
    1. Finds or creates the user by email
    2. Creates a session
    3. Sets session cookie
    4. Redirects to frontend (browser) or returns JSON (API client)
    
    Usage:
        Browser: GET /api/auth/login-by-email?email=user@example.com
        API: GET /api/auth/login-by-email?email=user@example.com&format=json
    
    Parameters:
        - email: User email address (required)
        - name: User name (optional)
        - redirect: If 'true', redirects to frontend home page (optional, auto-detected)
        - format: If 'json', forces JSON response (for API clients like Postman)
    
    Note: This bypasses Google OAuth. Use only for trusted environments.
    """
    if not email:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "session_id": None,
                "user": None,
                "message": "Email parameter is required. Usage: /api/auth/login-by-email?email=user@example.com"
            }
        )
    
    try:
        print(f"🔐 [AUTH] Login by email requested: {email}")
        result = auth_service.login_by_email(email=email, name=name, db=db)
        
        if result.success:
            print(f"✅ [AUTH] Email login successful for: {email}")
            
            # Determine if we should redirect or return JSON
            # Check Accept header to detect browser vs API client
            accept_header = request.headers.get("Accept", "")
            is_browser_request = (
                "text/html" in accept_header or 
                accept_header == "" or
                "*/*" in accept_header
            )
            
            # Force JSON if format=json parameter is set (for API clients like Postman)
            should_return_json = (format and format.lower() == 'json') or (
                not is_browser_request and 
                not (redirect and redirect.lower() == 'true')
            )
            
            # If redirect is explicitly requested OR it's a browser request, redirect to frontend
            if not should_return_json:
                frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
                # Redirect to email-login route which will handle the session properly
                # This ensures localStorage is set and user state is properly initialized
                redirect_url = f"{frontend_url}/email-login?email={email}"
                if name:
                    redirect_url += f"&name={name}"
                response = RedirectResponse(url=redirect_url, status_code=302)
                _set_session_cookie(response, result.session_id)
                print(f"🔄 [AUTH] Redirecting to frontend email-login: {redirect_url}")
                return response
            else:
                # Return JSON response for API calls (like Postman)
                response = JSONResponse(content=result.dict())
                _set_session_cookie(response, result.session_id)
                return response
        else:
            print(f"❌ [AUTH] Email login failed: {result.message}")
            response = JSONResponse(content=result.dict())
            _clear_session_cookie(response)
            return response
    except Exception as e:
        print(f"❌ [AUTH] Email login error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        error_response = LoginResponse(
            success=False,
            session_id="",
            user=None,
            message=f"Email login error: {str(e)}"
        )
        response = JSONResponse(content=error_response.dict())
        _clear_session_cookie(response)
        return response
```

**Make sure to import `Request` at the top:**
```python
from fastapi import FastAPI, Depends, UploadFile, File, Form, BackgroundTasks, Request
# If Request is not already imported, add it
```

---

## Step 2: Frontend Implementation

### File: `frontend/src/components/EmailLoginCallback.js`

**Create a new file with this content:**

```javascript
import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';
import './GoogleCallback.css';

const EmailLoginCallback = () => {
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const { setUser, setSessionId, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const handleEmailLogin = async () => {
      try {
        // If user is already authenticated, redirect to home
        if (isAuthenticated) {
          navigate('/home');
          return;
        }

        const urlParams = new URLSearchParams(location.search);
        const email = urlParams.get('email');
        const name = urlParams.get('name');

        if (!email) {
          setError('Email parameter is required. Usage: /email-login?email=user@example.com');
          setLoading(false);
          return;
        }

        // First, check if we already have a valid session cookie (from backend redirect)
        try {
          const sessionCheck = await axios.get(
            `${process.env.REACT_APP_API_URL}/api/auth/session`,
            { withCredentials: true }
          );
          
          if (sessionCheck.data?.success && sessionCheck.data?.session_id && sessionCheck.data?.user) {
            // Session already exists from backend redirect, use it
            setUser(sessionCheck.data.user);
            setSessionId(sessionCheck.data.session_id);
            localStorage.setItem('user', JSON.stringify(sessionCheck.data.user));
            localStorage.setItem('sessionId', sessionCheck.data.session_id);
            
            // Clear any existing workspace selection
            localStorage.removeItem('selectedWorkspace');
            // Clear chatbot session flags to ensure it shows on new login
            sessionStorage.removeItem('hasShownFullscreenChat');
            sessionStorage.removeItem('lastShownFullscreenChatUserId');
            
            // Clear the URL parameters to prevent back button issues
            window.history.replaceState({}, document.title, '/email-login');
            navigate('/home');
            return;
          }
        } catch (sessionError) {
          // Session check failed, continue with email login
          console.log('No existing session, proceeding with email login...');
        }

        // No valid session, call the email login endpoint with format=json to get JSON response
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/auth/login-by-email`, {
          params: { email, name, format: 'json' }, // Force JSON response
          withCredentials: true // Important for cookies
        });

        if (response.data.success) {
          // Clear any existing workspace selection
          localStorage.removeItem('selectedWorkspace');
          // Clear chatbot session flags to ensure it shows on new login
          sessionStorage.removeItem('hasShownFullscreenChat');
          sessionStorage.removeItem('lastShownFullscreenChatUserId');
          
          setUser(response.data.user);
          setSessionId(response.data.session_id);
          localStorage.setItem('user', JSON.stringify(response.data.user));
          localStorage.setItem('sessionId', response.data.session_id);
          
          // Clear the URL parameters to prevent back button issues
          window.history.replaceState({}, document.title, '/email-login');
          navigate('/home');
        } else {
          setError(response.data.message || 'Email login failed.');
          setLoading(false);
        }
      } catch (error) {
        console.error('Email login error:', error);
        setError(error.response?.data?.message || error.message || 'Email login failed. Please try again.');
        setLoading(false);
      }
    };

    handleEmailLogin();
  }, [location, navigate, setUser, setSessionId, isAuthenticated]);

  if (loading && !error) {
    return (
      <div className="callback-page">
        <div className="container">
          <div className="card">
            <div className="text-center">
              <div className="loading-spinner" style={{
                border: '4px solid #f3f3f3',
                borderTop: '4px solid #007bff',
                borderRadius: '50%',
                width: '50px',
                height: '50px',
                animation: 'spin 1s linear infinite',
                margin: '0 auto 20px'
              }}></div>
              <h2>Logging in...</h2>
              <p>Please wait while we authenticate you.</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="callback-page">
        <div className="container">
          <div className="card">
            <div className="text-center">
              <div className="error-icon">❌</div>
              <h2>Authentication Failed</h2>
              <p className="error-message">{error}</p>
              <button className="btn" onClick={() => navigate('/')}>
                Back to Login
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return null;
};

export default EmailLoginCallback;
```

---

### File: `frontend/src/App.js`

**Add the import and route:**

1. **Add import at the top:**
```javascript
import EmailLoginCallback from './components/EmailLoginCallback';
```

2. **Add route in the Routes section:**
```javascript
<Route path="/email-login" element={<EmailLoginCallback />} />
```

**Full Routes section should look like:**
```javascript
<Routes>
  <Route path="/" element={<LandingPage />} />
  <Route path="/callback" element={<GoogleCallback />} />
  <Route path="/email-login" element={<EmailLoginCallback />} />
  <Route path="/home" element={<HomePage />} />
  {/* ... other routes ... */}
</Routes>
```

---

### File: `frontend/src/components/HomePage.js`

**Update the useAuth hook to include loading state:**

Find this line:
```javascript
const { user, logout, isAuthenticated } = useAuth();
```

Change it to:
```javascript
const { user, logout, isAuthenticated, loading: authLoading } = useAuth();
```

**Update the authentication check to wait for loading:**

Find this section:
```javascript
// Safeguard: Ensure component always renders something, even if auth check fails
if (!isAuthenticated) {
  // Return a minimal loading/redirect message instead of null to prevent blank pages
  return (
    <div className="home-page" style={{ padding: '20px', textAlign: 'center' }}>
      <p>Redirecting to login...</p>
    </div>
  );
}
```

Replace it with:
```javascript
// Safeguard: Ensure component always renders something, even if auth check fails
// Wait for auth to finish loading before checking authentication
if (authLoading) {
  // Show loading state while AuthContext initializes (checks session cookie)
  return (
    <div className="home-page" style={{ padding: '20px', textAlign: 'center' }}>
      <p>Loading...</p>
    </div>
  );
}

if (!isAuthenticated) {
  // Return a minimal loading/redirect message instead of null to prevent blank pages
  return (
    <div className="home-page" style={{ padding: '20px', textAlign: 'center' }}>
      <p>Redirecting to login...</p>
    </div>
  );
}
```

---

### File: `frontend/src/components/GoogleCallback.css`

**Ensure this CSS exists (should already be there, but add spinner animation if missing):**

```css
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Spinner animation for loading states */
.loading-spinner {
  animation: spin 1s linear infinite;
}
```

---

## Step 3: Testing

### Test 1: Direct Backend URL (Local)

**Open in browser:**
```
http://localhost:8000/api/auth/login-by-email?email=your.email@example.com
```

**Expected:** Redirects to `http://localhost:3000/home` and shows the chatbot interface.

---

### Test 2: Frontend Route (Local)

**Open in browser:**
```
http://localhost:3000/email-login?email=your.email@example.com
```

**Expected:** Shows loading spinner, then redirects to `/home` with chatbot interface.

---

### Test 3: API Response (Postman/curl)

**Request:**
```
GET http://localhost:8000/api/auth/login-by-email?email=your.email@example.com&format=json
```

**Expected:** Returns JSON response with user info and session_id.

---

## Step 4: Verification

After implementation, verify:

1. ✅ User can login using email parameter in URL
2. ✅ Session cookie is set automatically
3. ✅ User is redirected to home page
4. ✅ Chatbot interface loads correctly
5. ✅ User state is persisted in localStorage
6. ✅ User can navigate to other pages

---

## Troubleshooting

### Issue: Redirect loop
**Solution:** Make sure `format=json` parameter is used in EmailLoginCallback component when calling API.

### Issue: Session not detected
**Solution:** Check that cookies are enabled and `withCredentials: true` is set in axios requests.

### Issue: 404 on /email-login route
**Solution:** Verify the route is added in `App.js` and component file exists.

### Issue: User not redirected to home
**Solution:** Check that HomePage waits for `authLoading` before checking authentication.

---

## Files Changed Summary

### Backend:
1. `backend/services/auth_service.py` - Added `login_by_email()` method
2. `backend/main.py` - Added `/api/auth/login-by-email` endpoint

### Frontend:
1. `frontend/src/components/EmailLoginCallback.js` - New component (create this file)
2. `frontend/src/App.js` - Added `/email-login` route
3. `frontend/src/components/HomePage.js` - Updated to wait for auth loading
4. `frontend/src/components/GoogleCallback.css` - Ensure spinner animation exists

---

## Usage Examples

### For Users:

**Direct login via backend (browser):**
```
http://localhost:8000/api/auth/login-by-email?email=user@example.com
```

**Direct login via frontend route:**
```
http://localhost:3000/email-login?email=user@example.com
```

**With name parameter:**
```
http://localhost:3000/email-login?email=user@example.com&name=John Doe
```

**For ngrok/remote access:**
```
https://your-ngrok-url.ngrok-free.app/email-login?email=user@example.com
```

---

## Notes

- This bypasses Google OAuth verification
- Use only for trusted environments (development/testing)
- Users are automatically created if they don't exist
- Sessions expire after 24 hours
- All requests must include cookies (`withCredentials: true`)

---

## Completion Checklist

- [ ] Backend `login_by_email()` method added
- [ ] Backend `/api/auth/login-by-email` endpoint added
- [ ] Frontend `EmailLoginCallback.js` component created
- [ ] Frontend route `/email-login` added to `App.js`
- [ ] `HomePage.js` updated to wait for auth loading
- [ ] CSS spinner animation exists
- [ ] Tested locally with browser
- [ ] Tested with API client (Postman)
- [ ] Verified session persistence
- [ ] Verified redirect flow works

---

in addition to this 

filter chats based on the current user that is logged in / parameter (email id). don't forget this.

**End of Implementation Prompt**

