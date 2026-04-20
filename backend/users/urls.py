from django.urls import path
from . import views

urlpatterns = [
    # path('주소/', 뷰함수, name='별칭')
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('test/', views.test_connection),
]