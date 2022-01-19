from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Count, Case, When, Avg
from rest_framework.test import APITestCase
from rest_framework import status
from store.models import Book, UserBookRelation, CommentBook
from store.serializers import BookSerializer, CommentBooksSerializer
import json
import collections


class BookApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.book_1 = Book.objects.create(name='cook_1 Aurhor-3', price='150.00',
                                          author_name='Aurhor-1', owner=self.user)
        self.book_2 = Book.objects.create(name='aook_2', price='250.00',
                                          author_name='Aurhor-2', owner=self.user)
        self.book_3 = Book.objects.create(name='book_3', price='150.00',
                                          author_name='Aurhor-3', owner=self.user)

    def test_get(self):
        url = reverse('book-list')
        # метод client делает запрос с указанным url и возвращает отвер
        response = self.client.get(url)
        books = Book.objects.all().annotate(
            likes_count=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        )

        serializer_data = BookSerializer(
            books, many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'price': '150.00'})
        books = Book.objects.filter(id__in=[self.book_1.id, self.book_3.id]).annotate(
            likes_count=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate'))
        serializer_data = BookSerializer(
            books, many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Aurhor-3'})
        books = Book.objects.filter(id__in=[self.book_1.id, self.book_3.id]).annotate(
            likes_count=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate'))
        serializer_data = BookSerializer(
            books, many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_ordering(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': 'name'})
        expexted_books = Book.objects.all().annotate(
            likes_count=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('name')
        serializer_data = BookSerializer(expexted_books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        # производится авторизация пользователя
        self.client.force_login(self.user)
        url = reverse('book-list')
        data = {
            "name": "Programing in Python3",
            "price": 25,
            "author_name": "Mikle Sikluhin"
        }
        json_data = json.dumps(data)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())

    def test_update(self):
        # производится авторизация пользователя
        self.client.force_login(self.user)
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 45,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        response = self.client.put(
            url, data=json_data, content_type='application/json')
        self.book_1.refresh_from_db()   # обновление объекта с БД
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(45, self.book_1.price)

    def test_delete(self):
        # производится авторизация пользователя
        self.client.force_login(self.user)
        url = reverse('book-detail', args=(self.book_1.id,))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.all().count())

    def test_get_detail(self):
        # производится авторизация пользователя
        self.client.force_login(self.user)
        url = reverse('book-detail', args=(self.book_1.id,))
        book = Book.objects.filter(id=self.book_1.id).annotate(
            likes_count=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate'))
        serializer_data = BookSerializer(book[0]).data
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_access_to_data_for_stuff_user(self):
        user_2 = User.objects.create(username='test_user_2', is_staff=True)
        self.client.force_login(user_2)
        book_1 = Book.objects.create(name='cook_1 Aurhor-3', price='150.00',
                                     author_name='Aurhor-1', owner=self.user)
        url = reverse('book-detail', args=(book_1.id,))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(False, Book.objects.filter(id=book_1.id).exists())

    def test_access_to_data(self):
        user_2 = User.objects.create(username='test_user_2')
        self.client.force_login(user_2)
        url = reverse('book-detail', args=(self.book_1.id,))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(True, Book.objects.filter(id=self.book_1.id).exists())


class BookRelationTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.user_2 = User.objects.create(username='test_user_2')
        self.book_1 = Book.objects.create(name='cook_1 Aurhor-3', price='150.00',
                                          author_name='Aurhor-1', owner=self.user)
        self.book_2 = Book.objects.create(name='aook_2', price='250.00',
                                          author_name='Aurhor-2', owner=self.user)

    def test_like(self):
        self.client.force_login(self.user)
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {
            "like": True,
        }
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        relation = UserBookRelation.objects.get(
            user=self.user, book=self.book_1)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(relation.like)
        data_2 = {
            "in_bookmarks": True,
        }
        json_data_2 = json.dumps(data_2)
        response = self.client.patch(
            url, data=json_data_2, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(relation.like)

    def test_rate(self):
        self.client.force_login(self.user)
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {
            "rate": 3,
        }
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        relation = UserBookRelation.objects.get(
            user=self.user, book=self.book_1)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, response.data["rate"])


class CommentApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.book_1 = Book.objects.create(name='cook_1 Aurhor-3', price='150.00',
                                          author_name='Aurhor-1', owner=self.user)
        self.book_2 = Book.objects.create(name='aook_2', price='250.00',
                                          author_name='Aurhor-2', owner=self.user)
        self.comment_1 = CommentBook.objects.create(
            book=self.book_1, owner=self.user, content='test comment')

    def test_get(self):
        url = reverse('commentbook-list')
        # метод client делает запрос с указанным url и возвращает отвер
        response = self.client.get(url)
        serializer_data = CommentBooksSerializer(
            [self.comment_1], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_post_no_access(self):
        url = reverse('commentbook-list')
        # метод client делает запрос с указанным url и возвращает отвер
        data = {
            "book": self.book_1.id,
            "owner": self.user.id,
            "content": "test comment",
        }
        json_data = json.dumps(data)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(1, CommentBook.objects.count())
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_post(self):
        self.client.force_login(self.user)
        url = reverse('commentbook-list')
        # метод client делает запрос с указанным url и возвращает отвер
        data = {
            "book": self.book_1.id,
            "owner": self.user.id,
            "content": "test comment",
        }
        json_data = json.dumps(data)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(2, CommentBook.objects.count())
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
