# AI-Powered CV Rater

An intelligent web application that analyzes CVs and provides ATS (Applicant Tracking System) compatibility scores with detailed feedback and improvement recommendations.

## Features

- 📄 **Multiple Format Support**: Upload CVs in PDF or DOCX format
- 🎯 **Comprehensive ATS Scoring**: Get scored across 6 key categories:
  - Keyword Optimization (25%)
  - Formatting & Structure (20%)
  - Experience Relevance (20%)
  - Education & Certifications (15%)
  - Skills Match (15%)
  - Contact Information (5%)
- 💡 **Actionable Feedback**: Receive strengths, improvements, and missing elements
- 🎨 **Modern UI**: Beautiful, responsive design with glassmorphism effects
- ⚡ **Real-time Analysis**: Instant feedback on your CV

## Technologies Used

### Backend
- **Django 6.0** - Python web framework
- **Django REST Framework** - RESTful API
- **PyPDF2** - PDF parsing
- **python-docx** - DOCX parsing
- **SQLite** - Database

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Build tool
- **Axios** - HTTP client
- **React Dropzone** - Drag-and-drop file upload
- **React Circular Progressbar** - Score visualization

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the project root directory:
   ```bash
   cd c:/Hackathon
   ```

2. Install Python dependencies:
   ```bash
   pip install Django djangorestframework django-cors-headers PyPDF2 python-docx
   ```

3. Run database migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the Django development server:
   ```bash
   python manage.py runserver
   ```
   The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd cv-rater-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

## Usage

1. Open your browser and navigate to `http://localhost:5173`
2. Drag and drop your CV (PDF or DOCX) or click to browse
3. Click "Analyze CV" to get instant feedback
4. Review your ATS compatibility score
5. Check the detailed analysis for each category
6. Follow the recommendations to improve your CV

## API Endpoints

### Upload and Analyze CV
```
POST /api/upload-cv/
Content-Type: multipart/form-data

Body: { file: <CV file> }

Response: {
  id: string,
  overall_score: number,
  score_category: string,
  keyword_score: number,
  formatting_score: number,
  experience_score: number,
  education_score: number,
  skills_score: number,
  contact_score: number,
  strengths: string[],
  improvements: string[],
  missing_elements: string[]
}
```

### Get Analysis
```
GET /api/analysis/{id}/

Response: Same as above
```

### Health Check
```
GET /api/health/

Response: { status: 'ok' }
```

## ATS Scoring Algorithm

The application uses a weighted scoring system:

1. **Keyword Optimization (25%)**: Analyzes industry-specific keywords and technical skills
2. **Formatting & Structure (20%)**: Checks for proper sections, bullet points, and length
3. **Experience Relevance (20%)**: Evaluates action verbs and quantifiable achievements
4. **Education & Certifications (15%)**: Verifies educational credentials
5. **Skills Match (15%)**: Assesses technical and soft skills
6. **Contact Information (5%)**: Ensures complete contact details

## File Structure

```
c:/Hackathon/
├── api/                          # Django app
│   ├── models.py                # Database models
│   ├── serializers.py           # REST serializers
│   ├── views.py                 # API views
│   ├── cv_parser.py             # CV parsing service
│   ├── ats_scorer.py            # ATS scoring engine
│   └── urls.py                  # API routes
├── cv_rater_backend/            # Django project
│   ├── settings.py              # Django settings
│   └── urls.py                  # Main URL config
├── cv-rater-frontend/           # React frontend
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── services/            # API service
│   │   ├── App.tsx              # Main app
│   │   └── main.tsx             # Entry point
│   └── tailwind.config.js       # Tailwind config
├── manage.py                    # Django management
└── requirements.txt             # Python dependencies
```

## Security & Privacy

- File size limited to 5MB
- Only PDF and DOCX formats accepted
- Files are temporarily stored for analysis
- No permanent data storage of CV content
- CORS configured for local development

## Future Enhancements

- User authentication and history
- Multiple language support
- Job description matching
- AI-powered content suggestions
- Export analysis as PDF report
- Integration with job boards

## License

This project is created for demo purposes.

## Support

For issues or questions, please create an issue in the repository.
