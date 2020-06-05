from . import views
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

# --------------- imports from other apps --------------------------
# import eval_student.views # eval_student app


urlpatterns = [
    path('', views.index, name='index'),
    path('student-login', views.student_login, name='student-login'),
    path('professor-login', views.professor_login, name='professor-login'),
    path('password-reset', views.password_reset, name='password-reset'),

    path('log_in', views.log_in, name='log_in'),
    path('log_out', views.log_out, name='log_out'),
    path('change_password', views.change_password, name='change_password'),

    # -------------- path to other Apps (Don't need this now, but leave as examples) ----------------------------
    # path('peer-assessments', eval_student.views.peer_assessments, name='peer-assessments'), # eval_student app
    # path('completed-assessments', eval_student.views.completed_assessments, name='completed-assessments'), # eval_student app
]