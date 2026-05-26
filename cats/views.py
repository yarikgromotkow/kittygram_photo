"""
API ViewSets for Kittygram Cats
Last updated: 2026-05-26
"""
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Achievement, Cat, User, Vote
from .permissions import IsOwnerOrReadOnly
from .serializers import (AchievementSerializer, CatRatingSerializer,
                          CatSerializer, UserSerializer, VoteSerializer)


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['color', 'owner']
    search_fields = ['name']
    ordering_fields = ['name', 'birth_year']
    ordering = ['name']
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated],
            url_path='vote')
    def vote(self, request, pk=None):
        """Проголосовать за кошку. Один голос на пользователя."""
        cat = self.get_object()
        serializer = VoteSerializer(
            data={'cat': cat.pk},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(
            {'detail': f'Вы успешно проголосовали за кошку «{cat.name}»!'},
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticatedOrReadOnly],
            url_path='rating')
    def rating(self, request):
        """Рейтинг кошек по количеству голосов (по убыванию)."""
        queryset = (
            Cat.objects.annotate(vote_count=Count('votes'))
            .order_by('-vote_count', 'name')
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CatRatingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CatRatingSerializer(queryset, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    pagination_class = PageNumberPagination
