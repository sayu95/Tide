# users/serializers.py
from rest_framework import serializers


# 1. 공통 필드만 있는 베이스 (또는 로그인용)
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

# 2. 로그인을 상속받아 필드를 추가한 가입용
class SignUpSerializer(LoginSerializer):
    email = serializers.EmailField()
    nickname = serializers.CharField(max_length=50)