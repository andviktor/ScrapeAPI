from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Project, Scraper, Element

class UserTests(APITestCase):

    def test_create_user(self):
        """
        Testing the creation of a new user object.
        """
        url = reverse('user-list')

        # Params: empty
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Params: username
        data = {'username': 'testuser'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Params: username, password
        data = {
            'username': 'testuser',
            'password': 'testpass'
            }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get token
        url_auth = reverse('auth')
        response = self.client.post(url_auth, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_token = response.data['token']

class ProjectTests(APITestCase):

    def setUp(self):
        """
        Creating 2 users for testing.
        Storing tokens into self.headers list.
        """
        url = reverse('user-list')

        self.headers = []
        for i in range(2):
            data = {
                'username': f'test_user_{i}',
                'password': f'test_pass_{i}'
                }
            self.client.post(url, data)
            url_auth = reverse('auth')
            response = self.client.post(url_auth, data)
            self.user_token = response.data['token']
            self.headers.append({
                'Authorization': f'Token {self.user_token}'
            })

    def test_create_project(self):
        """
        Testing the creation of a new project object.
        """
        url = reverse('project-list')

        # Params: empty
        data = {}
        response = self.client.post(url, data, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Params: title
        data = {'title': 'test_project'}
        response = self.client.post(url, data, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_projects(self):
        """
        Testing getting a project and a list of projects for a current and another user.
        """
        url_list = reverse('project-list')

        # Creating projects for 2 users, 2 projects per user
        for i in range(2): # Two users
            for k in range(2): # Two projects per user
                data = {'title': f'test_project #{k}'}
                response = self.client.post(url_list, data, headers=self.headers[i])

        # Testing of the amount of the first user projects
        response = self.client.get(url_list, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        project_id = response.data[0]['id']

        url_detail = reverse('project-detail', kwargs={'pk':project_id})
        
        # Testing getting a project of a current user
        response = self.client.get(url_detail, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Testing getting a project with another user
        response = self.client.get(url_detail, headers=self.headers[1])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_project(self):
        """
        Testing updating a project for a current and another user.
        """
        
        # Creating projects for 2 users, 1 project per user
        url_list = reverse('project-list')
        projects = []
        for i in range(2): # Two users
            for k in range(1): # One project per user
                data = {'title': f'testproject of user #{i}'}
                response = self.client.post(url_list, data, headers=self.headers[i])
                projects.append(response.data['id'])

        # Preparing data for update
        data = {
            'title': 'updated title',
            'description': 'updated_description'
        }

        # Testing updating a project of a current user
        url_detail = reverse('project-detail', kwargs={'pk':projects[0]})
        response = self.client.patch(url_detail, data=data, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['description'], data['description'])

        # Testing updating a project of another user
        url_detail = reverse('project-detail', kwargs={'pk':projects[1]})
        response = self.client.patch(url_detail, data=data, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_project(self):
        """
        Testing the removal a project for a current and another user.
        """
        # Creating projects for 2 users, 1 project per user
        url_list = reverse('project-list')
        projects = []
        for i in range(2): # Two users
            for k in range(1): # One project per user
                data = {'title': f'testproject of user #{i}'}
                response = self.client.post(url_list, data, headers=self.headers[i])
                projects.append(response.data['id'])

        # Testing the removal a project of a current user
        url_detail = reverse('project-detail', kwargs={'pk':projects[0]})
        response = self.client.delete(url_detail, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Testing the removal a project of another user
        url_detail = reverse('project-detail', kwargs={'pk':projects[1]})
        response = self.client.delete(url_detail, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ScraperTests(APITestCase):

    def setUp(self):
        """
        1. Creating 2 users for testing. Storing tokens into self.headers list.
        2. Creating 2 projects. One project per user.
        """
        url = reverse('user-list')

        self.headers = []
        for i in range(2):
            data = {
                'username': f'test_user_{i}',
                'password': f'test_pass_{i}'
                }
            self.client.post(url, data)
            url_auth = reverse('auth')
            response = self.client.post(url_auth, data)
            self.user_token = response.data['token']
            self.headers.append({
                'Authorization': f'Token {self.user_token}'
            })

        url_list = reverse('project-list')
        self.projects = []
        for i in range(2): # Two users
            for k in range(1): # One project per user
                data = {'title': f'testproject of user #{i}'}
                response = self.client.post(url_list, data, headers=self.headers[i])
                self.projects.append(response.data['id'])

    def test_create_scraper(self):
        """
        Testing the creation of a new scraper object.
        """
        url = reverse('scraper-list')

        # Params: empty
        data = {}
        response = self.client.post(url, data, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Params: only title
        data = {'title': 'test_scraper'}
        response = self.client.post(url, data, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Params: only project
        data = {'project': self.projects[0]}
        response = self.client.post(url, data, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Testing creating a scraper for a current user
        data = {
            'title': 'test_scraper',
            'project': self.projects[0]
            }
        response = self.client.post(url, data, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Testing creating a scraper for another user
        data = {
            'title': 'test_scraper',
            'project': self.projects[1]
            }
        response = self.client.post(url, data, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_scrapers(self):
        """
        Testing getting a scraper and a list of scrapers for a current and another user.
        """
        url_list = reverse('scraper-list')

        # Creating scrapers for 2 users, 2 scrapers per user
        for i in range(2): # Two users
            for k in range(2): # Two scrapers per user
                data = {
                    'title': f'test_scraper #{k}, user {i}, project {i}',
                    'project': self.projects[i]
                    }
                response = self.client.post(url_list, data, headers=self.headers[i])

        # Testing of the amount of the first user scrapers
        response = self.client.get(url_list, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        scraper_id = response.data[0]['id']

        url_detail = reverse('scraper-detail', kwargs={'pk':scraper_id})
        
        # Testing getting a scraper of a current user
        response = self.client.get(url_detail, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Testing getting a scraper with another user
        response = self.client.get(url_detail, headers=self.headers[1])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_scraper(self):
        """
        Testing updating a scraper for a current and another user.
        """
        url_list = reverse('scraper-list')
        
        # Creating scrapers for 2 users, 2 scrapers per user
        scrapers = []
        for i in range(2): # Two users
            for k in range(2): # Two scrapers per user
                data = {
                    'title': f'test_scraper #{k}, user {i}, project {i}',
                    'project': self.projects[i]
                    }
                response = self.client.post(url_list, data, headers=self.headers[i])
                scrapers.append(response.data['id'])

        # Preparing data for update
        data = {
            'title': 'updated title'
        }

        # Testing updating a scraper of a current user
        url_detail = reverse('scraper-detail', kwargs={'pk':scrapers[0]})
        response = self.client.patch(url_detail, data=data, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])

        # Testing updating a scraper of another user
        url_detail = reverse('project-detail', kwargs={'pk':scrapers[2]})
        response = self.client.patch(url_detail, data=data, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_scraper(self):
        """
        Testing the removal a scraper for a current and another user.
        """
        url_list = reverse('scraper-list')

        # Creating scrapers for 2 users, 2 scrapers per user
        scrapers = []
        for i in range(2): # Two users
            for k in range(2): # Two scrapers per user
                data = {
                    'title': f'test_scraper #{k}, user {i}, project {i}',
                    'project': self.projects[i]
                    }
                response = self.client.post(url_list, data, headers=self.headers[i])
                scrapers.append(response.data['id'])

        # Testing the removal a scraper of a current user
        url_detail = reverse('scraper-detail', kwargs={'pk':scrapers[0]})
        response = self.client.delete(url_detail, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Testing the removal a scraper of another user
        url_detail = reverse('scraper-detail', kwargs={'pk':scrapers[2]})
        response = self.client.delete(url_detail, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ElementTests(APITestCase):

    def setUp(self):
        """
        1. Creating 2 users for testing. Storing tokens into self.headers list.
        2. Creating 2 projects. One project per user.
        3. Creating 4 scrapers. Two scrapes per project.
        """
        url = reverse('user-list')

        self.headers = []
        for i in range(2):
            data = {
                'username': f'test_user_{i}',
                'password': f'test_pass_{i}'
                }
            self.client.post(url, data)
            url_auth = reverse('auth')
            response = self.client.post(url_auth, data)
            self.user_token = response.data['token']
            self.headers.append({
                'Authorization': f'Token {self.user_token}'
            })

        url_list = reverse('project-list')
        self.projects = []
        for i in range(2): # Two users
            for k in range(1): # One project per user
                data = {'title': f'testproject of user #{i}'}
                response = self.client.post(url_list, data, headers=self.headers[i])
                self.projects.append(response.data['id'])
        
        # Creating scrapers for 2 projects, 1 scraper per project
        url_list = reverse('scraper-list')
        self.scrapers = []
        for i in range(2): # Two projects
            for k in range(1): # One scraper per project
                data = {
                    'title': f'test_scraper #{k}, user {i}, project {i}',
                    'project': self.projects[i]
                    }
                response = self.client.post(url_list, data, headers=self.headers[i])
                self.scrapers.append(response.data.get('id'))

    def test_create_element(self):
        """
        Testing the creation of a new element object.
        """
        url = reverse('element-list')

        # Params: empty
        data = {}
        response = self.client.post(url, data, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Params: title
        data = {'title': 'test_element'}
        response = self.client.post(url, data, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Params: title, xpath
        data = {
            'title': 'test_element',
            'xpath': 'test_xpath'
            }
        response = self.client.post(url, data, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Params: only scraper
        data = {'scraper': self.scrapers[0]}
        response = self.client.post(url, data, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Testing creating an element for a current user
        data = {
            'title': 'test_element',
            'xpath': 'test_xpath',
            'scraper': self.scrapers[0]
            }
        response = self.client.post(url, data, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Testing creating an element for another user
        data = {
            'title': 'test_element',
            'xpath': 'test_xpath',
            'scraper': self.scrapers[1]
            }
        response = self.client.post(url, data, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_elements(self):
        """
        Testing getting an element and a list of elements for a current and another user.
        """
        url_list = reverse('element-list')

        # Creating elements for 2 scrapers, 2 elements per scraper
        elements = []
        for i in range(2): # Two scrapers
            for k in range(2): # Two elements per scraper
                data = {
                    'title': f'test_element',
                    'xpath': 'test_xpath',
                    'scraper': self.scrapers[i]
                    }
                response = self.client.post(url_list, data, headers=self.headers[i])
                elements.append(response.data['id'])

        # Testing of the amount of the first user elements
        response = self.client.get(url_list, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        element_id = response.data[0]['id']

        url_detail = reverse('element-detail', kwargs={'pk':element_id})
        
        # Testing getting an element of a current user
        response = self.client.get(url_detail, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Testing getting an element with another user
        response = self.client.get(url_detail, headers=self.headers[1])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_element(self):
        """
        Testing updating an element for a current and another user.
        """
        url_list = reverse('element-list')
        
        # Creating elements for 2 scrapers, 2 elements per scraper
        elements = []
        for i in range(2): # Two scrapers
            for k in range(2): # Two elements per scraper
                data = {
                    'title': f'test_element',
                    'xpath': 'test_xpath',
                    'scraper': self.scrapers[i]
                    }
                response = self.client.post(url_list, data, headers=self.headers[i])
                elements.append(response.data['id'])

        # Preparing data for update
        data = {
            'title': 'updated title'
        }

        # Testing updating an element of a current user
        url_detail = reverse('element-detail', kwargs={'pk':elements[0]})
        response = self.client.patch(url_detail, data=data, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])

        # Testing updating an element of another user
        url_detail = reverse('element-detail', kwargs={'pk':elements[2]})
        response = self.client.patch(url_detail, data=data, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_element(self):
        """
        Testing the removal an element for a current and another user.
        """
        url_list = reverse('element-list')

        # Creating elements for 2 scrapers, 2 elements per scraper
        elements = []
        for i in range(2): # Two scrapers
            for k in range(2): # Two elements per scraper
                data = {
                    'title': f'test_element',
                    'xpath': 'test_xpath',
                    'scraper': self.scrapers[i]
                    }
                response = self.client.post(url_list, data, headers=self.headers[i])
                elements.append(response.data['id'])

        # Testing the removal an element of a current user
        url_detail = reverse('element-detail', kwargs={'pk':elements[0]})
        response = self.client.delete(url_detail, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Testing the removal an element of another user
        url_detail = reverse('element-detail', kwargs={'pk':elements[2]})
        response = self.client.delete(url_detail, headers=self.headers[0])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)