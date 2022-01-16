from dataclasses import fields
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import Book, UserBookRelation


class BookSerializer(ModelSerializer):
    # owner = ReadOnlyField(source='owner.id') можно определить поле, которое сериалайзер будет показывать
    class Meta:
        model = Book
        fields = '__all__'

class UserBookRelationSerializer(ModelSerializer):

    class Meta:
        model = UserBookRelation
        fields = ['book', 'like', 'in_bookmarks', 'rate']

      