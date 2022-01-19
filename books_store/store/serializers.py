from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Book, UserBookRelation, CommentBook


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class BookSerializer(serializers.ModelSerializer):

    # альтернатива анотации
    # в сериализаторе создаем дополнительное поле для вывода лайков для конкретной книги
    # likes_count = serializers.SerializerMethodField()
    # метод который получает кол-во лайков для книги (обрати внимание на название поля и метода)

    # def get_likes_count(self, instance):
    #     return UserBookRelation.objects.filter(book=instance, like=True).count()

    # получаем кол-во лайков с помощю анотации (реализация самой анотации во view)
    likes_count = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(
        max_digits=3, decimal_places=2, read_only=True)

    # что бы вывести дополнительные поля об user исползуется сериализатор UserSerializer
    # owner = UserSerializer(read_only=True) 

    class Meta:
        model = Book
        fields = ['id', 'name', 'price', 'author_name',
                  'owner', 'likes_count', 'rating']


class UserBookRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserBookRelation
        fields = ['book', 'like', 'in_bookmarks', 'rate']


class CommentBooksSerializer(serializers.ModelSerializer):
    # в сериализаторе поле owner делаем только для чтения, при записи чере сериализатор оно не будет использоваться
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = CommentBook
        fields = '__all__'
