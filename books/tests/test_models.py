from django.test import TestCase
from books.models import Author, Book, User, UserProfile, CartItem, Order
import datetime

class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        
        self.author = Author.objects.create(
            name='Test Author',
            bio = 'Test Bio'
        )

        self.book = Book.objects.create(
            title = 'Test Title',
            author = self.author,
            description = 'Test Description',
            category = 'Test category',
            price = 29.99,
            pub_date = datetime.date.today(),
            quantity = 10
        )

        self.user_profile = UserProfile.objects.create(
            user = self.user,
            shipping_address = 'Test shipping address'
        )

        self.cart_item = CartItem.objects.create(
            user = self.user,
            book = self.book,
            quantity = 2
        )

        self.order = Order.objects.create(
            user = self.user,
            total_price = 59.98
        )
        self.order.items.add(self.cart_item)

    def test_user_str(self):
        self.assertEqual(str(self.user.username), 'testuser')

    def test_author_str(self):
        self.assertEqual(str(self.author.name), 'Test Author')
    
    def test_book_str(self):
        self.assertEqual(str(self.book.category), 'Test category')

    def test_user_profile_str(self):
        self.assertEqual(str(self.user_profile.shipping_address), 'Test shipping address')
    
    def test_cart_item_unique_together(self):
        duplicate_cart_item = CartItem(
            user=self.user,
            book=self.book,
            quantity=3
        )
        with self.assertRaises(Exception):
            duplicate_cart_item.save()

    def test_order_str(self):
        self.assertEqual(str(self.order.total_price), str(59.98))

    def test_order_total_price_calculation(self):
        result = self.cart_item.quantity * self.book.price
        self.assertEqual(self.order.total_price, result)

    def test_order_items_count(self):
        self.assertEqual(self.order.items.count(), 1)

    def test_order_status(self):
        self.assertEqual(self.order.status, 'Pending')