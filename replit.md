# Overview

CrackResume is an AI-powered resume analysis web application that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS). The application allows users to upload resume files (PDF, DOC, DOCX), specify a target job position, and receive detailed AI-powered feedback including ATS compatibility scores, selection probability, and actionable improvement suggestions. Built with Flask and integrated with Google's Gemini AI, the application provides comprehensive resume analysis with an intuitive web interface.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Web Framework**: Flask-based web application with server-side rendering using Jinja2 templates
- **UI Framework**: Bootstrap 5 for responsive design and styling
- **Interactive Elements**: Chart.js for data visualization and custom JavaScript for file upload handling
- **File Upload**: Drag-and-drop interface with client-side file validation

## Backend Architecture
- **Web Framework**: Flask application with modular structure separating routes, models, and business logic
- **Database ORM**: SQLAlchemy with declarative base model for database operations
- **File Processing**: Dedicated text extraction module supporting multiple file formats (PDF via PyPDF2, DOC/DOCX via docx2txt)
- **AI Integration**: Google Gemini AI client for resume analysis with structured response parsing using Pydantic models
- **Session Management**: Flask sessions with configurable secret key for user state management

## Data Storage
- **Primary Database**: SQLite for development (configurable to other databases via DATABASE_URL)
- **Database Schema**: Single table architecture storing resume analysis results with JSON serialization for complex data
- **File Storage**: Local file system storage in uploads directory with secure filename handling
- **Connection Pool**: SQLAlchemy connection pooling with health checks and automatic reconnection

## Authentication and Authorization
- **Current State**: No authentication system implemented
- **Security Measures**: Secure filename processing, file type validation, and file size limits (16MB max)
- **Session Security**: Configurable session secret key with environment variable override

## AI Analysis Engine
- **Primary AI Service**: Google Gemini API for resume analysis
- **Analysis Components**: ATS scoring, selection probability calculation, suggestions generation, strengths/weaknesses identification
- **Response Structure**: Structured JSON responses validated with Pydantic models
- **Error Handling**: Comprehensive logging and fallback mechanisms for AI service failures

# External Dependencies

## AI Services
- **Google Gemini AI**: Primary AI service for resume analysis and feedback generation
- **API Configuration**: Environment variable-based API key management

## File Processing Libraries
- **PyPDF2**: PDF text extraction and processing
- **docx2txt**: Microsoft Word document text extraction
- **Werkzeug**: Secure file upload handling and utilities

## Web Framework Stack
- **Flask**: Core web application framework
- **Flask-SQLAlchemy**: Database ORM and connection management
- **Jinja2**: Template rendering engine (included with Flask)

## Frontend Libraries (CDN)
- **Bootstrap 5**: UI framework and responsive design
- **Font Awesome**: Icon library for enhanced UI
- **Chart.js**: Data visualization for analysis results

## Database Support
- **SQLite**: Default database for development and testing
- **PostgreSQL**: Configurable via DATABASE_URL environment variable for production deployments

## Development Tools
- **ProxyFix**: WSGI middleware for handling proxy headers in deployment environments
- **Python Logging**: Comprehensive logging system for debugging and monitoring