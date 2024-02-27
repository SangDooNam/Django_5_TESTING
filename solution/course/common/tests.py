from django.test import TestCase, tag
from django.urls import reverse
from .forms import LoginForm
# Create your tests here.


class CommonTest(TestCase):
    
    def setUp(self):
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.username = 'admin'
        self.password = 'admin'
        self.response_home = self.client.get(reverse('home'))
        self.response_login = self.client.get(reverse('login'))
        self.response_logout = self.client.get(reverse('logout'))
        self.response_note_details = self.client.get(reverse('redirect-to-note-detail', args=[1,]))
        self.response_redirected_from_logout_to_home = self.client.get(self.logout_url, follow=True)
        self.the_old_url = reverse('redirect-to-note-detail', args=[1,])
        self.response_redirected_from_old_to_new = self.client.get(self.the_old_url, follow=True)
        self.login_data = {
            'user_name': self.username,
            'password': self.password,
            }
        self.login_data_missing_username = {
            'user_name': '',
            'password': self.password,
        }
        self.login_data_missing_password = {
            'user_name': self.username,
            'password': '',
        }
    
    @tag('path')
    def test_page_status_code(self):
        self.assertEqual(self.response_home.status_code, 200)
        
        
    @tag('path', 'session', 'auth', 'redirect')
    def test_logout_path_session_auth_redirect(self):
        
        self.assertEqual(self.response_login.status_code, 200)
        
        self.assertEqual(self.response_logout.status_code, 302)
        
        session = self.client.session
        
        self.assertEqual(session.get('user_name'), None)
        self.assertNotIn('user_votes', session)
        self.assertFalse(session.get('user_can_write_notes'))
        
        self.assertRedirects(self.response_redirected_from_logout_to_home, reverse('home'))

        
    @tag('path', 'redirect')
    def test_old_details_path_redirection(self):
        self.assertEqual(self.response_note_details.status_code, 302)
        self.assertRedirects(self.response_redirected_from_old_to_new, reverse('notes:details', args=[1]))
        
        
    @tag('path', 'auth')
    def test_login_path(self):
        
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, 302)
    
    
    @tag('path', 'session', 'auth',)
    def test_login_post_redirect_and_session_data(self):
        
        self.assertEqual(self.response_login.status_code, 200)
        
        response = self.client.post(self.login_url, self.login_data)
        
        self.assertEqual(response.status_code, 302)
        
        session = self.client.session
        
        self.assertEqual(session.get('user_name'), 'admin')
        
        self.assertIn('user_votes', session)
        
        self.assertTrue(session.get('user_can_write_notes'))
    
    
    @tag('redirect', 'auth')
    def test_redirect_after_login_to_home(self):
        
        response = self.client.post(self.login_url, self.login_data)
        
        self.assertRedirects(response, reverse('home'))
    
    
    @tag('form', 'auth')
    def test_login_in_form_field_validation(self):
        
        form_missing_username = LoginForm(data=self.login_data_missing_username)
        
        self.assertFalse(form_missing_username.is_valid())
        
        self.assertTrue(form_missing_username.has_error('user_name'))
        
        form_missing_password = LoginForm(data=self.login_data_missing_password)
        
        self.assertFalse(form_missing_password.is_valid())
        
        self.assertTrue(form_missing_password.has_error('password'))