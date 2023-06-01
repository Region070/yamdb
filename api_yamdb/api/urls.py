from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import sign_up, get_token
from api.views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UserMeAPIView,
    ReviewViewSet,
    UserViewSet,
    CommentViewSet
)

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register(r'^titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='reviews')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', sign_up),
    path('v1/auth/token/', get_token),
    path('v1/users/me/', UserMeAPIView.as_view(), name='user-me'),
    path('v1/', include(router.urls)),
]
