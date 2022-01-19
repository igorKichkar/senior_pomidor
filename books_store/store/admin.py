from django.contrib import admin
from .models import Book, UserBookRelation, CommentBook


admin.site.register(Book)
admin.site.register(UserBookRelation)
admin.site.register(CommentBook)

