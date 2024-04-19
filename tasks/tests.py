from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Task
from django.contrib.auth.models import User

# Create your tests here.

class TaskTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'test@gmail.com',
            password = 'secret'
        )

        self.task = Task.objects.create(
            title = 'A good title',
            description = 'This is a nice task',
            user = self.user,
        )

    def test_string_representation(self):
        task = Task(title='A sample title')
        self.assertEqual(str(task), task.title)

    def test_get_absolute_url(self):
        self.assertEqual(self.task.get_absolute_url(), '/task/1/')

    def test_task_content(self):
        self.assertEqual(f'{self.task.title}', 'A good title')
        self.assertEqual(f'{self.task.user}', 'testuser')
        self.assertEqual(f'{self.task.description}', 'This is a nice task')

    def test_task_list_view(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'task_list.html')

    def test_task_detail_view(self):
        response = self.client.get('/task/1/')
        no_response = self.client.get('/task/100000')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'task.html')

    def test_task_create_view(self):
        self.client.login(username='testuser', password='secrer')
        response = self.client.post(reverse('create'), {
            'title': 'New title',
            'description': 'New text',
            'user': self.user,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New title')
        self.assertContains(response, 'New text')

    def test_task_update_view(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.post(reverse('edit', args='1'), {
            'title': 'Updated title',
            'description': 'Updated text',
        })
        self.assertEqual(response.status_code, 302)

    def test_task_delete_view(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.post(
            reverse('delete', args='1')
        )
        self.assertEqual(response.status_code, 302)

    def test_no_tasks_available(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('tasks'))
        self.assertContains(response, 'No tasks found!')