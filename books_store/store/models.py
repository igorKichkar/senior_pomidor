from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author_name = models.CharField(max_length=250)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_books')
    readers = models.ManyToManyField(User, through='UserBookRelation', related_name='books')

    def __str__(self) -> str:
        return f'Name: {self.name} Price: {self.price}'


class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)


class CommentBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_mycomments')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='my_mycomment_books')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)