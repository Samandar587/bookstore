from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from books.models import Author, Book, User, CartItem
from rest_framework.test import force_authenticate
from decimal import Decimal
from books.utils import is_book_available

class AuthorViewSetTest(APITestCase):
    def setUp(self):
        self.author1 = Author.objects.create(name='Author 1', bio='Bio 1')
        self.author2 = Author.objects.create(name='Author 2', bio='Bio 2')

    def test_author_list(self):
        url = reverse('author-list')
        response = self.client.get(url)

        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class BookViewSet(APITestCase):

    def setUp(self):
        self.url = reverse('book-list')
        self.search_url = reverse('book-search')

        self.author_data = {
            'name':'Test Author',
            'bio':'Test Bio'
        }

        self.book_data = {
                'title': 'Test Book',
                'author': self.author_data,
                'description': 'Test book description',
                'category': 'Test category',
                'price': 29.99,
                'pub_date': '2023-08-13',
                'quantity': 10
            }

        self.post_response = self.client.post(self.url, self.book_data, format='json')

    def test_book_create_list(self):
        

        self.assertEqual(self.post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.post_response.data.get('title', 'title key not found'), 'Test Book')
        self.assertEqual(self.post_response.data.get('author', {}).get('name', {}), 'Test Author')
        self.assertEqual(str(self.post_response.data.get('price', 'price key not found')),  str(29.99))
        self.assertEqual(str(self.post_response.data.get('quantity', 'quantity key not found')), str(10))

    def test_book_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_book_search(self):
        url = self.search_url
        full_url = url+'?query=Test'
        response = self.client.get(full_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    
class TestCartItemViewSet(APITestCase):
    def setUp(self):
        
        self.url = reverse('cartitem-list')
        self.url_add_to_cart = reverse('cartitem-add-to-cart')

        self.user = User.objects.create_user(
            username = 'testuser',
            email = 'test@example.com',
            password = 'testpass'
        )
        self.client.force_authenticate(user=self.user)

        self.author_instance = Author.objects.create(
            name='test author',
            bio='test bio'
        )
        
        self.book_instance = Book.objects.create(
            title = 'test book',
            author = self.author_instance,
            description = 'test book description',
            category = 'test category',
            price = 10,
            pub_date = '2023-08-13',
            quantity = 10
        )

    def test_add_to_cart(self):

        # tesing add_to_cart function
        url = self.url_add_to_cart
        cart_data = {
            'book_id':self.book_instance.id,
            'quantity':4
        }
        response = self.client.post(url, cart_data, 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('book', {}).get('title'), 'test book')
        self.assertEqual(str(response.data.get('quantity')), str(4))
        self.assertEqual(str(response.data.get('book', {}).get('quantity', {})), str(10))


    def test_remove_from_cart(self):
        
        cart_item = CartItem.objects.create(
            user=self.user,
            book=self.book_instance,
            quantity=2
        )
        url = reverse('cartitem-remove-from-cart', args=[cart_item.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.filter(id=cart_item.id).exists(), False)

    def test_remove_from_cart_not_found(self):
        cart_item = CartItem.objects.create(
            user=self.user,
            book=self.book_instance,
            quantity=3
        )
        url = reverse('cartitem-remove-from-cart', args=[100])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('detail'), 'Cart Item is not found.')
        
    def test_checkout_process(self):
        cart_item = CartItem.objects.create(
            user=self.user,
            book=self.book_instance,
            quantity=7
        )
        url = '/books/api/checkout'
        response = self.client.post(url)
        for item in response.data.get('items'):
            self.assertEqual(item.get('quantity'), 7)
            self.assertEqual(item.get('book', {}).get('quantity', {}), 3)
            self.assertEqual(item.get('book', {}).get('price', {}), '10.00')
            self.assertEqual(item.get('book', {}).get('title', {}), 'test book')

        self.assertEqual(response.data.get('status'), 'Pending')
        self.assertEqual(response.data.get('total_price'), '70.00')

    def test_is_book_available(self):
        cart_item = CartItem.objects.create(
            user=self.user,
            book=self.book_instance,
            quantity=11
        )
        url = reverse('cartitem-add-to-cart')
        cart_data = {
            'book_id':self.book_instance.id,
            'quantity':11
        }
        response = self.client.post(url, cart_data, 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Book is not available in the requested quantity.')

    def test_book_does_not_exist(self):
        data = is_book_available(777, 5)
        self.assertEqual(data, False)

        


        
        



        


