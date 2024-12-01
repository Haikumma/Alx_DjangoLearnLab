from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import Book
User = get_user_model()

class BookTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ali', password='123')
        self.book = Book.objects.create(title='romantic', publication_year='2020', author="karim")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.login(username='ali', password='123')

    # Test for BookListView 
    def test_book_list(self):
        # Test for retrieving a list of books
        response = self.client.get(reverse('books/'))    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test for filtering books by title
        response = self.client.get(reverse('books/') + '?title=romantic')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'romantic')
        # Test for searching books by author
        response = self.client.get(reverse('books/') + '?search=karim')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0] ['author'], 'karim')
        # Test for ordering books by publication year
        response = self.client.get(reverse('books/') + '?ordering=publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
     
    # Test for BookDetailView
    def test_book_detail(self):    
        # Test for retrieving an existing book
        url = reverse('books', args=[self.book.id])  # Ensure this matches your detail URL name
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'title': 'romantic', 'author': 'karim', 'publication_year': '2020'})
        # Test for non-existent book
        url = reverse('books', args=[100])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test for CreateView
    def test_create_book(self):
        # Test for creating a new book
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('books')  # Ensure this matches your create URL name
        data = {'title': 'book a', 'author': 'author a', 'publication_year': '2015'}    
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.last().title, 'book a')
        # Test for missing required fields
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test for UpdateView
    def test_update_book(self):
        # Test for updating an existing book
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('books', args=[self.book.id])  # Ensure this matches your update URL name
        data = {'title': 'book b', 'author': 'author a', 'publication_year': '2015'}   
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'book b')
        # Test for missing required fields
        response = self.client.put(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_book(self):
        # Test for deleting an existing book
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('books', args=[self.book.id])  # Ensure this matches your delete URL name
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())
        # Test for non-existent book.
        url = reverse('books', args=[100])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)    

  