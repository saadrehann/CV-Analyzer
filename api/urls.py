from django.urls import path
from . import views

urlpatterns = [
    path('upload-cv/', views.upload_and_analyze_cv, name='upload-cv'),
    path('analysis/<uuid:analysis_id>/', views.get_analysis, name='get-analysis'),
    path('health/', views.health_check, name='health-check'),
]
