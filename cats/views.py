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
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .models import Achievement, Cat, Contest, ContestEntry, User, Vote
from .permissions import IsOwnerOrReadOnly
from .serializers import (AchievementSerializer, CatRatingSerializer,
                          CatSerializer, ContestEntryCreateSerializer,
                          ContestEntrySerializer, ContestResultSerializer,
                          ContestSerializer, UserSerializer, VoteSerializer)


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


class ContestViewSet(viewsets.ModelViewSet):
    """CRUD по фотоконкурсам + действия: подать заявку, выйти, результаты."""
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'owner']
    search_fields = ['title']
    ordering_fields = ['start_date', 'end_date', 'created_at']
    ordering = ['-start_date']
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated], url_path='enter')
    def enter(self, request, pk=None):
        """Подать заявку: своя кошка участвует в конкурсе."""
        contest = self.get_object()
        serializer = ContestEntryCreateSerializer(
            data=request.data,
            context={'request': request, 'contest': contest}
        )
        serializer.is_valid(raise_exception=True)
        entry = serializer.save(contest=contest)
        return Response(
            {'detail': f'Кошка «{entry.cat.name}» подана на конкурс '
                       f'«{contest.title}».',
             'entry': ContestEntrySerializer(entry).data},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated], url_path='leave')
    def leave(self, request, pk=None):
        """Снять свою кошку с конкурса."""
        contest = self.get_object()
        entry = ContestEntry.objects.filter(
            contest=contest, cat_id=request.data.get('cat'),
            cat__owner=request.user
        ).first()
        if entry is None:
            return Response(
                {'detail': 'Заявка не найдена или принадлежит другому '
                           'пользователю.'},
                status=status.HTTP_404_NOT_FOUND
            )
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'],
            permission_classes=[AllowAny], url_path='entries')
    def entries(self, request, pk=None):
        """Список участников конкурса."""
        contest = self.get_object()
        queryset = (contest.entries
                    .select_related('cat', 'cat__owner')
                    .order_by('-created_at'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ContestEntrySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ContestEntrySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'],
            permission_classes=[AllowAny], url_path='results')
    def results(self, request, pk=None):
        """Результаты конкурса: участники по убыванию числа голосов."""
        contest = self.get_object()
        queryset = (
            contest.entries
            .select_related('cat', 'cat__owner')
            .annotate(vote_count=Count('cat__votes'))
            .order_by('-vote_count', 'cat__name')
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ContestResultSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ContestResultSerializer(queryset, many=True)
        return Response(serializer.data)
