from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import Topic, Story, StoryPanel

class StoryPanelInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        panels = [form.cleaned_data for form in self.forms if form.cleaned_data and not form.cleaned_data.get('DELETE')]
        
        # Validation: min 5 panels, max 15 panels per story
        if len(panels) < 5:
            raise ValidationError("A story must have at least 5 panels.")
        if len(panels) > 15:
            raise ValidationError("A story cannot have more than 15 panels.")

        # Validation: at least 1 question or activity panel required.
        has_interactive = any(p.get('panel_type') in ['question', 'activity'] for p in panels)
        if not has_interactive:
            raise ValidationError("A story must have at least one 'Question' or 'Activity Cue' panel.")

class StoryPanelInline(admin.TabularInline):
    model = StoryPanel
    formset = StoryPanelInlineFormSet
    extra = 5
    fields = ('order', 'panel_type', 'title', 'image', 'text', 'audio_file', 'linked_activity')
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'text':
            kwargs['widget'] = forms.Textarea(attrs={'rows': 2, 'cols': 40, 'maxlength': '250'})
        return super().formfield_for_dbfield(db_field, **kwargs)

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'story_type', 'status', 'created_at')
    list_filter = ('story_type', 'status', 'topic')
    search_fields = ('title', 'tagline', 'character_name')
    inlines = [StoryPanelInline]
    
    fieldsets = (
        (None, {
            'fields': ('topic', 'title', 'tagline', 'cover_image', 'story_type', 'status')
        }),
        ('Character Information', {
            'fields': ('character_name', 'character_age', 'character_avatar', 'character_description'),
            'description': 'Customize the character who leads the story.'
        }),
        ('Admin Meta', {
            'fields': ('created_by', 'approved_by'),
            'classes': ('collapse',),
        }),
    )

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'class_level', 'is_published')
    list_filter = ('category', 'class_level', 'is_published')
    search_fields = ('title', 'description')

admin.site.register(StoryPanel) # Optional, usually managed via inline but good to have if needed
