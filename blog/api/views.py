from django.contrib.auth import models
from django.db.models import fields
from django.shortcuts import get_object_or_404
from filter_map.backends import FilterMapBackend
from rest_framework import (generics, mixins, permissions, serializers, status,
                            viewsets)
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.api.permissions import IsOwner

from ..models import Category, Task
from .filters import BlogCustomFilter
from .pagination import BlogCustomPagination
from .serializers import CategorySerializer, TaskSerializers


class TaskAPIView(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    generics.ListCreateAPIView,
):
    serializer_class = TaskSerializers
    queryset = Task.objects.all()
    pagination_class = BlogCustomPagination
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (BlogCustomFilter, FilterMapBackend)
    filter_map = {
        "name": "name",
        "username": "user__username",
        "category": "category__name",
    }

    def get_object(self):
        request = self.request
        passed_id = request.GET.get("id", None)

        obj = None

        if passed_id is not None:
            obj = generics.get_object_or_404(self.queryset, id=passed_id)
            self.check_object_permissions(request, obj)

        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TaskAPIDetailView(mixins.CreateModelMixin, generics.RetrieveAPIView):
    serializer_class = TaskSerializers
    queryset = Task.objects.all()
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TasksByCategoryView(generics.ListAPIView):
    serializer_class = TaskSerializers
    lookup_field = "category_slug"

    def get_queryset(self):
        url_slug = self.kwargs.get("category_slug")
        category_obj = Category.objects.get(slug=url_slug)
        qs = Task.objects.filter(category__in=[category_obj])
        return qs


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers
    lookup_field = "pk"


class CategoryAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
