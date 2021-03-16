from django.test import TestCase, Client

from django.urls import reverse
from django.template import Template, Context


from classroom.models import Student

class LoginPageTest(TestCase):
    fixtures = ["datas.json"]

    def setUp(self):
        self.client = Client()
        self.student = Student.objects.get(user__username = 'student')

        self.home_url = reverse('home')
        self.student_list_url = reverse('students:student_list')
        self.about_url = reverse('about')

        self.tabs = f'''
        <ul class="nav nav-tabs mb-3">          
            <li class="nav-item"><a class="nav-link active" href="{self.home_url}">Quizzes</a></li>
            <li class="nav-item"><a class="nav-link" href="{self.student_list_url}">Students</a></li>
            <li class="nav-item"><a class="nav-link" href="{self.about_url}">About</a></li>
        </ul>'''

        self.tabs = lambda active_tab='': f'''
        <ul class="nav nav-tabs mb-3">          
            <li class="nav-item"><a class="nav-link{' active' if active_tab=='home' else ''}" href="{self.home_url}">Quizzes</a></li>
            <li class="nav-item"><a class="nav-link{' active' if active_tab=='students' else ''}" href="{self.student_list_url}">Students</a></li>
            <li class="nav-item"><a class="nav-link{' active' if active_tab=='about' else ''}" href="{self.about_url}">About</a></li>
        </ul>'''

    def test_login_page_returns_correct_html(self):
        loginurl = reverse('login')
        response = self.client.get(loginurl)
        self.assertEqual(response.status_code,200)
        # test response contains Username and Password
        self.assertIn(b'Username', response.content)
        self.assertIn(b'Password', response.content)

        # blank fields
        response = self.client.post(loginurl)
        self.assertIn(b'This field is required.', response.content)
        
        # wrong username or password
        response = self.client.post(loginurl, {'username':'bad', 'password':'bad'})
        self.assertIn(b'Please enter a correct username and password.', response.content)

    def test_login_as_teacher(self):
        loginurl = reverse('login')
        # login as teacher
        response = self.client.post(loginurl, {'username':'sumee', 'password':'sumee1910'}, follow=True)
        # print(response.redirect_chain)
        # self.assertEqual(response.redirect_chain[1][0],reverse('teachers:quiz_change_list'))
        # self.assertIn(b'My Quizzes', response.content)

    def test_guest_user_can_access_quiz_list(self):
        response = self.client.get(self.home_url)
        
        # there is tab view in homepage and check there is quiz list url in home page 
        self.assertInHTML(self.tabs('home'), response.content.decode())

        quiz1 = '''<tr>
            <td class="align-middle">World War 1</td>
            <td class="align-middle d-none d-sm-table-cell"><span class="badge badge-primary" style="background-color: #ffc107">History</span></td>
            <td class="align-middle d-none d-sm-table-cell">4</td>
            <td class="text-right" data-orderable="false">
                <a href="/students/quiz/1/" class="btn btn-primary">Start quiz</a>
            </td>
        </tr>
        '''
        self.assertInHTML(quiz1, response.content.decode())

    def test_guest_user_can_access_student_list(self):
        
        # there is tab view in homepage and check there is student list url in home page
        response = self.client.get(self.student_list_url)        
        self.assertInHTML(self.tabs('students'), response.content.decode())
        
        # guest user can access student list
        student_search_form = '''
            <form method='GET'>
              <div class="row">
                <div class="col-sm-6">
                  <div class="input-group mb-3">
                    <input type="text" class="form-control" name='q' value='' placeholder="Filter by username">
                    <div class="input-group-append">
                      <button class="btn btn-outline-secondary" type="submit">Search...</button>
                    </div>
                  </div>
                </div>
              </div>
            </form>
        '''
        self.assertInHTML(student_search_form, response.content.decode())

        
        # test students listed in the page
        student_detail_url = reverse('students:student_detail', kwargs={'student':self.student.pk})
        

        gravatar_url = Template('''
            {% load quiz_extras %} 
            <img class="mr-3" src="{{ student.user.username|gravatar_url:50 }}" alt="{{student.user.get_full_name}}">
        ''').render(Context({'student':self.student}))

        student_info = f'''
            <div class="col-sm-3">
                <div class="media">
                    <a href="{student_detail_url}">{gravatar_url}</a>
                    <div class="media-body" style="font-size: 12px">
                    <a href="{student_detail_url}">{self.student.user.username}</a><br>
                    <strong>0</strong><br>
                </div>
            </div>
        '''
        self.assertInHTML(student_info, response.content.decode())

    def test_guest_user_can_access_student_detail(self):

        student_detail_url = reverse('students:student_detail', kwargs={'student':self.student.pk})
        response = self.client.get(student_detail_url)

        self.assertInHTML(self.tabs('students'), response.content.decode())

        breadcrumb = f'''
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
              <li class="breadcrumb-item"><a href="{self.student_list_url}">Students</a></li>
              <li class="breadcrumb-item active" aria-current="page">{self.student.user.username}</li>
            </ol>
        </nav>
        '''
        # breadcrumb in student details page
        self.assertInHTML(breadcrumb, response.content.decode())


    def test_login_and_signup_page_contains_navbar(self):
        # check tabs in login page
        response = self.client.get(reverse('login'))
        self.assertInHTML(self.tabs(), response.content.decode())

        # check tabs in signup page
        response = self.client.get(reverse('signup'))
        self.assertInHTML(self.tabs(), response.content.decode())

        # check tabs in student_signup page
        # response = self.client.get(reverse('student_signup'))
        # self.assertInHTML(self.tabs(), response.content.decode())

        # check tabs in teacher_signup page
        response = self.client.get(reverse('teacher_signup'))
        self.assertInHTML(self.tabs(), response.content.decode())

        

