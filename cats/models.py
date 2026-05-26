"""
Models for Kittygram Cats - Cat travel management system
Last updated: 2026-05-05
"""
from django.contrib.auth import get_user_model
from django.db import models

CHOICES = (
    ('Gray', 'Серый'),
    ('Black', 'Чёрный'),
    ('White', 'Белый'),
    ('Ginger', 'Рыжий'),
    ('Mixed', 'Смешанный'),
)

User = get_user_model()


class Achievement(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Cat(models.Model):
    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16, choices=CHOICES)
    birth_year = models.IntegerField()
    owner = models.ForeignKey(
        User, related_name='cats', on_delete=models.CASCADE)
    achievements = models.ManyToManyField(Achievement, through='AchievementCat')

    class Meta:
        unique_together = ('name', 'owner')

    def __str__(self):
        return self.name


class AchievementCat(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.achievement} {self.cat}'


class Vote(models.Model):
    """Голос пользователя за кошку в фотоконкурсе."""
    user = models.ForeignKey(
        User, related_name='votes', on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    cat = models.ForeignKey(
        Cat, related_name='votes', on_delete=models.CASCADE,
        verbose_name='Кошка'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата голосования')

    class Meta:
        unique_together = ('user', 'cat')
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'

    def __str__(self):
        return f'{self.user} → {self.cat}'
