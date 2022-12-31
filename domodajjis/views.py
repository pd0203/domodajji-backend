from domodajjis.models import Gathering, UserGathering
from domodajjis.serializers import GatheringCreateSerializer, GatheringRetrieveSerializer, GatheringListSerializer
from utils.user_validation import user_validator
from rest_framework import status 
from rest_framework.response import Response 
from rest_framework.viewsets import ModelViewSet
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.http import Http404

class GatheringAPI(ModelViewSet):
    def get_queryset(self):
        if self.action == 'list':
           user_id = self.request.user_id
           return Gathering.objects.filter(participant=user_id).prefetch_related('host')
        return Gathering.objects.all()
    def get_serializer_class(self):
        if self.action == 'create':
           return GatheringCreateSerializer 
        if self.action == 'retrieve':
           return GatheringRetrieveSerializer
        if self.action == 'list':
           return GatheringListSerializer 
    def get_object(self):
        queryset = self.get_queryset()
        if self.action == 'retrieve':
           user_id = self.request.user_id
           return get_object_or_404(queryset, id=self.kwargs.get('id'), participant=user_id)
    @transaction.atomic
    @user_validator
    def create(self, request, *args, **kwargs):
        try:
            gathering_json_data = {
              'name': request.data['name'],
              'host': self.request.user_id
            }
            new_gathering = self.get_serializer(data=gathering_json_data)
            new_gathering.is_valid(raise_exception=True)
            self.perform_create(new_gathering)
            return Response({"SUCESSFULLY_CREATED"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'ERROR_MESSAGE': e.args}, status=status.HTTP_400_BAD_REQUEST)
    @transaction.atomic
    @user_validator 
    def list(self, request, *args, **kwargs):
        try:
            # Gathering DB Table에 있는 모든 레코드 조회 
            gathering_queryset = self.get_queryset()
            # DB Table의 모든 레코드들을 serializer를 통해 정제하고 Json화 해서 변수에 저장 
            serializer = self.get_serializer(gathering_queryset, many=True)
            gathering_list = serializer.data 
            # 결과값 반환 
            return Response(gathering_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'ERROR_MESSAGE': e.args}, status=status.HTTP_400_BAD_REQUEST)
    @transaction.atomic
    @user_validator 
    def retrieve(self, request, *args, **kwargs):
        try:
           gathering = self.get_object() 
           gathering_instance= self.get_serializer(gathering)
           return Response(gathering_instance.data)
        except Http404 as n:
            return Response({'ERROR_MESSAGE': n.args}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
           return Response({'ERROR_MESSAGE': e.args}, status=status.HTTP_400_BAD_REQUEST)
        