import json
import logging
import os
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List, Dict, Any

# Initialize Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "default-key"))

class ResumeAnalysisResult(BaseModel):
    ats_score: int
    selection_probability: float
    suggestions: List[str]
    focus_areas: List[str]
    strengths: List[str]
    weaknesses: List[str]

def analyze_resume(resume_text: str, job_position: str) -> Dict[str, Any]:
    """
    Analyze resume using Gemini AI and return structured feedback
    """
    try:
        system_prompt = (
            "You are an expert ATS (Applicant Tracking System) analyzer and career counselor. "
            "Analyze the provided resume for the specified job position and provide detailed feedback. "
            "Your analysis should include:\n"
            "1. ATS compatibility score (0-100)\n"
            "2. Selection probability (0.0-1.0)\n"
            "3. Specific improvement suggestions\n"
            "4. Key focus areas for improvement\n"
            "5. Current strengths\n"
            "6. Areas of weakness\n\n"
            "Respond with JSON in this exact format:\n"
            "{\n"
            "  \"ats_score\": number,\n"
            "  \"selection_probability\": number,\n"
            "  \"suggestions\": [\"suggestion1\", \"suggestion2\"],\n"
            "  \"focus_areas\": [\"area1\", \"area2\"],\n"
            "  \"strengths\": [\"strength1\", \"strength2\"],\n"
            "  \"weaknesses\": [\"weakness1\", \"weakness2\"]\n"
            "}"
        )

        user_prompt = f"""
        Target Job Position: {job_position}
        
        Resume Content:
        {resume_text}
        
        Please analyze this resume for the specified position and provide detailed feedback focusing on:
        - Keyword optimization for ATS systems
        - Skills alignment with job requirements
        - Experience relevance and presentation
        - Format and structure improvements
        - Missing critical elements
        """

        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                types.Content(role="user", parts=[types.Part(text=user_prompt)])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=ResumeAnalysisResult,
            ),
        )

        raw_json = response.text
        logging.info(f"Gemini Response: {raw_json}")

        if raw_json:
            data = json.loads(raw_json)
            return data
        else:
            raise ValueError("Empty response from Gemini API")

    except Exception as e:
        logging.error(f"Failed to analyze resume: {e}")
        # Return default response in case of error
        return {
            "ats_score": 0,
            "selection_probability": 0.0,
            "suggestions": [f"Analysis failed: {str(e)}"],
            "focus_areas": ["Technical Error"],
            "strengths": [],
            "weaknesses": ["Unable to analyze due to technical issues"]
        }

def get_detailed_feedback(resume_text: str, job_position: str) -> str:
    """
    Get detailed narrative feedback for the resume
    """
    try:
        prompt = f"""
        As an expert career counselor, provide detailed, actionable feedback for this resume targeting the position: {job_position}

        Resume Content:
        {resume_text}

        Provide comprehensive feedback covering:
        1. Overall impression and first thoughts
        2. Specific improvements for ATS optimization
        3. Content and experience suggestions
        4. Format and presentation recommendations
        5. Industry-specific advice for {job_position}

        Write in a professional, encouraging tone with specific actionable steps.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text or "Unable to generate detailed feedback at this time."

    except Exception as e:
        logging.error(f"Failed to get detailed feedback: {e}")
        return f"Error generating feedback: {str(e)}"
