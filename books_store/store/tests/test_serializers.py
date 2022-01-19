from django.http import request
from django.test import TestCase
from django.contrib.auth.models import User
from store.serializers import BookSerializer
from store.models import Book, UserBookRelation
from django.db.models import Count, Case, When, Avg

class BookSerializerTestCase(TestCase):
    def test_ok(self):
        user = User.objects.create(username='test_user')
        user2 = User.objects.create(username='test_user2')
        user3 = User.objects.create(username='test_user3')
        # relate =UserBookRelation.objects.create(user=user, )
        book_1 = Book.objects.create(name='Test book_1', price=150, author_name='Author', owner=user)
        book_2 = Book.objects.create(name='Test book_2', price=250, author_name='Author', owner=user)
       
        UserBookRelation.objects.create(user=user, book=book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=book_1, like=True, rate=4)
        UserBookRelation.objects.create(user=user3, book=book_1, like=False)

        UserBookRelation.objects.create(user=user, book=book_2, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=book_2, like=True, rate=4)
        UserBookRelation.objects.create(user=user3, book=book_2, like=True)

        books = Book.objects.all().annotate(
            likes_count=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
            ).order_by('id')
            
        
        data = BookSerializer(books, many=True).data  
        expected_data = [
            {
                'id' : book_1.id,
                'name' : 'Test book_1',
                'price' : '150.00',
                'author_name' : 'Author',
                'owner' : user.id,
                'likes_count': 2,
                'rating': '4.50'
            },
             {
                'id' : book_2.id,
                'name' : 'Test book_2',
                'price' : '250.00',
                'author_name' : 'Author',
                'owner' : user.id,
                'likes_count': 3,
                'rating': '4.50'
            }
        ]
        self.assertEqual(expected_data, data)