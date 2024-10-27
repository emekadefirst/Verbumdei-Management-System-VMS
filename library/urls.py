from django.urls import path
from .views import BookView, BookDetailView, BookCountView, LoanView, LoanDetailView, CategoryView, ShelfView, ShelfDetailView, ShelfCountView, BookSearch

urlpatterns = [
    # Book endpoints
    path('books/', BookView.as_view(), name='book-list'),
    path('books/count/', BookCountView.as_view(), name='book-count'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    # Loan endpoints
    path('loans/', LoanView.as_view(), name='loan-list'),  
    path('loans/<int:pk>/', LoanDetailView.as_view(), name='loan-detail'),  

    # Category endpoints
    path('categories/', CategoryView.as_view(), name='category-list'),  
    # Shelf endpoints
    path('shelves/', ShelfView.as_view(), name='shelf-list'),  
    path('shelves/count/', ShelfCountView.as_view(), name='shelf-count'),  
    path('shelves/<uuid:str>/', ShelfDetailView.as_view(), name='shelf-detail'),  
    
    # Book search
    path('books/search/', BookSearch.as_view(), name='book-search'),  
]
