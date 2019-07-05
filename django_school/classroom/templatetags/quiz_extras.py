from django import template
from classroom.models import StudentAnswer
register = template.Library()



@register.simple_tag
def marked_answer(user,opt):
    studentanswer = StudentAnswer.objects.filter(student=user.student, answer =opt)
    if studentanswer:
        if opt.is_correct:
            return 'correct'
        return 'wrong'

    return ''