from Core.models.Projects.Showcase import Showcase
from Core.models.Projects.ShowcaseUpdate import ShowcaseUpdate
from Core.tests import BaseTestCase
from rest_framework import status
from Core.models import Project, TextMessage, Event
from django.test import tag
from django.utils import timezone

@tag('Showcases', 'showcase-tests')
class ShowcaseTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(name="test", 
                                              creator=self.user)
        self.showcase = Showcase.objects.get(project=self.project,name="Generale")

    @tag('get','auth') 
    def test_showcase_list_auth(self):
        response = self.client.get(f'/api/projects/{self.project.id}/showcases/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.users.add(self.new_user)
        self.project.save()
        self.client.force_authenticate(user=self.new_user)
        response = self.client.get(f'/api/projects/{self.project.id}/showcases/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    @tag('get', 'auth')
    def test_showcase_list_last_message(self):
        showcase = self.project.showcases.all()[0]
        message = TextMessage.objects.create(text="test", author=self.user,
                                            showcase=showcase)
        Event.objects.create(author=self.user, date=timezone.now(),
                             showcase=showcase)
        response = self.client.get(f'/api/projects/{self.project.id}/showcases/')
        self.assertEqual(list(response.data)[0]['last_message']['id'], str(message.id))
        
    @tag('get','unauth') 
    def test_showcase_list_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.get(f'/api/projects/{self.project.id}/showcases/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    @tag('post','auth')
    def test_showcase_create_auth(self):
        data = {'name':'test', "users": [str(self.new_user.id)]}
        response = self.client.post(f'/api/projects/{self.project.id}/showcases/',data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['users_list'][0]['secret_key'], self.user.secret_key)
        self.project.users.add(self.new_user)
        self.project.save()
        self.client.force_authenticate(user=self.new_user)
        response = self.client.post(f'/api/projects/{self.project.id}/showcases/',data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['users_list'][0]['secret_key'], self.new_user.secret_key)

    @tag('post','unauth') 
    def test_showcase_create_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        data = {'name':'test'}
        response = self.client.post(f'/api/projects/{self.project.id}/showcases/',data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
      
    @tag('get', 'auth')  
    def test_message_viewed_by_auth(self):
        TextMessage.objects.create(text='test',showcase=self.showcase,author=self.new_user)
        response = self.client.get(f'/api/projects/{self.project.id}/showcases/')
        self.assertEqual(list(response.data)[0]["notify"], 1)
        
        self.client.get(f'/api/showcase/{self.showcase.id}/messages/')
        response = self.client.get(f'/api/projects/{self.project.id}/showcases/')
        self.assertEqual(list(response.data)[0]["notify"], 0)
        
    @tag('patch', 'auth', 'this') 
    def test_showcase_update_auth(self):
        data = {"description":"test"}
        response = self.client.patch(f"/api/showcase/{self.showcase.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(ShowcaseUpdate.objects.all().count(), 1)
    
    @tag('delete', 'auth', 'this') 
    def test_showcase_destroy_auth(self):
        response = self.client.delete(f"/api/showcase/{self.showcase.id}/")
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
    
    @tag('patch', 'unauth', 'this') 
    def test_showcase_update_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        data = {"description":"test"}
        response = self.client.patch(f"/api/showcase/{self.showcase.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.showcase.users.add(self.new_user)
        self.showcase.save()
        response = self.client.patch(f"/api/showcase/{self.showcase.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @tag('delete', 'unauth', 'this') 
    def test_showcase_destroy_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.delete(f"/api/showcase/{self.showcase.id}/")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.showcase.users.add(self.new_user)
        self.showcase.save()
        response = self.client.delete(f"/api/showcase/{self.showcase.id}/")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)