from django.urls import path
from domodajjis.views import GatheringAPI

urlpatterns = [
    path('gathering/list', GatheringAPI.as_view({'get': 'list'}), name='gathering_list'),
]