# Deploying to Vercel

## Frontend Deployment

The React frontend is configured for Vercel deployment with the following setup:

### Prerequisites
1. Install Vercel CLI: `npm install -g vercel`
2. Create a Vercel account at https://vercel.com

### Deployment Steps

#### Option 1: Using Vercel CLI
```bash
cd cv-rater-frontend
vercel login
vercel
```

#### Option 2: Using Vercel Dashboard
1. Push your code to GitHub
2. Go to https://vercel.com/new
3. Import your repository
4. Vercel will auto-detect the Vite framework
5. Click "Deploy"

### Environment Variables

After deployment, you'll need to configure the backend API URL:

1. Go to your Vercel project settings
2. Navigate to "Environment Variables"
3. Add: `VITE_API_URL` = `https://your-backend-url.com/api`
4. Redeploy the application

**Important**: Update `src/services/api.ts` to use the environment variable:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
```

---

## Backend Deployment

The Django backend needs to be deployed separately. Recommended platforms:

### Option 1: Railway (Recommended)
1. Go to https://railway.app
2. Create new project from GitHub repo
3. Railway will auto-detect Django
4. Add environment variables:
   - `DJANGO_SETTINGS_MODULE=cv_rater_backend.settings`
   - `SECRET_KEY=your-secret-key`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-railway-domain.railway.app`
5. Deploy

### Option 2: Render
1. Go to https://render.com
2. New Web Service
3. Connect GitHub repository
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn cv_rater_backend.wsgi:application`
6. Add environment variables
7. Deploy

### Option 3: PythonAnywhere
1. Go to https://www.pythonanywhere.com
2. Upload your code
3. Configure WSGI file
4. Set up virtual environment
5. Deploy

---

## Post-Deployment Configuration

1. **Update CORS Settings** in Django `settings.py`:
   ```python
   CORS_ALLOWED_ORIGINS = [
       'https://your-vercel-app.vercel.app',
   ]
   ```

2. **Update Frontend API URL** in `src/services/api.ts`:
   ```typescript
   const API_BASE_URL = 'https://your-backend-url.com/api';
   ```

3. **Test the deployment**:
   - Visit your Vercel URL
   - Upload a test CV
   - Verify the full workflow

---

## Production Checklist

- [ ] Backend deployed and accessible
- [ ] Frontend environment variables configured
- [ ] CORS settings updated in Django
- [ ] API URL updated in React app
- [ ] Static files configured for Django
- [ ] Database migrations run on production
- [ ] SSL/HTTPS enabled
- [ ] Error tracking configured (optional: Sentry)
- [ ] Performance monitoring enabled
