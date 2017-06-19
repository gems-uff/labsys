from django.shortcuts import render

from rest_framework import viewsets

from .serializers import CollectionMethodSerializer
from .models import CollectionMethod


class CollectionMethodViewSet(viewsets.ModelViewSet):
    queryset = CollectionMethod.objects.all()
    serializer_class = CollectionMethodSerializer
