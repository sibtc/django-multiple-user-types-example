"""
    Mixins for class-based views,
    that check user auth. and role
"""

from django.contrib.auth.mixins import UserPassesTestMixin


class StudentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_student


class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_teacher
