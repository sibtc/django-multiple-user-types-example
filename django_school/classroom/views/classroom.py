from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.db.models import Count
from classroom.models import Quiz

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:quiz_change_list')
        elif request.user.is_student:
            return redirect('students:quiz_list')
        else:
            return redirect('admin:index')

    return render(request,'classroom/quiz_list.html',{
        'quizzes':Quiz.objects.annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)})

class AboutView(TemplateView):
    template_name = 'classroom/about.html'