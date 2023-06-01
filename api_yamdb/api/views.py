import os

from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import filters
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status, mixins, viewsets, generics, permissions
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import ValidationError


from reviews.models import Category, Genre, Title, Review, Comment
from api.serializers import (CategorySerializer,
                             GenreSerializer,
                             TitleSerializer,
                             UserSerializer,
                             UserMeSerializer,
                             UserSignUpSerializer,
                             ReviewSerializer,
                             CommentSerializer,
                             TitleWriteSerializer,)
from api.permissions import (IsAdminOrSuperuser,
                             IsAdminOrReadOnly,
                             PermissionReviewComment)
from api.pagination import UsersPagination
from api.filters import TitleFilter
from dotenv import load_dotenv


load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')

User = get_user_model()

token_generator = PasswordResetTokenGenerator()


def send_token_by_email(user):
    token = token_generator.make_token(user)
    send_mail(
        'Token for yamdb API.',
        f'{user.username} {user.email}'
        f'Here is your token: '
        f'{token}',
        EMAIL_ADDRESS,
        [user.email, ],
        fail_silently=False,
    )


@api_view(['POST'])
def sign_up(request):
    serializer = UserSignUpSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        user = serializer.save()
        send_token_by_email(user)
        return Response({
            "email": user.email,
            "username": user.username
        }, status=status.HTTP_200_OK)
    else:
        try:
            username = request.data['username']
            email = request.data['email']
        except KeyError:
            return Response({
                'username': ["This field is required."],
                "email": ["This field is required."]
            }, status=status.HTTP_400_BAD_REQUEST)
        user_queryset = User.objects.filter(
            username__iexact=username,
            email__iexact=email
        )
        if user_queryset.exists():
            user = user_queryset[0]
            send_token_by_email(user)
            return Response({
                "email": user.email,
                "username": user.username
            }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    try:
        username = request.data['username']
        token = request.data['confirmation_code']
    except KeyError:
        return Response('Request do not match requirements',
                        status=status.HTTP_400_BAD_REQUEST)
    user_queryset = User.objects.filter(username__iexact=username)
    if user_queryset.exists():
        user = user_queryset[0]
        if token_generator.check_token(user, token):
            jwt_token = str(AccessToken.for_user(user))
            return Response({'token': jwt_token}, status=status.HTTP_200_OK)
        else:
            return Response('Invalid token',
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Invalid user', status=status.HTTP_404_NOT_FOUND)


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = UsersPagination
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = UsersPagination
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = UsersPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitleWriteSerializer


class UserMeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserMeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return User.objects.get(username=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete', ]
    permission_classes = (IsAdminOrSuperuser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', )
    pagination_class = UsersPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [PermissionReviewComment]
    pagination_class = UsersPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        queryset = Review.objects.filter(
            title=title_id,
            author=self.request.user)
        if queryset.exists():
            raise ValidationError(
                'Нельзя два раза писать отзыв на одно произведение!'
            )
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [PermissionReviewComment]
    pagination_class = UsersPagination

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        new_queryset = Comment.objects.filter(review=review_id)
        return new_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
