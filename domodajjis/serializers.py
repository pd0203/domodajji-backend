from domodajjis.models import Gathering, UserGathering
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer

class UserGatheringCreateSerializer(ModelSerializer):
    class Meta:
        model = UserGathering
        fields = ['role', 'user', 'gathering']

class GatheringCreateSerializer(ModelSerializer):
    class Meta:
        model = Gathering
        fields = ['name', 'host']
    def create(self, validated_data):
        gathering = Gathering.objects.create(**validated_data)
        user_gathering_data = {
            'role': '방장',
            'user': gathering.host_id,
            'gathering': gathering.id
        }
        user_gathering = UserGatheringCreateSerializer(data=user_gathering_data)
        user_gathering.is_valid(raise_exception=True)
        user_gathering.save()
        return gathering
class GatheringListSerializer(ModelSerializer):
    host = serializers.SerializerMethodField()
    class Meta:
        model = Gathering
        fields = ['id', 'name', 'member_count', 'host', 'created_at']
    def get_host(self, obj):
        return obj.host.name
