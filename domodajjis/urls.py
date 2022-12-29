from django.urls import path
from domodajjis.views import GatheringAPI

urlpatterns = [
    path('gathering', GatheringAPI.as_view({'post': 'create'}), name='gathering_create'),
    path('gathering/list', GatheringAPI.as_view({'get': 'list'}), name='gathering_list'),
]