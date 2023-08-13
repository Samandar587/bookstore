from books.serializers.crud_serializers import AuthorSerializer, BookSerializer, CartItemSerializer, OrderSerializer
from rest_framework import viewsets, status, filters
from books.models import Author, Book, CartItem, Order
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
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

        if not is_book_available(book_id, quantity):
            
            return Response({'detail':'Book is not available in the requested quantity.'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item, created = CartItem.objects.get_or_create(user=request.user, book_id=book_id)
            
        cart_item.quantity += quantity
        cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)
        
    
    @action(detail=True, methods=['POST'])
    def remove_from_cart(self, request, pk=None):
        try:
            cart_item = CartItem.objects.get(pk=pk, user=request.user)
            cart_item.delete()
            return Response(status=204)
        except CartItem.DoesNotExist:
            return Response({'detail':'Cart Item is not found.'}, status=404)
<<<<<<< HEAD
        
    @action(detail=False, methods=['GET'])
    def get_cart(self, request):
        cart_item = CartItem.objects.all()
        serializer = self.get_serializer(cart_item, many=True)
        return Response(serializer.data)
        

@api_view(['POST'])
def checkout(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
=======
>>>>>>> parent of 6b3e502 (small changes in shopping cart)

        total_price = sum(item.book.price * item.quantity for item in cart_items)

        order= Order.objects.create(user=request.user, total_price=total_price)
        new_cart_items = cart_items
        order.items.set(new_cart_items)

        order_items = list(cart_items)

        serializer = OrderSerializer(order)
        response_data = serializer.data

        cart_items.delete()

        cart_serializer = CartItemSerializer(order_items, many=True)
        response_data['items'] = cart_serializer.data
        
        return Response(response_data, status=status.HTTP_201_CREATED)