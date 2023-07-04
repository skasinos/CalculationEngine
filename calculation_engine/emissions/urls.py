from django.urls import path
from .views import EmissionListView


app_name = 'emissions'

urlpatterns = [
    path('emissions/', EmissionListView.as_view(), name='emission-factor-list'),
    path('emissions/<int:pk>/', EmissionListView.as_view(), name='emission-detail'),
    path('calculate-emissions/', EmissionListView.as_view(), name='calculate-emissions'),
]