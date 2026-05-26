from django.contrib import admin

from .models import Achievement, AchievementCat, Cat, Vote


class AchievementCatInline(admin.TabularInline):
    model = AchievementCat
    extra = 1


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'birth_year', 'owner')
    list_filter = ('color', 'owner')
    search_fields = ('name',)
    inlines = [AchievementCatInline]


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'cat', 'created_at')
    list_filter = ('cat', 'user')
    search_fields = ('user__username', 'cat__name')
    ordering = ('-created_at',)
