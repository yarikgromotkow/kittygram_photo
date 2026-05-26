"""
Serializers for Kittygram Cats with data validation
Last updated: 2026-05-05
"""
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

import datetime as dt

from .models import CHOICES, Achievement, AchievementCat, Cat, User, Vote


class UserSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'cats')
        ref_name = 'ReadOnlyUsers'


class AchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source='name')

    class Meta:
        model = Achievement
        fields = ('id', 'achievement_name')


class CatSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializer(many=True, required=False)
    color = serializers.ChoiceField(choices=CHOICES)
    age = serializers.SerializerMethodField()
    owner = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'achievements', 'owner',
                  'age')
        validators = [
            UniqueTogetherValidator(
                queryset=Cat.objects.all(),
                fields=('name', 'owner')
            )
        ]

    def get_age(self, obj):
        return dt.datetime.now().year - obj.birth_year

    def validate_birth_year(self, value):
        current_year = dt.datetime.now().year
        if not (current_year - 40 < value <= current_year):
            raise serializers.ValidationError('Проверьте год рождения!')
        return value

    def validate(self, data):
        if 'color' in data and 'name' in data:
            if data['color'] == data['name']:
                raise serializers.ValidationError('Имя не может совпадать с цветом!')
        return data

    def create(self, validated_data):
        achievements = validated_data.pop('achievements', [])
        cat = Cat.objects.create(**validated_data)
        for achievement in achievements:
            current_achievement, _ = Achievement.objects.get_or_create(**achievement)
            AchievementCat.objects.create(achievement=current_achievement, cat=cat)
        return cat

    def update(self, instance, validated_data):
        achievements = validated_data.pop('achievements', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if achievements is not None:
            instance.achievements.clear()
            for achievement in achievements:
                current_achievement, _ = Achievement.objects.get_or_create(**achievement)
                AchievementCat.objects.create(achievement=current_achievement, cat=instance)
        return instance


class VoteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания голоса за кошку."""
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Vote
        fields = ('id', 'user', 'cat', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Vote.objects.all(),
                fields=('user', 'cat'),
                message='Вы уже проголосовали за эту кошку!'
            )
        ]

    def validate_cat(self, cat):
        request = self.context['request']
        if cat.owner == request.user:
            raise serializers.ValidationError('Нельзя голосовать за собственную кошку!')
        return cat


class CatRatingSerializer(serializers.ModelSerializer):
    """Сериализатор для рейтинга кошек с количеством голосов."""
    vote_count = serializers.IntegerField(read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner', 'owner_username', 'vote_count')
