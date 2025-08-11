from app import db
from datetime import datetime

class ResumeAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    job_position = db.Column(db.String(255), nullable=False)
    extracted_text = db.Column(db.Text)
    ats_score = db.Column(db.Integer)
    selection_probability = db.Column(db.Float)
    suggestions = db.Column(db.Text)  # JSON string
    focus_areas = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ResumeAnalysis {self.filename}>'
