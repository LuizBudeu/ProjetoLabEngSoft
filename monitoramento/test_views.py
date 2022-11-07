from django.test import TestCase

# Create your tests here.


from django.urls import reverse


class MonitoramentoViewTest(TestCase):

    def test_view_url_exists_at_desired_location_login(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location_home(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location_crud(self):
        response = self.client.get('/crud/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location_crudcreate(self):
        response = self.client.get('/crud/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location_crudread(self):
        response = self.client.get('/crud/read/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location_crudupdate(self):
        response = self.client.get('/crud/update/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location_cruddelete(self):
        response = self.client.get('/crud/delete/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_exists_at_desired_location_relatorio(self):
        response = self.client.get('/relatorio/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_crud(self):
        response = self.client.get(reverse('crud'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_crudcreate(self):
        response = self.client.get(reverse('crudcreate'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_crudread(self):
        response = self.client.get(reverse('crudread'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_crudupdate(self):
        response = self.client.get(reverse('crudupdate'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_cruddelete(self):
        response = self.client.get(reverse('cruddelete'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name_relatorio(self):
        response = self.client.get(reverse('relatorio'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_view_uses_correct_template_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_view_uses_correct_template_crud(self):
        response = self.client.get(reverse('crud'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crud.html')

    def test_view_uses_correct_template_crudcreate(self):
        response = self.client.get(reverse('crudcreate'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crud-create.html')

    def test_view_uses_correct_template_crudread(self):
        response = self.client.get(reverse('crudread'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crud-read.html')

    def test_view_uses_correct_template_crudupdate(self):
        response = self.client.get(reverse('crudupdate'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crud-update.html')

    def test_view_uses_correct_template_cruddelete(self):
        response = self.client.get(reverse('cruddelete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crud-delete.html')
    
    def test_view_uses_correct_template_relatorio(self):
        response = self.client.get(reverse('relatorio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'relatorio.html')
