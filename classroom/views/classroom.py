from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:quiz_change_list')
        else:
            return redirect('students:quiz_list')
    return render(request, 'classroom/home.html')

def home_page(request) :
    logout(request)
    return render(request, 'classroom/home.html')