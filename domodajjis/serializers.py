from domodajjis.models import Gathering, UserGathering
from rest_framework.serializers import ModelSerializer, SerializerMethodField

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

class GatheringRetrieveSerializer(ModelSerializer):
    participants = SerializerMethodField()
    class Meta:
        model = Gathering
        fields = ['id', 'name', 'policy', 'host', 'participants']
    def get_participants(self, obj):
        participants = []
        user_gathering = UserGathering.objects.filter(gathering=obj.id).prefetch_related('user')
        for participant in user_gathering:
            participants.append({
                'id': participant.user_id,
                'role': participant.role,
                'name': participant.user.name,
                'profile_img_url': participant.user.profile_img_url
            })
        return participants
   
class GatheringListSerializer(ModelSerializer):
    host = SerializerMethodField()
    class Meta:
        model = Gathering
        fields = ['id', 'name', 'member_count', 'host', 'created_at']
    def get_host(self, obj):
        return obj.host.name
