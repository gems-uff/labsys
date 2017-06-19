from rest_framework import serializers

from .models import CollectionMethod

class  CollectionMethodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CollectionMethod
        fields = '__all__'
