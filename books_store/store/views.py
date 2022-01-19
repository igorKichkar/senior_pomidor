from audioop import reverse
from cgitb import lookup
from django.shortcuts import render
from django.db.models import Count, Case, When, Avg
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsOwnerOrStuffOrReadOnly
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import Book, UserBookRelation, CommentBook
from .serializers import BookSerializer, UserBookRelationSerializer, CommentBooksSerializer
from rest_framework.response import Response


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().annotate(
        likes_count=Count(Case(When(userbookrelation__like=True, then=1))),
        rating=Avg('userbookrelation__rate'))

    # Таким образом можно получить  owner и readers без пополнительных запросов в БД 
    # (что бы получить всю информацию об owner, а не только одно поле, нужно создать 
    # дополнительный серилизатор и использовать его в BookSerializer)
    #
    # queryset = Book.objects.all().annotate(
    #         likes_count=Count(Case(When(userbookrelation__like=True, then=1))),
    #         rating=Avg('userbookrelation__rate')).select_related('owner').prefetch_related('readers')

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
    queryset = CommentBook.objects.all()
    serializer_class = CommentBooksSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrStuffOrReadOnly]

    def perform_create(self, serializer):

        serializer.save(owner=self.request.user)


def auth(request):
    return render(request, 'auth.html')
