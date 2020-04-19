from django import template
from django.db.models import Sum

from classroom.models import StudentAnswer
import hashlib

register = template.Library()

@register.simple_tag
def marked_answer(user,opt):
    studentanswer = StudentAnswer.objects.filter(student=user.student, answer =opt)
    if studentanswer:
        if opt.is_correct:
            return 'correct'
        return 'wrong'
    return ''

@register.filter
def gravatar_url(username, size=40):
    # TEMPLATE USE:  {{ email|gravatar_url:150 }}
    username_hash = hashlib.md5(username.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{username_hash}?s={size}&d=identicon"

@register.filter
def top_subject(taken_quizzes):
    subjects = taken_quizzes.values('quiz__subject__name') \
        .annotate(score = Sum('score')) \
        .order_by('-score')
    if subjects:
        name = subjects[0]['quiz__subject__name']
        score = subjects[0]['score']
        return f"{name} x {score}"
    return ""