from django.test import TestCase
from django.contrib.auth.models import User
from store.serializers import BookSerializer
from store.models import Book, UserBookRelation

class BookSerializerTestCase(TestCase):
    def test_ok(self):
        user = User.objects.create(username='test_user')
        # relate =UserBookRelation.objects.create(user=user, )
        book_1 = Book.objects.create(name='Test book_1', price=150, author_name='Author', owner=user)
        book_2 = Book.objects.create(name='Test book_2', price=250, author_name='Author', owner=user)
        book_3 = Book.objects.create(name='Test book_3', price=50, author_name='Author', owner=user)
        data = BookSerializer([book_1, book_2, book_3], many=True).data  
        expected_data = [
            {
                'id' : book_1.id,
                'name' : 'Test book_1',
                'price' : '150.00',
                'author_name' : 'Author',
                'owner' : user.id,
                'readers' : [],
            },
             {
                'id' : book_2.id,
                'name' : 'Test book_2',
                'price' : '250.00',
                'author_name' : 'Author',
                'owner' : user.id,
                'readers' : [],
            },
             {
                'id' : book_3.id,
                'name' : 'Test book_3',
                'price' : '50.00',
                'author_name' : 'Author',
                'owner' : user.id,
                'readers' : [],
            }
        ]
        self.assertEqual(expected_data, data)