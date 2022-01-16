from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from rest_framework.routers import SimpleRouter
from store.views import auth

from store.views import BookViewSet, UserBooksRelationViev

router = SimpleRouter()
router.register(r'book', BookViewSet)
router.register(r'book_relation', UserBooksRelationViev)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'', include('social_django.urls', namespace='social')), # пути для social auth
    path('auth/', auth)
]

urlpatterns += router.urls


