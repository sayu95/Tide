from django.urls import path
from .views import sync_indicator_view  # 위에서 만든 뷰 함수 이름과 같아야 함

urlpatterns = [
    path('sync/', sync_indicator_view, name='sync_indicator'),
]