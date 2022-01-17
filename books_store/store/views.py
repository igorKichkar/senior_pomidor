from audioop import reverse
from cgitb import lookup
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsOwnerOrStuffOrReadOnly
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import Book, UserBookRelation, CommentBook
from .serializers import BookSerializer, UserBookRelationSerializer, CommentBooksSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrStuffOrReadOnly]
    filterset_fields = ['name', 'price', 'author_name']
    search_fields = ['name', 'price', 'author_name']
    ordering_fields = '__all__'

    # переопределяется метод миксина для добавленимя owner в запись
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserBooksRelationViev(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'  # в запросе через book передается id книги

    def get_object(self):   # по книге и пользователю получаем
        # объект UserBookRelation если он существует, иначе создается
        # (т.е. пользователь ставит лайк и объект создается если его нет или изменяется)
        obj, _ = UserBookRelation.objects.get_or_create(
            user=self.request.user, book_id=self.kwargs['book'])
        return obj


class CommentBooksView(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrStuffOrReadOnly]
    queryset = CommentBook.objects.all()
    serializer_class = CommentBooksSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


    # lookup_field = 'book'

    # def perform_update(self, serializer):
    #     print(self.request.method)
    #     book = Book.objects.filter(id=self.kwargs['book'])
    #     comment_book = CommentBook.objects.filter(book=book).exists()
    #     if comment_book:
    #         serializer.save()
    #     else:
    #         serializer.save(user=self.request.user, book=comment_book)

def auth(request):
    return render(request, 'auth.html')
