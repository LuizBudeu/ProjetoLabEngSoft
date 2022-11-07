# ### COPIANDO TESTES DO GITHUB ###
# from django.test import TestCase

# # Create your tests here.


# from catalog.models import Author
# from django.urls import reverse


# class AuthorListViewTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         # Create authors for pagination tests
#         number_of_authors = 13
#         for author_id in range(number_of_authors):
#             Author.objects.create(first_name='Christian {0}'.format(author_id),
#                                   last_name='Surname {0}'.format(author_id))

#     def test_view_monitoramento_url_exists_at_desired_location(self):
#         response = self.client.get('/monitoramento/')
#         self.assertEqual(response.status_code, 200)

#     def test_view_estado_url_exists_at_desired_location(self):
#         response = self.client.get('/monitoramento/estado')
#         self.assertEqual(response.status_code, 200)

#     def test_view_uses_correct_template(self):
#         response = self.client.get(reverse('authors'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'catalog/author_list.html')

#     def test_pagination_is_ten(self):
#         response = self.client.get(reverse('authors'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue('is_paginated' in response.context)
#         self.assertTrue(response.context['is_paginated'] is True)
#         self.assertEqual(len(response.context['author_list']), 10)

#     def test_lists_all_authors(self):
#         # Get second page and confirm it has (exactly) the remaining 3 items
#         response = self.client.get(reverse('authors')+'?page=2')
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue('is_paginated' in response.context)
#         self.assertTrue(response.context['is_paginated'] is True)
#         self.assertEqual(len(response.context['author_list']), 3)