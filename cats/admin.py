from django.contrib import admin

from .models import (Achievement, AchievementCat, Cat, Contest, ContestEntry,
                     Vote)


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


class ContestEntryInline(admin.TabularInline):
    model = ContestEntry
    extra = 1


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active', 'owner')
    list_filter = ('is_active', 'owner')
    search_fields = ('title',)
    inlines = [ContestEntryInline]


@admin.register(ContestEntry)
class ContestEntryAdmin(admin.ModelAdmin):
    list_display = ('contest', 'cat', 'created_at')
    list_filter = ('contest',)
    search_fields = ('cat__name', 'contest__title')
    ordering = ('-created_at',)
