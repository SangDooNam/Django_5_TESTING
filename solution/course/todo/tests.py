from django.test import TestCase, tag
from django.urls import reverse


# Create your tests here.
class TodoTest(TestCase):
    
    def setUp(self) -> None:
        self.response_details = self.client.get(reverse('todo:details', args=[1,]))
    
    @tag('path')
    def test_tode_status_code(self):
        self.assertEqual(self.response_details.status_code, 200)

