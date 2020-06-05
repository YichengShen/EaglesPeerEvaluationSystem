from . import views
from django.urls import path
from django.conf.urls import url


urlpatterns = [
    path('student-dashboard', views.student_dashboard, name='student-dashboard'),
    path('peer-assessments', views.peer_assessments, name='peer-assessments'),
    path('completed-assessments', views.completed_assessments, name='completed-assessments'),
    path('answer-assessment/<int:assessment_id>/', views.answer_assessment, name='answer-assessment'),

    # functions
    path('submit_assessment/<int:assessment_id>/', views.submit_assessment, name='submit_assessment'),
    path('edit_assessment/<int:assessment_id>/', views.edit_assessment, name='edit_assessment'),
    
]