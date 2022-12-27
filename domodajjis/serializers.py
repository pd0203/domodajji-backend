from domodajjis.models import Gathering
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

class GatheringListSerializer(ModelSerializer):
    host = serializers.SerializerMethodField()
    class Meta:
        model = Gathering
        fields = ['name', 'member_count', 'host', 'created_at']
    def get_host(self, obj):
        return obj.host.name
