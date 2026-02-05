from rest_framework import serializers
from .models import CVUpload, ATSAnalysis


class CVUploadSerializer(serializers.ModelSerializer):
    """Serializer for CV upload"""
    class Meta:
        model = CVUpload
        fields = ['id', 'file', 'filename', 'file_type', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class ATSAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for ATS analysis results"""
    cv_upload = CVUploadSerializer(read_only=True)
    score_category = serializers.CharField(read_only=True)
    
    class Meta:
        model = ATSAnalysis
        fields = [
            'id', 'cv_upload', 'overall_score', 'score_category',
            'keyword_score', 'formatting_score', 'experience_score',
            'education_score', 'skills_score', 'contact_score',
            'extracted_text', 'strengths', 'improvements',
            'missing_elements', 'analyzed_at'
        ]
        read_only_fields = ['id', 'analyzed_at']
