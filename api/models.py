from django.db import models
from django.utils import timezone
import uuid


class CVUpload(models.Model):
    """Model to store uploaded CV files"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='cvs/')
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10)  # pdf or docx
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at}"
    
    class Meta:
        ordering = ['-uploaded_at']


class ATSAnalysis(models.Model):
    """Model to store ATS analysis results"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cv_upload = models.OneToOneField(CVUpload, on_delete=models.CASCADE, related_name='analysis')
    
    # Overall score
    overall_score = models.IntegerField(default=0)  # 0-100
    
    # Category scores
    keyword_score = models.IntegerField(default=0)  # 0-100
    formatting_score = models.IntegerField(default=0)  # 0-100
    experience_score = models.IntegerField(default=0)  # 0-100
    education_score = models.IntegerField(default=0)  # 0-100
    skills_score = models.IntegerField(default=0)  # 0-100
    contact_score = models.IntegerField(default=0)  # 0-100
    
    # Extracted text
    extracted_text = models.TextField(blank=True)
    
    # Feedback JSON
    strengths = models.JSONField(default=list)
    improvements = models.JSONField(default=list)
    missing_elements = models.JSONField(default=list)
    
    # Analysis metadata
    analyzed_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Analysis for {self.cv_upload.filename} - Score: {self.overall_score}"
    
    @property
    def score_category(self):
        """Return score interpretation"""
        if self.overall_score >= 80:
            return "Excellent"
        elif self.overall_score >= 65:
            return "Good"
        elif self.overall_score >= 50:
            return "Fair"
        else:
            return "Needs Improvement"
    
    class Meta:
        ordering = ['-analyzed_at']
