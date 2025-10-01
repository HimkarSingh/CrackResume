# CrackResume

CrackResume is an AI-powered resume analysis web application that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS). Users can upload their resume (PDF, DOC, DOCX), specify the target job position, and receive detailed AI-powered feedback including:

- ATS compatibility scores
- Selection probability
- Actionable improvement suggestions

The app is built with Flask and integrates Google's Gemini AI to provide comprehensive resume analysis through a simple web interface.

## Features

- **AI Analysis**: Uses Google Gemini AI for resume feedback and scoring.
- **ATS Scoring**: Instantly see how your resume performs in Applicant Tracking Systems.
- **Actionable Suggestions**: Get specific advice for improvement.
- **Multiple Formats Supported**: PDF, DOC, DOCX uploads.
- **Modern UI**: Responsive design with Bootstrap 5, drag-and-drop file upload.
- **Data Visualization**: Analysis results visualized with Chart.js.

## System Architecture

### Frontend

- **Web Framework**: Flask (server-side rendering with Jinja2 templates)
- **UI Framework**: Bootstrap 5 for responsive and modern design
- **Data Visualization**: Chart.js for displaying analysis results
- **File Upload**: Drag-and-drop upload with client-side validation (PDF, DOC, DOCX, max 16MB)
- **Custom JavaScript**: Interactive file upload handling and alerts

### Backend

- **Web Framework**: Flask with modular structure (routes, models, business logic)
- **Database ORM**: SQLAlchemy with declarative base for database operations
- **File Processing**: Text extraction module for PDF (PyPDF2), DOC/DOCX (docx2txt)
- **AI Integration**: Google Gemini AI for resume analysis, using structured JSON validation via Pydantic
- **Session Management**: Flask sessions with configurable secret key for user state management

### Data Storage

- **Primary Database**: SQLite for development (configurable to PostgreSQL for production)
- **Database Schema**: Single table architecture storing resume analysis results, using JSON serialization for complex data
- **File Storage**: Local uploads directory with secure filename handling
- **Connection Pool**: SQLAlchemy pooling with health checks and automatic reconnection

### Security

- **File Validation**: Allowed types and file size limits enforced
- **Session Security**: Secret key configuration via environment variables
- **Error Handling**: Logging and fallback mechanisms for AI service failures
