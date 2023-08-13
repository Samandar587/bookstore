from .models import Book

def is_book_available(book_id, quantity):
    try:
        book = Book.objects.get(pk=book_id)
        return book.quantity >= quantity
    except Book.DoesNotExist:
        return False