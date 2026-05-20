from django.db import models
from django.contrib.auth.models import User


class Cat(models.Model):
    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16)
    birth_year = models.IntegerField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cats', null=True, blank=True)

    def __str__(self):
        return self.name


class Contest(models.Model):
    """Модель фото-конкурса"""
    title = models.CharField(max_length=200, verbose_name='Название конкурса')
    description = models.TextField(verbose_name='Описание')
    start_date = models.DateTimeField(verbose_name='Дата начала')
    end_date = models.DateTimeField(verbose_name='Дата окончания')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Конкурс'
        verbose_name_plural = 'Конкурсы'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Entry(models.Model):
    """Модель заявки на участие в конкурсе"""
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='entries', verbose_name='Конкурс')
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='contest_entries', verbose_name='Кот')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contest_entries', verbose_name='Пользователь')
    photo = models.ImageField(upload_to='contest_photos/', verbose_name='Фото', blank=True, null=True)
    description = models.TextField(blank=True, verbose_name='Описание заявки')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']
        unique_together = ['contest', 'cat']

    def __str__(self):
        return f'{self.cat.name} - {self.contest.title}'

    @property
    def votes_count(self):
        """Количество голосов за эту заявку"""
        return self.votes.count()


class Vote(models.Model):
    """Модель голоса за заявку"""
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='votes', verbose_name='Заявка')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'
        unique_together = ['entry', 'user']

    def __str__(self):
        return f'{self.user.username} -> {self.entry}'