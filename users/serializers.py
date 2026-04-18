# users/serializers.py
from rest_framework import serializers

# 1. 공통 필드 및 로그인용 (Base DTO 역할)
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        error_messages={
            'blank': '아이디를 입력해주세요.',
            'required': '아이디 필드가 누락되었습니다.',
        }
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={
            'blank': '비밀번호를 입력해주세요.',
            'required': '비밀번호 필드가 누락되었습니다.',
        }
    )

# 2. 로그인을 상속받은 가입용 (Extended DTO 역할)
class SignUpSerializer(LoginSerializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            'blank': '이메일을 입력해주세요.',
            'invalid': '유효한 이메일 형식이 아닙니다.',
            'required': '이메일 필드가 누락되었습니다.',
        }
    )
    nickname = serializers.CharField(
        max_length=50,
        required=True,
        error_messages={
            'blank': '닉네임을 입력해주세요.',
            'required': '닉네임 필드가 누락되었습니다.',
        }
    )