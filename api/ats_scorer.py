"""
ATS Scoring Engine
Analyzes CVs and provides ATS compatibility scores
"""
import re
from .cv_parser import CVParser


class ATSScorer:
    """Service to calculate ATS scores for CVs"""
    
    # Common keywords for different industries/roles
    COMMON_SKILLS = [
        'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node',
        'django', 'flask', 'spring', 'sql', 'mongodb', 'aws', 'azure', 'gcp',
        'docker', 'kubernetes', 'ci/cd', 'git', 'agile', 'scrum', 'project management',
        'communication', 'leadership', 'teamwork', 'problem solving', 'analytical',
        'machine learning', 'data analysis', 'ai', 'deep learning', 'tensorflow',
        'development', 'design', 'testing', 'qa', 'devops', 'security'
    ]
    
    EDUCATION_KEYWORDS = [
        'bachelor', 'master', 'phd', 'degree', 'diploma', 'bsc', 'msc',
        'university', 'college', 'institute', 'certification', 'certified'
    ]
    
    ACTION_VERBS = [
        'developed', 'designed', 'implemented', 'created', 'built', 'managed',
        'led', 'improved', 'increased', 'reduced', 'achieved', 'delivered',
        'established', 'optimized', 'streamlined', 'coordinated', 'executed'
    ]
    
    def __init__(self, text):
        """
        Initialize scorer with extracted CV text
        
        Args:
            text: Extracted text from CV
        """
        self.text = text
        self.text_lower = text.lower()
        self.sections = CVParser.extract_sections(text)
        self.email = CVParser.extract_email(text)
        self.phone = CVParser.extract_phone(text)
        
    def score_keywords(self):
        """
        Score based on keyword optimization (25%)
        Returns: (score 0-100, feedback list)
        """
        found_skills = []
        for skill in self.COMMON_SKILLS:
            if skill in self.text_lower:
                found_skills.append(skill)
        
        # Calculate score based on number of skills found
        skill_count = len(found_skills)
        if skill_count >= 15:
            score = 100
        elif skill_count >= 10:
            score = 80
        elif skill_count >= 7:
            score = 65
        elif skill_count >= 4:
            score = 50
        else:
            score = max(skill_count * 10, 20)
        
        feedback = {
            'score': score,
            'found_skills': found_skills[:10],  # Top 10
            'skill_count': skill_count
        }
        
        return score, feedback
    
    def score_formatting(self):
        """
        Score based on formatting and structure (20%)
        Returns: (score 0-100, feedback dict)
        """
        score = 0
        issues = []
        strengths = []
        
        # Check for proper sections
        section_count = sum(1 for v in self.sections.values() if v)
        if section_count >= 4:
            score += 30
            strengths.append("Well-organized with multiple sections")
        elif section_count >= 2:
            score += 20
            issues.append("Add more sections like Skills or Certifications")
        else:
            score += 10
            issues.append("Missing key sections")
        
        # Check for bullet points or lists (look for common bullet characters)
        bullet_pattern = r'[•●○■□▪▫–—-]\s'
        bullet_count = len(re.findall(bullet_pattern, self.text))
        if bullet_count >= 10:
            score += 25
            strengths.append("Good use of bullet points")
        elif bullet_count >= 5:
            score += 15
        else:
            issues.append("Use more bullet points for better readability")
        
        # Check length (ideal CV is 1-2 pages, roughly 500-1500 words)
        word_count = len(self.text.split())
        if 500 <= word_count <= 1500:
            score += 25
            strengths.append("Appropriate length")
        elif word_count < 500:
            score += 10
            issues.append("CV might be too brief")
        else:
            score += 15
            issues.append("CV might be too long")
        
        # Check for consistent formatting (capitalization patterns)
        lines = [line.strip() for line in self.text.split('\n') if line.strip()]
        if len(lines) > 5:
            score += 20
            strengths.append("Well-structured content")
        
        return min(score, 100), {'issues': issues, 'strengths': strengths}
    
    def score_experience(self):
        """
        Score based on experience relevance (20%)
        Returns: (score 0-100, feedback dict)
        """
        score = 0
        strengths = []
        improvements = []
        
        # Check if experience section exists
        if self.sections.get('experience', False):
            score += 30
            strengths.append("Experience section present")
        else:
            score += 10
            improvements.append("Add a clear Experience or Work History section")
        
        # Check for action verbs
        action_verb_count = sum(1 for verb in self.ACTION_VERBS if verb in self.text_lower)
        if action_verb_count >= 8:
            score += 35
            strengths.append("Strong use of action verbs")
        elif action_verb_count >= 5:
            score += 25
            improvements.append("Use more action verbs to describe achievements")
        else:
            score += 10
            improvements.append("Add action verbs (developed, led, improved, etc.)")
        
        # Check for numbers/metrics (quantifiable achievements)
        number_pattern = r'\b\d+%|\b\d+\s*(percent|million|thousand|users|projects)\b'
        metrics = re.findall(number_pattern, self.text_lower)
        if len(metrics) >= 5:
            score += 35
            strengths.append("Quantifiable achievements highlighted")
        elif len(metrics) >= 2:
            score += 20
            improvements.append("Add more quantifiable metrics to achievements")
        else:
            score += 5
            improvements.append("Include numbers and metrics to show impact")
        
        return min(score, 100), {'strengths': strengths, 'improvements': improvements}
    
    def score_education(self):
        """
        Score based on education and certifications (15%)
        Returns: (score 0-100, feedback dict)
        """
        score = 0
        details = []
        
        # Check if education section exists
        if self.sections.get('education', False):
            score += 50
            details.append("Education section found")
        else:
            score += 20
            details.append("Add an Education section")
        
        # Check for education keywords
        edu_keyword_count = sum(1 for keyword in self.EDUCATION_KEYWORDS if keyword in self.text_lower)
        if edu_keyword_count >= 3:
            score += 50
            details.append("Educational credentials mentioned")
        elif edu_keyword_count >= 1:
            score += 30
        
        return min(score, 100), {'details': details}
    
    def score_skills(self):
        """
        Score based on skills section (15%)
        Returns: (score 0-100, feedback dict)
        """
        score = 0
        feedback = []
        
        # Check if skills section exists
        if self.sections.get('skills', False):
            score += 40
            feedback.append("Dedicated Skills section present")
        else:
            score += 10
            feedback.append("Add a dedicated Skills section")
        
        # Check for technical skills mentioned
        technical_skills = ['python', 'java', 'javascript', 'sql', 'react', 'aws', 'docker', 'git']
        tech_count = sum(1 for skill in technical_skills if skill in self.text_lower)
        
        if tech_count >= 5:
            score += 60
            feedback.append("Multiple technical skills listed")
        elif tech_count >= 3:
            score += 40
            feedback.append("Some technical skills mentioned")
        else:
            score += 20
            feedback.append("List more specific technical skills")
        
        return min(score, 100), {'feedback': feedback}
    
    def score_contact(self):
        """
        Score based on contact information (5%)
        Returns: (score 0-100, feedback dict)
        """
        score = 0
        elements = []
        missing = []
        
        # Check for email
        if self.email:
            score += 50
            elements.append(f"Email: {self.email}")
        else:
            missing.append("Email address")
        
        # Check for phone
        if self.phone:
            score += 50
            elements.append(f"Phone: {self.phone}")
        else:
            missing.append("Phone number")
        
        return score, {'elements': elements, 'missing': missing}
    
    def calculate_overall_score(self):
        """
        Calculate overall ATS score and detailed feedback
        
        Returns:
            Dictionary with scores and feedback
        """
        # Calculate individual scores
        keyword_score, keyword_feedback = self.score_keywords()
        formatting_score, formatting_feedback = self.score_formatting()
        experience_score, experience_feedback = self.score_experience()
        education_score, education_feedback = self.score_education()
        skills_score, skills_feedback = self.score_skills()
        contact_score, contact_feedback = self.score_contact()
        
        # Calculate weighted overall score
        overall_score = int(
            keyword_score * 0.25 +
            formatting_score * 0.20 +
            experience_score * 0.20 +
            education_score * 0.15 +
            skills_score * 0.15 +
            contact_score * 0.05
        )
        
        # Compile strengths
        strengths = []
        if keyword_feedback.get('skill_count', 0) >= 7:
            strengths.append(f"Contains {keyword_feedback['skill_count']} relevant keywords")
        if formatting_feedback.get('strengths'):
            strengths.extend(formatting_feedback['strengths'])
        if experience_feedback.get('strengths'):
            strengths.extend(experience_feedback['strengths'])
        
        # Compile improvements
        improvements = []
        if keyword_feedback.get('skill_count', 0) < 7:
            improvements.append("Add more industry-specific keywords and skills")
        if formatting_feedback.get('issues'):
            improvements.extend(formatting_feedback['issues'])
        if experience_feedback.get('improvements'):
            improvements.extend(experience_feedback['improvements'])
        if skills_feedback.get('feedback'):
            improvements.extend([f for f in skills_feedback['feedback'] if 'add' in f.lower() or 'list' in f.lower()])
        
        # Compile missing elements
        missing_elements = []
        if contact_feedback.get('missing'):
            missing_elements.extend(contact_feedback['missing'])
        
        # Add section-based improvements
        for section, exists in self.sections.items():
            if not exists:
                missing_elements.append(f"{section.title()} section")
        
        return {
            'overall_score': overall_score,
            'category_scores': {
                'keyword_score': keyword_score,
                'formatting_score': formatting_score,
                'experience_score': experience_score,
                'education_score': education_score,
                'skills_score': skills_score,
                'contact_score': contact_score,
            },
            'strengths': strengths[:5],  # Top 5 strengths
            'improvements': improvements[:5],  # Top 5 improvements
            'missing_elements': missing_elements[:5],  # Top 5 missing
            'keyword_details': keyword_feedback,
        }
