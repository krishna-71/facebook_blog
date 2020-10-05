from django.urls import path
from .views import *

urlpatterns = [
    path('post_details/', PostAPIView.as_view(),name='post_details'),
    path('post_list/<int:id>/', PostdetailAPIView.as_view(),name='post_list'),
]