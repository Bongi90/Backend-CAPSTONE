from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from .models import Task
from .serializers import TaskSerializer, UserCreateSerializer, UserMeSerializer
from .permissions import IsOwner

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "priority", "due_date"]
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "priority", "created_at"]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.status = "COMPLETED"
        task.completed_at = timezone.now()
        task.save()
        return Response(self.get_serializer(task).data)

    @action(detail=True, methods=["post"])
    def incomplete(self, request, pk=None):
        task = self.get_object()
        task.status = "PENDING"
        task.completed_at = None
        task.save()
        return Response(self.get_serializer(task).data)

# User endpoints
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from django.contrib.auth.models import User

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

class MeView(RetrieveUpdateAPIView):
    serializer_class = UserMeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
