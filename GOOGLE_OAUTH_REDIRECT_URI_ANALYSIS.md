# Google OAuth Redirect URI Analysis

## 1. Files Where redirect_uri is Defined/Used

### Backend Files:

#### `backend/services/auth_service.py`
- **Line 14**: Reads `GOOGLE_REDIRECT_URI` from environment variable
  ```python
  self.google_redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
  ```
- **Line 24**: Uses it in OAuth URL generation
  ```python
  'redirect_uri': self.google_redirect_uri,
  ```
- **Line 46**: Uses it in token exchange
  ```python
  'redirect_uri': self.google_redirect_uri
  ```

#### `backend/main.py`
- **Line 704**: Logs the redirect URI value
  ```python
  print(f"🔐 [AUTH] GOOGLE_REDIRECT_URI: {os.getenv('GOOGLE_REDIRECT_URI', 'NOT SET')}")
  ```
- **Line 849**: Backend callback endpoint (POST)
  ```python
  @app.post("/api/auth/google/callback")
  ```
  **Note**: This is a BACKEND API endpoint, NOT the redirect URI.

### Frontend Files:

#### `frontend/src/App.js`
- **Line 95**: Frontend route for callback
  ```javascript
  <Route path="/callback" element={<GoogleCallback />} />
  ```
  **ACTUAL FRONTEND ROUTE: `/callback`**

#### `frontend/src/components/GoogleCallback.js`
- **Line 36**: Sends code to backend API
  ```javascript
  const response = await axios.post(`${process.env.REACT_APP_API_URL}/api/auth/google/callback`, { code });
  ```

#### `frontend/src/contexts/AuthContext.js`
- **Line 65**: Gets OAuth URL from backend
  ```javascript
  const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/auth/google/url`);
  ```

### Documentation Files (INCORRECT):

#### `backend/env_setup_instructions.md`
- **Line 28**: Shows incorrect redirect URI
  ```bash
  GOOGLE_REDIRECT_URI=http://localhost:3000/auth/google/callback
  ```
  **❌ WRONG**: This path doesn't exist in the frontend!

#### `README.md`
- **Line 268**: Also shows incorrect redirect URI
  ```bash
  http://localhost:3000/auth/google/callback
  ```
  **❌ WRONG**: This path doesn't exist in the frontend!

---

## 2. EXACT Redirect URI Being Sent to Google

**Location**: `backend/services/auth_service.py`, line 24

**Code**:
```python
params = {
    'client_id': self.google_client_id,
    'redirect_uri': self.google_redirect_uri,  # ← This is what's sent to Google
    'scope': 'openid email profile',
    'response_type': 'code',
    'access_type': 'offline'
}
```

**Value**: Whatever is set in `GOOGLE_REDIRECT_URI` environment variable.

**Current Documentation Says**: `http://localhost:3000/auth/google/callback` (WRONG)
**Actual Frontend Route**: `/callback` (CORRECT)

---

## 3. Comparison with Google Cloud Console

### What's Currently in Documentation:
- `http://localhost:3000/auth/google/callback` ❌

### What Should Be Registered:
- `http://localhost:3000/callback` ✅

### The Mismatch:
- **Path difference**: Documentation says `/auth/google/callback` but actual route is `/callback`
- **Missing**: `/auth/google/` prefix in the actual frontend route

---

## 4. Configuration Requirements

### For Localhost Development:

**Frontend Route**: `/callback` (defined in `frontend/src/App.js`)

**Backend Callback Endpoint**: `/api/auth/google/callback` (POST endpoint, not a redirect URI)

**Flow**:
1. User clicks "Login with Google"
2. Frontend calls `/api/auth/google/url` to get OAuth URL
3. Backend generates OAuth URL with `redirect_uri` from `GOOGLE_REDIRECT_URI` env var
4. User is redirected to Google
5. Google redirects back to the `redirect_uri` (FRONTEND URL)
6. Frontend `/callback` route receives the `code` parameter
7. Frontend sends `code` to backend `/api/auth/google/callback` (POST API)

### Correct Configuration:

#### `.env` file (in `backend/` directory):
```bash
GOOGLE_REDIRECT_URI=http://localhost:3000/callback
```

#### Google Cloud Console - Authorized redirect URIs:
```
http://localhost:3000/callback
```

### For ngrok/Production:

#### `.env` file:
```bash
GOOGLE_REDIRECT_URI=https://your-ngrok-url.ngrok-free.app/callback
```

#### Google Cloud Console - Authorized redirect URIs:
```
https://your-ngrok-url.ngrok-free.app/callback
```

### Who Handles the Callback:

- **Frontend** (`/callback` route): Receives the redirect from Google with the `code` parameter
- **Backend** (`/api/auth/google/callback` POST endpoint): Exchanges the code for tokens and authenticates the user

---

## 5. Corrected Configuration

### `.env` File (backend/.env):
```bash
# Google OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
GOOGLE_REDIRECT_URI=http://localhost:3000/callback
```

### Google Cloud Console Configuration:

#### For Localhost:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to: **APIs & Services** → **Credentials**
3. Select your OAuth 2.0 Client ID
4. Under **Authorized redirect URIs**, add:
   ```
   http://localhost:3000/callback
   ```
5. Click **Save**

#### For ngrok/Production:
Add both:
```
http://localhost:3000/callback
https://your-ngrok-url.ngrok-free.app/callback
```

---

## Summary of Issues Found:

1. ❌ **Documentation Error**: `env_setup_instructions.md` and `README.md` show incorrect redirect URI
2. ❌ **Mismatch**: Documentation says `/auth/google/callback` but actual route is `/callback`
3. ✅ **Backend Code**: Correctly reads from environment variable
4. ✅ **Frontend Route**: Correctly defined as `/callback`

## Action Required:

1. **Update `.env` file** with correct redirect URI: `http://localhost:3000/callback`
2. **Update Google Cloud Console** to register: `http://localhost:3000/callback`
3. **Restart backend server** after updating `.env`
4. **Fix documentation files** to reflect the correct path

