from . import views
from django.urls import path
from django.conf.urls import url


urlpatterns = [
    # path for pages
    path('professor-dashboard', views.professor_dashboard, name='professor-dashboard'),
    path('all-assessments', views.all_assessments, name='all-assessments'),
    path('create-new-assessment', views.create_new_assessment, name='create-new-assessment'),
    path('my-courses', views.my_courses, name='my-courses'),
    path('create-new-course', views.create_new_course, name='create-new-course'),
    path('teams-students', views.teams_students, name='teams-students'),
    
    # path for functions
    # functions for course
    path('make_new_course', views.make_new_course, name='make_new_course'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('add_student/<int:course_id>/', views.add_student, name='add_student'),
    path('remove_student/<int:course_id>/<str:eagle_id>/', views.remove_student, name='remove_student'),

    # functions for teams
    path('add_new_team', views.add_new_team, name='add_new_team'),
    path('delete_team/<int:team_id>/', views.delete_team, name='delete_team'),
    path('add_student_to_team/<int:team_id>/', views.add_student_to_team, name='add_student_to_team'),
    path('remove_student_from_team/<int:team_id>/<str:eagle_id>/', views.remove_student_from_team, name='remove_student_from_team'),

    # functions for assessment
    path('make_new_assessment', views.make_new_assessment, name='make_new_assessment'),
    path('delete_assessment/<int:assessment_id>/', views.delete_assessment, name='delete_assessment'),
    path('update_dates/<int:assessment_id>/', views.update_dates, name='update_dates'),
    path('close_and_release/<int:assessment_id>/', views.close_and_release, name='close_and_release'),
    path('download_csv/<int:assessment_id>/', views.download_csv, name='download_csv'),
    path('send_email_reminders/<int:assessment_id>/', views.send_email_reminders, name='send_email_reminders'),
    path('download_csv/<int:assessment_id>/', views.download_csv, name='download_csv'),
    
]