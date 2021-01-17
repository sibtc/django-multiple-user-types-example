from django.test import TestCase, Client

from django.urls import reverse

class LoginPageTest(TestCase):
    fixtures = ["datas.json"]

    def setUp(self):
        self.client = Client()

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

    
    def test_guest_user_can_access_student_list(self):
        home_url = reverse('home')
        student_list_url = reverse('students:student_list')
        about_url = reverse('about')
        
        # there is tab view in homepage and check there is student list url in home page
        response = self.client.get(student_list_url)
        tabs = f'''
        <ul class="nav nav-tabs mb-3">          
            <li class="nav-item"><a class="nav-link" href="{home_url}">Quizzes</a></li>
            <li class="nav-item"><a class="nav-link active" href="{student_list_url}">Students</a></li>
            <li class="nav-item"><a class="nav-link" href="{about_url}">About</a></li>
        </ul>'''
        self.assertInHTML(tabs, response.content.decode())
        
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


    def test_guest_user_can_access_quiz_list(self):
        home_url = reverse('home')
        response = self.client.get(home_url)
        student_list_url = reverse('students:student_list')
        about_url = reverse('about')
        
        # there is tab view in homepage and check there is quiz list url in home page

        tabs = f'''
        <ul class="nav nav-tabs mb-3">          
            <li class="nav-item"><a class="nav-link active" href="{home_url}">Quizzes</a></li>
            <li class="nav-item"><a class="nav-link" href="{student_list_url}">Students</a></li>
            <li class="nav-item"><a class="nav-link" href="{about_url}">About</a></li>
        </ul>'''
        
        self.assertInHTML(tabs, response.content.decode())

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