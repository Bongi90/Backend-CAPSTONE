from rest_framework import serializers
from .models import TaskTemplate, DailyTask

class TaskTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTemplate
        fields = "__all__"

class DailyTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTask
        fields = "__all__"
        read_only_fields = ["owner", "completed_at", "created_at"]
