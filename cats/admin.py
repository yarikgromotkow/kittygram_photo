from django.contrib import admin
from .models import Cat, Contest, Entry, Vote


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'birth_year', 'owner']
    list_filter = ['color']
    search_fields = ['name']


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'is_active', 'created_at']
    list_filter = ['is_active', 'start_date']
    search_fields = ['title', 'description']


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['cat', 'contest', 'user', 'created_at', 'votes_count']
    list_filter = ['contest', 'created_at']
    search_fields = ['cat__name', 'user__username']

    def votes_count(self, obj):
        return obj.votes_count
    votes_count.short_description = 'Голосов'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['entry', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'entry__cat__name']
