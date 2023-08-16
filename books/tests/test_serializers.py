from django.test import TestCase
from books.serializers.crud_serializers import AuthorSerializer, BookSerializer, UserProfileSerializer, CartItemSerializer, OrderSerializer
from books.models import Author, User

class TestSerialzers(TestCase):

    def setUp(self):
        self.author  = {
            'name': 'Test Author',
            'bio': 'Test author biography'
        }

    def test_author_serializer(self):
        author_data = {
            'name': 'Test Author',
            'bio': 'Test bio'
        }
        test_serializer = AuthorSerializer(data=author_data)
        self.assertTrue(test_serializer.is_valid())
        data = test_serializer.save()
        
        self.assertEqual(data.name, 'Test Author')
        self.assertEqual(data.bio, 'Test bio')

    def test_book_serializer(self):
        
        book_data = {
            'title': 'Test Book',
            'author': self.author,
            'description': 'Test book description',
            'category': 'Test category',
            'price': 29.99,
            'pub_date': '2023-08-13',
            'quantity': 10
        }
        serializer = BookSerializer(data=book_data)
        self.assertTrue(serializer.is_valid())
        data = serializer.save()
        self.assertTrue(data.title, 'Test Book')
        self.assertTrue(data.author.name, 'Test Author')
        self.assertTrue(data.price, 29.99)
        self.assertTrue(data.pub_date, '2023-08-13')

    def test_user_profile_serializer(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        
        user_profile_data = {
                'user':user.id,
                'shipping_address': 'Tashkent'
            }
        serializer = UserProfileSerializer(data=user_profile_data)
        if not serializer.is_valid():
            print(serializer.errors)
        self.assertTrue(serializer.is_valid())
        data = serializer.save()
        self.assertEqual(data.shipping_address, 'Tashkent')

    # def test_cart_item_serializer(self):
    

    # def test_order_serializer(self):
        