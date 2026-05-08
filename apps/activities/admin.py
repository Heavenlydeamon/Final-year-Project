from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
import json
from .models import ActivityQuestion

class ActivityQuestionForm(forms.ModelForm):
    class Meta:
        model = ActivityQuestion
        fields = '__all__'
        widgets = {
            'items': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
            'answer': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
        }

    def clean(self):
        cleaned_data = super().clean()
        q_type = cleaned_data.get('question_type')
        items = cleaned_data.get('items')
        answer = cleaned_data.get('answer')

        if q_type == 'drag_drop':
            if not isinstance(items, dict) or 'draggables' not in items or 'containers' not in items:
                raise forms.ValidationError("drag_drop must have 'draggables' and 'containers' in items.")
        elif q_type == 'sequence':
            if not isinstance(items, dict) or 'items' not in items:
                raise forms.ValidationError("sequence must have 'items' in items.")
        elif q_type == 'tap_match':
            if not isinstance(items, dict) or 'left_items' not in items or 'right_items' not in items:
                raise forms.ValidationError("tap_match must have 'left_items' and 'right_items' in items.")
        elif q_type == 'image_pick':
            if not isinstance(items, dict) or 'options' not in items:
                raise forms.ValidationError("image_pick must have 'options' in items.")

        return cleaned_data

@admin.register(ActivityQuestion)
class ActivityQuestionAdmin(admin.ModelAdmin):
    form = ActivityQuestionForm
    list_display = ('topic', 'question_type', 'order')
    list_filter = ('question_type', 'topic')
    readonly_fields = ('activity_preview',)
    
    fieldsets = (
        (None, {
            'fields': ('topic', 'question_type', 'question_text', 'order')
        }),
        ('Content', {
            'fields': ('items', 'answer', 'explanation'),
            'description': mark_safe("""
                <div style="background: #f8f9fa; padding: 10px; border-radius: 4px; border: 1px solid #ddd; margin-bottom: 10px;">
                    <strong>JSON Examples:</strong><br>
                    <code>drag_drop</code>: <code>{"draggables": [...], "containers": [...]}</code> | <code>answer: {"id": "target"}</code><br>
                    <code>sequence</code>: <code>{"items": [...]}</code> | <code>answer: ["id1", "id2"]</code><br>
                    <code>tap_match</code>: <code>{"left_items": [...], "right_items": [...]}</code> | <code>answer: {"l1": "r1"}</code><br>
                    <code>image_pick</code>: <code>{"options": [...]}</code> | <code>answer: "id"</code>
                </div>
            """)
        }),
        ('Preview', {
            'fields': ('activity_preview',),
        }),
    )

    def activity_preview(self, obj):
        if not obj.items:
            return "No content to preview"
        
        try:
            items = obj.items
            if obj.question_type == 'drag_drop':
                drags = ", ".join([d.get('label', d.get('id')) for d in items.get('draggables', [])])
                conts = ", ".join([c.get('label', c.get('id')) for c in items.get('containers', [])])
                return mark_safe(f"<b>Draggables:</b> {drags}<br><b>Containers:</b> {conts}")
            
            elif obj.question_type == 'sequence':
                seq = " → ".join([i.get('label', i.get('id')) for i in items.get('items', [])])
                return mark_safe(f"<b>Sequence:</b> {seq}")
            
            elif obj.question_type == 'tap_match':
                left = ", ".join([i.get('label', i.get('id')) for i in items.get('left_items', [])])
                right = ", ".join([i.get('label', i.get('id')) for i in items.get('right_items', [])])
                return mark_safe(f"<b>Match:</b> {left} <---> {right}")
            
            elif obj.question_type == 'image_pick':
                opts = ", ".join([o.get('label', o.get('id')) for o in items.get('options', [])])
                return mark_safe(f"<b>Options:</b> {opts}")
            
        except Exception as e:
            return f"Error rendering preview: {str(e)}"
        
        return "Preview not available for this type"

    activity_preview.short_description = "Visual Summary"
