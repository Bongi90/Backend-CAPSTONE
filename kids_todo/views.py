from datetime import date as date_cls
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse 
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import TaskTemplate, DailyTask
from .serializers import TaskTemplateSerializer, DailyTaskSerializer

def home_view(request):
    return HttpResponse("<h1>Welcome to the Backend API!</h1>")

class TaskTemplateViewSet(viewsets.ModelViewSet):
    queryset = TaskTemplate.objects.all()
    serializer_class = TaskTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]

class DailyTaskViewSet(viewsets.ModelViewSet):
    serializer_class = DailyTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        date_str = self.request.query_params.get("date")
        if date_str:
            try:
                y, m, d = map(int, date_str.split("-"))
                the_date = date_cls(y, m, d)
            except Exception:
                the_date = timezone.now().date()
        else:
            the_date = timezone.now().date()
        return DailyTask.objects.filter(owner=self.request.user, date=the_date)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=["post"])
    def generate_for_today(self, request):
        today = timezone.now().date()
        created = 0
        for idx, tpl in enumerate(TaskTemplate.objects.filter(is_active=True).order_by("category", "order")):
            obj, was_created = DailyTask.objects.get_or_create(
                owner=request.user,
                date=today,
                title=tpl.title,
                category=tpl.category,
            )
            if was_created:
                created += 1
        return Response({"created": created, "date": str(today)})

    @action(detail=True, methods=["post"])
    def toggle(self, request, pk=None):
        task = self.get_object()
        task.is_completed = not task.is_completed
        task.completed_at = timezone.now() if task.is_completed else None
        task.save()
        return Response(self.get_serializer(task).data)
