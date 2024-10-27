from django.http import Http404
from .models import *
from django.db.models import Q
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class BookView(APIView):
    def get(self, request):
        obj = Book.objects.all()
        serializer = BookListSerilizer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, formart=None):
        serializer = CreateBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookCountView(APIView):
    def get(self, request):
        obj = Book.objects.count()
        return Response({"count": obj}, status=status.HTTP_200_OK)

class BookDetailView(APIView):
    def get_by_id(self, id):
        try:
            return Book.objects.get(id=id)
        except Book.DoesNotExist:
            raise Http404("Book not found")

    def get(self, request, pk):
        book = self.get_by_id(pk)
        serializer = BookListSerilizer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
            book = self.get_by_id(pk)
            serializer = CreateBookSerializer(book, data=request.data)  
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""Loan Views"""
class LoanView(APIView):
    def get(self, request):
        obj = Loan.objects.all()
        serializer = GetLoanListSerilizer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, formart=None):
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanDetailView(APIView):
    def get_by_id(self, id):
        try:
            return Loan.objects.get(id=id)
        except Loan.DoesNotExist:
            raise Http404("Loan not found")

    def get(self, request, pk):
        loan = self.get_by_id(pk)
        serializer = GetLoanListSerilizer(loan)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        book = self.get_by_id(pk)
        serializer = LoanSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""Category"""
class CategoryView(APIView):
    def get(self, request):
        obj = BookCategory.objects.all()
        serializer = CategoryListSerilizer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, formart=None):
        serializer = BookCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""Shelf"""
class ShelfView(APIView):
    def get(self, request):
        obj = Shelf.objects.all()
        serializer = ShelfSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, formart=None):
        serializer = ShelfSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookSearch(APIView):
    def post(self, request):
        search_query = request.data.get("query", "")
        if search_query:
            search_results = Book.objects.filter(
                Q(name__icontains=search_query)
                | Q(title__icontains=search_query)
                | Q(author__icontains=search_query)
                | Q(isbn__icontains=search_query)
                | Q(category__icontains=search_query)
                | Q(shelf__icontains=search_query)
            )

            search_results = search_results.order_by("registration_id")
            serializer = BookListSerilizer(search_results, many=True)
            return Response(serializer.data)
        else:
            return Response("Invalid search query", status=status.HTTP_400_BAD_REQUEST)


class ShelfCountView(APIView):
    def get(self, request):
        obj = Shelf.objects.count()
        return Response({"count": obj}, status=status.HTTP_200_OK)


class ShelfDetailView(APIView):
    def get_by_id(self, id):
        try:
            return Shelf.objects.get(id=id)
        except Shelf.DoesNotExist:
            raise Http404("Shelf not found")

    def get(self, request, pk):
        shelf = self.get_by_id(pk)
        serializer = ShelfSerializer(shelf)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        shelf = self.get_by_id(pk)
        serializer = ShelfSerializer(shelf, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
