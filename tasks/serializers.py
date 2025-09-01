from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Task

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["owner", "completed_at", "created_at", "updated_at"]

    def validate_due_date(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Due date must be today or in the future.")
        return value

    def validate(self, attrs):
        instance = getattr(self, "instance", None)
        if instance and instance.status == "COMPLETED":
            if attrs.get("status") not in (None, "PENDING"):
                raise serializers.ValidationError("Completed tasks cannot be edited unless reverted to incomplete.")
        return attrs
