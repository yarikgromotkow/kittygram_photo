from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count

from .models import Cat, Contest, Entry, Vote
from .serializers import (
    CatSerializer, ContestSerializer, EntrySerializer,
    EntryDetailSerializer, VoteSerializer
)


@api_view(['GET', 'POST'])
def cat_list(request):
    if request.method == 'POST':
        serializer = CatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    cats = Cat.objects.all()
    serializer = CatSerializer(cats, many=True)
    return Response(serializer.data)


class ContestViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с конкурсами"""
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def entries(self, request, pk=None):
        """Получить все заявки конкретного конкурса"""
        contest = self.get_object()
        entries = contest.entries.all()
        serializer = EntrySerializer(entries, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def leaderboard(self, request, pk=None):
        """Таблица лидеров конкурса"""
        contest = self.get_object()
        entries = contest.entries.annotate(vote_count=Count('votes')).order_by('-vote_count')

        leaderboard = []
        for entry in entries:
            leaderboard.append({
                'id': entry.id,
                'cat_name': entry.cat.name,
                'user': entry.user.username if entry.user else 'Anonymous',
                'votes_count': entry.vote_count,
                'photo': entry.photo.url if entry.photo else None
            })

        return Response(leaderboard)


class EntryViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с заявками"""
    queryset = Entry.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EntryDetailSerializer
        return EntrySerializer

    def get_queryset(self):
        queryset = Entry.objects.all()
        contest_id = self.request.query_params.get('contest', None)
        if contest_id:
            queryset = queryset.filter(contest_id=contest_id)
        return queryset

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        """Проголосовать за заявку"""
        entry = self.get_object()
        user = request.user

        if Vote.objects.filter(entry=entry, user=user).exists():
            return Response(
                {'detail': 'Вы уже голосовали за эту заявку'},
                status=status.HTTP_400_BAD_REQUEST
            )

        vote = Vote.objects.create(entry=entry, user=user)
        serializer = VoteSerializer(vote, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def unvote(self, request, pk=None):
        """Отменить голос за заявку"""
        entry = self.get_object()
        user = request.user

        try:
            vote = Vote.objects.get(entry=entry, user=user)
            vote.delete()
            return Response(
                {'detail': 'Голос отменен'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Vote.DoesNotExist:
            return Response(
                {'detail': 'Вы не голосовали за эту заявку'},
                status=status.HTTP_400_BAD_REQUEST
            )


class VoteViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра голосов"""
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]