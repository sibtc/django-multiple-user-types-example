from django.urls import include, path

from classroom.views import classroom, students, teachers
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('classroom.urls')),
    path('accounts/login/', auth_views.login, name='login', kwargs={'redirect_field_name': '/', 'redirect_authenticated_user': True}),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', classroom.SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', students.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/teacher/', teachers.TeacherSignUpView.as_view(), name='teacher_signup'),
]
