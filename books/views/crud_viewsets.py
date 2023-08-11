from books.serializers.crud_serializers import AuthorSerializer, BookSerializer, CartItemSerializer
from rest_framework import viewsets, status, filters
from books.models import Author, Book, CartItem
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from books.utils import is_book_available

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__name']

    def create(self, request, *args, **kwargs):
        author_serializer = AuthorSerializer(data=request.data.get('author'))
        if author_serializer.is_valid():
            author_instance = author_serializer.save()

            book_data = {
                **request.data,
                'author_id': author_instance.id
            }

            book_serializer = self.get_serializer(data=book_data)
            if book_serializer.is_valid():

                print('23234')
                self.perform_create(book_serializer)
                return Response(book_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(book_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:   
            return Response(author_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    
    @action(detail=False, methods=['GET'])
    def search(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        query = request.query_params.get('query')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(author__name__icontains=query)
                )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'])
    def add_to_cart(self, request):
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity', 1)

        print(f"Trying to add book {book_id} to cart for user {request.user}")

        if not is_book_available(book_id, quantity):
            print(f"Book {book_id} is not available in the requested quantity.")
            return Response({'detail':'Book is not available in the requested quantity.'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item, created = CartItem.objects.get_or_create(user=request.user, book_id=book_id)
        print(cart_item)
        print()
        if not created:
            print('not created')
            cart_item.quantity += quantity
            cart_item.save()

        serializer = self.get_serializer(cart_item)
        print(serializer.data)
        return Response(serializer.data)
        
    
    @action(detail=True, methods=['POST'])
    def remove_from_cart(self, request, pk=None):
        try:
            cart_item = CartItem.objects.get(pk=pk, user=request.user)
            cart_item_id = cart_item.id
            cart_item.delete()
            return Response({'detail':f"Item with id {cart_item_id} successfully removed"}, status=204)
        except CartItem.DoesNotExist:
            return Response({'detail':'Cart Item is not found.'}, status=404)
        


