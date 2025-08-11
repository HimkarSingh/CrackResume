import os
import json
import logging
from flask import render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from app import app, db
from models import ResumeAnalysis
from text_extractor import extract_text_from_file, save_uploaded_file, is_allowed_file
from gemini_analyzer import analyze_resume, get_detailed_feedback

@app.route('/')
def index():
    """
    Home page with file upload form
    """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and redirect to analysis
    """
    try:
        # Check if file was uploaded
        if 'resume_file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        file = request.files['resume_file']
        job_position = request.form.get('job_position', '').strip()
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
            
        if not job_position:
            flash('Please specify a target job position', 'error')
            return redirect(url_for('index'))
        
        if not file.filename or not is_allowed_file(file.filename):
            flash('Invalid file type. Please upload PDF, DOC, or DOCX files only.', 'error')
            return redirect(url_for('index'))
        
        # Save the uploaded file
        file_path = save_uploaded_file(file, app.config['UPLOAD_FOLDER'])
        if not file_path:
            flash('Failed to save uploaded file', 'error')
            return redirect(url_for('index'))
        
        # Extract text from the file
        filename = file.filename or "unknown.txt"
        extracted_text = extract_text_from_file(file_path, filename)
        if not extracted_text:
            flash('Failed to extract text from the uploaded file', 'error')
            # Clean up the uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
            return redirect(url_for('index'))
        
        # Analyze the resume using Gemini AI
        analysis_result = analyze_resume(extracted_text, job_position)
        
        # Save analysis to database
        analysis = ResumeAnalysis()
        analysis.filename = secure_filename(filename)
        analysis.job_position = job_position
        analysis.extracted_text = extracted_text
        analysis.ats_score = analysis_result.get('ats_score', 0)
        analysis.selection_probability = analysis_result.get('selection_probability', 0.0)
        analysis.suggestions = json.dumps(analysis_result.get('suggestions', []))
        analysis.focus_areas = json.dumps(analysis_result.get('focus_areas', []))
        
        db.session.add(analysis)
        db.session.commit()
        
        # Clean up the uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return redirect(url_for('show_analysis', analysis_id=analysis.id))
        
    except Exception as e:
        logging.error(f"Error in upload_file: {e}")
        flash(f'An error occurred while processing your file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/analysis/<int:analysis_id>')
def show_analysis(analysis_id):
    """
    Display analysis results
    """
    try:
        analysis = ResumeAnalysis.query.get_or_404(analysis_id)
        
        # Parse JSON strings back to lists
        suggestions = json.loads(analysis.suggestions) if analysis.suggestions else []
        focus_areas = json.loads(analysis.focus_areas) if analysis.focus_areas else []
        
        return render_template('analysis.html', 
                             analysis=analysis,
                             suggestions=suggestions,
                             focus_areas=focus_areas)
    except Exception as e:
        logging.error(f"Error in show_analysis: {e}")
        flash('Analysis not found or error loading results', 'error')
        return redirect(url_for('index'))

@app.route('/api/detailed-feedback/<int:analysis_id>')
def get_detailed_feedback_api(analysis_id):
    """
    API endpoint to get detailed feedback for an analysis
    """
    try:
        analysis = ResumeAnalysis.query.get_or_404(analysis_id)
        
        detailed_feedback = get_detailed_feedback(
            analysis.extracted_text, 
            analysis.job_position
        )
        
        return jsonify({
            'success': True,
            'feedback': detailed_feedback
        })
    except Exception as e:
        logging.error(f"Error getting detailed feedback: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(413)
def too_large(e):
    flash('File too large. Please upload a file smaller than 16MB.', 'error')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    flash('An internal server error occurred. Please try again.', 'error')
    return redirect(url_for('index'))
