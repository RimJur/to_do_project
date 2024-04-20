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
        self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'tasks/task_list.html')

    def test_task_detail_view(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get('/task/1/')
        no_response = self.client.get('/task/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertContains(response, 'Hi, testuser!')
        self.assertTemplateUsed(response, 'tasks/task.html')

    def test_task_create_view(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.post(reverse('create'), {
            'title': 'New title',
            'description': 'New text',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New title')
        self.assertContains(response, 'New text')

    def test_task_update_view(self):
        url = reverse('edit', kwargs={'pk': '1'})
        response = self.client.post(url, {
            'title': 'Updated title',
            'description': 'Updated text',
        })
        self.assertEqual(response.status_code, 302)

    def test_task_delete_view(self):
        response = self.client.post(
            reverse('delete', args='1')
        )
        self.assertEqual(response.status_code, 302)


class NoTaskTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'test@gmail.com',
            password = 'secret'
        )

    def test_no_tasks_available(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('tasks'))
        self.assertContains(response, 'No tasks found!')


class GuestAccessTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'test@gmail.com',
            password = 'secret'
        )
                
        self.task = Task.objects.create(
            title = 'A good title',
            description = 'This is a nice task',
            user = user,
        )

    def test_access_update_page(self):
        response = self.client.get(reverse('edit', args='1'))
        self.assertEqual(response.status_code, 302)

    def test_access_delete_page(self):
        response = self.client.get(reverse('delete', args='1'))
        self.assertEqual(response.status_code, 302)

    def test_access_create_page(self):
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 302)

    def test_no_tasks_available_for_guest(self):
        response = self.client.get(reverse('tasks'))
        self.assertContains(response, 'Please log in to view your tasks.')


class OnlyMyTasks(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'test@gmail.com',
            password = 'secret'
        )

        self.user = get_user_model().objects.create_user(
            username = 'me',
            email = 'test@gmail.com',
            password = 'secret'
        )
                
        self.ongoing_task = Task.objects.create(
            title = 'A good title',
            description = 'This is a nice task',
            user = user,
        )

        self.completed_task = Task.objects.create(
            title = 'A second task of user',
            description = 'This is a nice task',
            completed = True,
            user = user,
        )

        self.task = Task.objects.create(
            title = 'A task of mine',
            description = 'This is a nice task',
            user = self.user,
        )

    def test_i_see_my_task(self):
        self.client.login(username='me', password='secret')
        response = self.client.get(reverse('tasks'))
        self.assertContains(response, 'A task of mine')
        self.assertNotContains(response, 'A good title')
        self.assertNotContains(response, 'A second task of user')

    def test_user_see_his_tasks(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('tasks'))
        self.assertNotContains(response, 'A task of mine')
        self.assertContains(response, 'A good title')
        self.assertContains(response, 'A second task of user')

    def test_completed_task_crossed_out(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('tasks'))
        self.assertContains(response, f'<s><h4><a href="/task/{self.completed_task.pk}/">Task: {self.completed_task.title}</a></h4></s>', html=True)
        self.assertContains(response, f'<h3><a href="/task/{self.ongoing_task.pk}/">Task: {self.ongoing_task.title}</a></h3>', html=True)