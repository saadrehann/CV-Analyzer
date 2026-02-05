from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.files.uploadedfile import UploadedFile
from .models import CVUpload, ATSAnalysis
from .serializers import ATSAnalysisSerializer
from .cv_parser import CVParser
from .ats_scorer import ATSScorer
import os


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_and_analyze_cv(request):
    """
    API endpoint to upload CV and get ATS analysis
    
    POST /api/upload-cv/
    """
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    uploaded_file = request.FILES['file']
    
    # Validate file type
    filename = uploaded_file.name
    file_extension = os.path.splitext(filename)[1].lower()
    
    if file_extension not in ['.pdf', '.docx', '.doc']:
        return Response(
            {'error': 'Invalid file type. Please upload PDF or DOCX file.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate file size (5MB limit)
    if uploaded_file.size > 5 * 1024 * 1024:
        return Response(
            {'error': 'File size exceeds 5MB limit'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Save CV upload
        cv_upload = CVUpload.objects.create(
            file=uploaded_file,
            filename=filename,
            file_type=file_extension[1:]  # Remove the dot
        )
        
        # Parse CV
        file_type = file_extension[1:]  # Remove dot from extension
        cv_upload.file.seek(0)  # Reset file pointer
        extracted_text = CVParser.parse_cv(cv_upload.file, file_type)
        
        # Score CV
        scorer = ATSScorer(extracted_text)
        analysis_results = scorer.calculate_overall_score()
        
        # Create analysis record
        analysis = ATSAnalysis.objects.create(
            cv_upload=cv_upload,
            overall_score=analysis_results['overall_score'],
            keyword_score=analysis_results['category_scores']['keyword_score'],
            formatting_score=analysis_results['category_scores']['formatting_score'],
            experience_score=analysis_results['category_scores']['experience_score'],
            education_score=analysis_results['category_scores']['education_score'],
            skills_score=analysis_results['category_scores']['skills_score'],
            contact_score=analysis_results['category_scores']['contact_score'],
            extracted_text=extracted_text[:5000],  # Store first 5000 chars
            strengths=analysis_results['strengths'],
            improvements=analysis_results['improvements'],
            missing_elements=analysis_results['missing_elements']
        )
        
        # Serialize and return
        serializer = ATSAnalysisSerializer(analysis)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'Error processing CV: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_analysis(request, analysis_id):
    """
    API endpoint to retrieve analysis results
    
    GET /api/analysis/<id>/
    """
    try:
        analysis = ATSAnalysis.objects.get(id=analysis_id)
        serializer = ATSAnalysisSerializer(analysis)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ATSAnalysis.DoesNotExist:
        return Response(
            {'error': 'Analysis not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint
    
    GET /api/health/
    """
    return Response({'status': 'ok'}, status=status.HTTP_200_OK)
