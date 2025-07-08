from django.contrib import admin
from .models import (
    Profile, Researcher, Reference, Project, Event, Post, 
    Talk, Organizer, Speaker
)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'institution', 'is_public', 'created_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'institution']

@admin.register(Researcher)
class ResearcherAdmin(admin.ModelAdmin):
    list_display = ['name', 'institution', 'email', 'is_active', 'created_at']
    list_filter = ['is_active', 'institution', 'created_at']
    search_fields = ['name', 'email', 'institution', 'research_areas']
    ordering = ['name']

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ['title', 'authors', 'year', 'reference_type', 'added_by']
    list_filter = ['reference_type', 'year', 'added_by']
    search_fields = ['title', 'authors', 'keywords', 'abstract']
    ordering = ['-year', 'title']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'lead_researcher', 'status', 'start_date', 'is_public']
    list_filter = ['status', 'is_public', 'start_date']
    search_fields = ['name', 'description', 'lead_researcher__name']
    filter_horizontal = ['collaborators']
    ordering = ['-start_date']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'location', 'is_featured']
    list_filter = ['is_featured', 'start_date', 'location']
    search_fields = ['title', 'description', 'location']
    filter_horizontal = ['organizers', 'speakers']
    ordering = ['-start_date']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'published_at', 'created_at']
    list_filter = ['is_published', 'published_at', 'author']
    search_fields = ['title', 'content', 'tags']
    filter_horizontal = ['related_projects']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-published_at']

@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    list_display = ['title', 'speaker', 'event', 'start_time', 'end_time']
    list_filter = ['event', 'start_time', 'speaker']
    search_fields = ['title', 'abstract', 'speaker__name']
    ordering = ['start_time']

@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'institution', 'role']
    list_filter = ['event', 'institution']
    search_fields = ['name', 'email', 'institution']

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'institution']
    list_filter = ['event', 'institution']
    search_fields = ['name', 'bio', 'institution']
