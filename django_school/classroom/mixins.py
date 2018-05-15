"""
    Mixins for class-based views,
    that check user role, they count
    on decorators logic functionality!
"""

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from .decorators import student_required, teacher_required


class StudentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return login_required() and student_required()


class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return login_required() and teacher_required()
