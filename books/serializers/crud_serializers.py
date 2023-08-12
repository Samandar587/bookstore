from books.models import Author, Book, UserProfile, CartItem, Order
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    def create(self, validated_data):
        author_data = validated_data.pop('author')

        author_instance, _ = Author.objects.get_or_create(**author_data)
        
        book = Book.objects.create(author=author_instance, **validated_data)
        return book


    class Meta:
        model = Book
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    class Meta:
        model = CartItem
        fields = ['id', 'book', 'quantity', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['items', 'status', 'total_price', 'created_at']