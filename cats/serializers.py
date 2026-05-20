from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Cat, Contest, Entry, Vote


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ContestSerializer(serializers.ModelSerializer):
    entries_count = serializers.SerializerMethodField()

    class Meta:
        model = Contest
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'is_active', 'created_at', 'entries_count']
        read_only_fields = ['created_at']

    def get_entries_count(self, obj):
        return obj.entries.count()


class VoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Vote
        fields = ['id', 'entry', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']


class EntrySerializer(serializers.ModelSerializer):
    cat = CatSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    votes_count = serializers.ReadOnlyField()
    cat_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Entry
        fields = ['id', 'contest', 'cat', 'cat_id', 'user', 'photo', 'description', 'created_at', 'votes_count']
        read_only_fields = ['user', 'created_at', 'votes_count']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class EntryDetailSerializer(EntrySerializer):
    """Детальная информация о заявке с голосами"""
    votes = VoteSerializer(many=True, read_only=True)

    class Meta(EntrySerializer.Meta):
        fields = EntrySerializer.Meta.fields + ['votes']