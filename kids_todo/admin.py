from django.contrib import admin
from .models import TaskTemplate, DailyTask

@admin.register(TaskTemplate)
class TaskTemplateAdmin(admin.ModelAdmin):
    list_display = ("id","title","category","order","is_active")
    list_filter = ("category","is_active")
    ordering = ("category","order")

@admin.register(DailyTask)
class DailyTaskAdmin(admin.ModelAdmin):
    list_display = ("id","title","owner","date","category","is_completed","completed_at")
    list_filter = ("category","is_completed","date")
    search_fields = ("title","owner__username")
