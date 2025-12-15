# Sprint Planning Demo Application

A full-stack demo application featuring React.js frontend, FastAPI backend, and PostgreSQL database with simulated authentication and sprint planning functionality.

## 🚀 First Time Setup (Complete Beginner Guide)

**If you're new to this project and just downloaded it from GitHub, start here!**

This guide assumes you have no prior knowledge of this project and will walk you through everything step-by-step.

### What This Application Does
- **Sprint Planning**: Interactive chat-based sprint planning with AI
- **Authentication**: Simulated Google OAuth login (demo mode)
- **Document Processing**: Upload and process various document types
- **Risk Assessment**: Generate risk assessments from uploaded documents
- **Modern UI**: Clean, responsive web interface

### What You'll Need
Before starting, you need these installed on your computer:
1. **Python 3.8+** (for the backend server)
2. **Node.js 16+** (for the frontend application)
3. **PostgreSQL** (for the database)
4. **Git** (usually already installed)

### Quick Start (5 Minutes)
If you want to get running quickly, use our automated scripts:

**Windows Users:**
```bash
# Double-click start.bat or run in Command Prompt
start.bat
```

**Mac/Linux Users:**
```bash
# Make executable and run
chmod +x start.sh
./start.sh
```

These scripts will automatically:
- Check if you have the required software
- Set up the database
- Install all dependencies
- Start both frontend and backend servers

### Manual Setup (Recommended for Learning)
If you want to understand each step or the automated script doesn't work, follow the detailed setup guide below.

## Features

- **Demo Authentication**: Simulated Google OAuth login flow
- **Sprint Planning**: Interactive chat-based sprint planning with LLM integration
- **Grok API Integration**: Summary generation using Grok API
- **Modern UI**: Clean, responsive design with dropdown navigation

## Tech Stack

- **Frontend**: React.js with modern hooks and context
- **Backend**: FastAPI with async support
- **Database**: PostgreSQL
- **Authentication**: Demo-only (simulated Google OAuth)
- **LLM Integration**: Mock/Stub implementation
- **Grok API**: Mock endpoint for summarization

## Libraries & Dependencies

### Backend Dependencies (Python)
```
fastapi==0.104.1              # Modern, fast web framework for building APIs
uvicorn[standard]==0.24.0     # ASGI server for FastAPI
sqlalchemy==2.0.23            # SQL toolkit and ORM
psycopg2-binary==2.9.9        # PostgreSQL adapter for Python
alembic==1.12.1               # Database migration tool
python-multipart==0.0.6       # Multipart form data parsing
python-jose[cryptography]==3.3.0  # JWT token handling
passlib[bcrypt]==1.7.4        # Password hashing library
python-dotenv==1.0.0          # Environment variable management
pydantic==2.5.0               # Data validation using Python type annotations
pydantic-settings==2.1.0      # Settings management using Pydantic
httpx==0.25.2                 # Modern HTTP client
requests==2.31.0              # HTTP library for Python
reportlab==4.0.7              # PDF generation library
PyPDF2==3.0.1                 # PDF manipulation library
pdfplumber==0.10.3            # PDF text extraction library
```

### Frontend Dependencies (Node.js)
```
react==18.2.0                 # Frontend UI library
react-dom==18.2.0             # React DOM rendering
react-router-dom==6.20.1      # Client-side routing
react-scripts==5.0.1          # Create React App scripts
axios==1.6.2                  # HTTP client for API calls
html2pdf.js==0.10.3           # HTML to PDF conversion
jspdf==3.0.1                  # PDF generation in JavaScript
xlsx==0.18.5                  # Excel file processing
@testing-library/jest-dom==5.17.0      # Jest DOM matchers
@testing-library/react==13.4.0         # React testing utilities
@testing-library/user-event==14.5.2    # User event simulation
web-vitals==2.1.4             # Web performance metrics
```

## Project Structure

```
Sharuk_Proj/
├── frontend/          # React.js application
├── backend/           # FastAPI application
├── database/          # Database setup and migrations
└── README.md         # This file
```

## Complete Setup Guide (Initial to Final)

### Prerequisites Installation

#### 1. Install Required Software

**Python 3.8+**
- Download from [python.org](https://www.python.org/downloads/)
- Verify installation: `python --version`

**Node.js 16+**
- Download from [nodejs.org](https://nodejs.org/)
- Verify installation: `node --version`

**PostgreSQL**
- Download from [postgresql.org](https://www.postgresql.org/download/)
- Start PostgreSQL service:
  - **Windows**: Start PostgreSQL service from Services
  - **Mac**: `brew services start postgresql`
  - **Linux**: `sudo systemctl start postgresql`

**Git**
- Download from [git-scm.com](https://git-scm.com/)

### Database Setup

#### 1. Create Database
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE sprint_demo;

# Exit psql
\q
```

#### 2. Initialize Database Schema
```bash
# Run setup script
psql -U postgres -d sprint_demo -f database/setup.sql
```

### Backend Setup

#### 1. Navigate to Backend Directory
```bash
cd backend
```

#### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

#### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables
```bash
# Copy environment template
cp env.example .env

# Edit .env file with your settings
```

**Required .env Configuration:**
```bash
# Database Configuration
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/sprint_demo

# Security
SECRET_KEY=your-secret-key-here-change-in-production

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://192.168.11.101:3000

# Environment
ENVIRONMENT=development

# Gemini API (Optional)
GEMINI_API_KEY=your-gemini-api-key-here

# Google OAuth Configuration (Optional)
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
GOOGLE_REDIRECT_URI=http://localhost:3000/callback
```

#### 5. Start Backend Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

#### 1. Navigate to Frontend Directory
```bash
# In a new terminal
cd frontend
```

#### 2. Install Node.js Dependencies
```bash
npm install
```

#### 3. Start Frontend Development Server
```bash
npm start
```

### Quick Start Scripts

#### Windows Users
```bash
# Run the automated setup script
start.bat
```

#### Mac/Linux Users
```bash
# Make script executable
chmod +x start.sh

# Run the automated setup script
./start.sh
```

### Access Points

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Interactive API**: http://localhost:8000/redoc

### Google OAuth Setup (Optional)

#### 1. Create Google OAuth Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Set Application Type to "Web application"
6. Add Authorized redirect URIs: `http://localhost:3000/callback`
7. Copy the Client ID and Client Secret

#### 2. Update .env File
```bash
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your-actual-secret-here
```

### Verification Steps

#### 1. Check Backend Health
```bash
curl http://localhost:8000/health
```

#### 2. Check Database Connection
```bash
# Connect to database
psql -U postgres -d sprint_demo

# Check tables
\dt

# Exit
\q
```

#### 3. Test Frontend-Backend Connection
- Open http://localhost:3000
- Check browser console for errors
- Verify API calls in Network tab

## 🎯 What to Expect When Everything Works

### Success Indicators
When your setup is complete and working, you should see:

#### 1. Backend Server Running
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

#### 2. Frontend Server Running
```
Compiled successfully!

You can now view sprint-planning-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000

Note that the development build is not optimized.
To create a production build, use npm run build.
```

#### 3. Application Access Points
- **Main Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Interactive API**: http://localhost:8000/redoc

### First Time User Experience

#### 1. Landing Page
- Clean, professional landing page
- "Login with Google (Demo)" button
- Project information and features

#### 2. After Login (Demo Mode)
- Home page with navigation dropdown
- Available features: Sprint Planning, Risk Assessment, etc.
- User profile information

#### 3. Sprint Planning Feature
- Interactive chat interface
- AI-powered questions about your sprint
- Dynamic conversation flow
- Generated sprint plan summary

#### 4. Risk Assessment Feature
- Document upload functionality
- Support for PDF, DOCX, and other formats
- AI-powered risk analysis
- Generated risk assessment reports

### Common First-Time Issues

#### If Backend Won't Start
- Check if port 8000 is already in use
- Verify Python virtual environment is activated
- Ensure all dependencies are installed
- Check database connection in `.env` file

#### If Frontend Won't Start
- Check if port 3000 is already in use
- Verify Node.js version (16+)
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and reinstall: `npm install`

#### If Database Connection Fails
- Ensure PostgreSQL service is running
- Check database credentials in `.env`
- Verify database exists: `psql -U postgres -d sprint_demo`
- Run database setup: `psql -U postgres -d sprint_demo -f database/setup.sql`

### Next Steps After Setup
1. **Explore the Features**: Try each feature in the dropdown menu
2. **Upload Documents**: Test the document processing capabilities
3. **Run Sprint Planning**: Experience the AI-powered chat interface
4. **Check API Documentation**: Visit http://localhost:8000/docs
5. **Customize**: Modify the code to add your own features

## Demo Flow

1. **Landing Page**: Click "Login with Google" to simulate authentication
2. **Home Page**: Select "sprint" from the dropdown menu
3. **Sprint Planning**: Click "Start Planning" to begin the interactive chat
4. **Chat Interface**: Answer dynamic questions from the LLM
5. **Summary**: View the Grok-generated sprint plan summary

## API Endpoints

### Authentication (Demo)
- `POST /api/auth/login` - Simulate Google OAuth login
- `POST /api/auth/logout` - Simulate logout

### Sprint Planning
- `POST /api/sprint/start` - Start a new sprint planning session
- `POST /api/sprint/chat` - Send message to LLM and get response
- `POST /api/sprint/finish` - Complete planning and get Grok summary

### Mock Endpoints
- `POST /api/llm/chat` - Mock LLM chat endpoint
- `POST /api/grok/summarize` - Mock Grok summarization endpoint

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://username:password@localhost:5432/sprint_demo
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_LLM_ENDPOINT=http://localhost:8000/api/llm/chat
REACT_APP_GROK_ENDPOINT=http://localhost:8000/api/grok/summarize
```

## Development Notes

- **Authentication**: Currently simulated - no real OAuth implementation
- **LLM Integration**: Mock responses for demo purposes
- **Grok API**: Stubbed endpoint returning sample summaries
- **Database**: PostgreSQL with basic user and session tables

## Future Enhancements

- Real Google OAuth integration
- Secure credential storage with hashing
- Expanded feature dropdowns (rpx, etc.)
- Real LLM API integration
- Actual Grok API integration
- User management and persistence
- Advanced sprint planning features

## Troubleshooting

### Common Issues & Solutions

#### 1. Database Connection Issues
**Problem**: `psycopg2.OperationalError: connection to server failed`
**Solutions**:
- Ensure PostgreSQL service is running
- Check credentials in `backend/.env`
- Verify database exists: `psql -U postgres -d sprint_demo`
- Test connection: `psql -U postgres -h localhost -p 5432`

#### 2. CORS Errors
**Problem**: `Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy`
**Solutions**:
- Add frontend URL to `CORS_ORIGINS` in backend `.env`
- Restart backend server after changes
- Check browser console for specific CORS errors

#### 3. Port Conflicts
**Problem**: `Port 8000 is already in use` or `Port 3000 is already in use`
**Solutions**:
- **Backend**: Change port in uvicorn command: `uvicorn main:app --reload --host 0.0.0.0 --port 8001`
- **Frontend**: Change port in `package.json` scripts or use: `PORT=3001 npm start`
- Kill existing processes: `lsof -ti:8000 | xargs kill` (Mac/Linux)

#### 4. Virtual Environment Issues
**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
**Solutions**:
- Ensure virtual environment is activated: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python path: `which python` (Mac/Linux) or `where python` (Windows)

#### 5. Node.js Dependencies Issues
**Problem**: `npm ERR! peer dep missing` or `Module not found`
**Solutions**:
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and `package-lock.json`: `rm -rf node_modules package-lock.json`
- Reinstall: `npm install`
- Check Node.js version: `node --version` (should be 16+)

#### 6. Environment Variables Issues
**Problem**: `KeyError: 'DATABASE_URL'` or configuration not loading
**Solutions**:
- Ensure `.env` file exists in `backend/` directory
- Check file permissions and syntax
- Restart backend server after changes
- Verify no spaces around `=` in `.env` file

### Logs & Debugging

#### Backend Logs
- **Location**: Terminal where uvicorn is running
- **Debug mode**: Add `--log-level debug` to uvicorn command
- **Common log locations**: Check for error messages in terminal output

#### Frontend Logs
- **Browser Console**: Press F12 → Console tab
- **Terminal**: Check npm start terminal for build errors
- **Network Tab**: Check API calls and responses

#### Database Logs
- **PostgreSQL logs**: Check system logs or PostgreSQL log directory
- **Connection testing**: Use `psql` command line tool

### Performance Optimization

#### Backend Optimization
- Use connection pooling for database
- Enable gzip compression
- Implement caching for static responses
- Monitor memory usage

#### Frontend Optimization
- Enable production build: `npm run build`
- Use React.memo for expensive components
- Implement lazy loading
- Optimize bundle size

## Production Deployment

### Environment Preparation

#### 1. Production Environment Variables
```bash
# Production .env configuration
DATABASE_URL=postgresql://prod_user:secure_password@prod_host:5432/sprint_demo_prod
SECRET_KEY=very-secure-production-secret-key
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
ENVIRONMENT=production
```

#### 2. Database Production Setup
```bash
# Create production database
psql -U postgres
CREATE DATABASE sprint_demo_prod;
CREATE USER prod_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE sprint_demo_prod TO prod_user;
\q

# Run migrations
psql -U prod_user -d sprint_demo_prod -f database/setup.sql
```

### Deployment Options

#### Option 1: Docker Deployment
```dockerfile
# Dockerfile for backend
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Option 2: Cloud Platform Deployment
- **Heroku**: Use Procfile and environment variables
- **AWS**: Use Elastic Beanstalk or ECS
- **Google Cloud**: Use App Engine or Cloud Run
- **Azure**: Use App Service

#### Option 3: VPS Deployment
```bash
# Install dependencies
sudo apt update
sudo apt install nginx postgresql python3-pip nodejs npm

# Setup reverse proxy
sudo nano /etc/nginx/sites-available/sprint-demo
# Configure nginx to proxy to backend and serve frontend

# Setup systemd service
sudo nano /etc/systemd/system/sprint-demo.service
# Configure service to run backend

# Enable services
sudo systemctl enable sprint-demo
sudo systemctl start sprint-demo
```

### Security Considerations

#### 1. Environment Security
- Use strong, unique passwords
- Rotate secrets regularly
- Use environment-specific configurations
- Never commit `.env` files to version control

#### 2. Database Security
- Use SSL connections
- Implement connection limits
- Regular backups
- Access control and user permissions

#### 3. Application Security
- Enable HTTPS in production
- Implement rate limiting
- Input validation and sanitization
- Regular security updates

### Monitoring & Maintenance

#### 1. Health Checks
- Implement `/health` endpoint
- Monitor database connectivity
- Set up uptime monitoring
- Log application metrics

#### 2. Backup Strategy
- Regular database backups
- Configuration backup
- Code repository backup
- Disaster recovery plan

#### 3. Updates & Maintenance
- Regular dependency updates
- Security patches
- Performance monitoring
- User feedback collection

## Contributing

This is a demo application. For production use, implement proper security measures, real OAuth flows, and actual API integrations. #   P M - p o r t a l 
 
 