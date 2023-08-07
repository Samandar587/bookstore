from books.serializers.crud_serializers import AuthorSerializer, BookSerializer, UserProfileSerializer
from rest_framework import viewsets, status, filters
from books.models import Author, Book
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q

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


