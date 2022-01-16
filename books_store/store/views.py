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

from .models import Book, UserBookRelation
from .serializers import BookSerializer, UserBookRelationSerializer


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
    lookup_field = 'book' # в запросе через book передается id книги 

    def get_object(self):   # по книге и пользователю получаем
                            # объект UserBookRelation если он существует, иначе создается
        obj, _ = UserBookRelation.objects.get_or_create(
            user=self.request.user, book_id=self.kwargs['book'])
        return obj


def auth(request):
    return render(request, 'auth.html')
