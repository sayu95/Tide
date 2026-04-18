# users/serializers.py
from rest_framework import serializers

def common_error(name):
    return {
        'blank': f'{name}을(를) 입력해주세요.',
        'required': f'{name} 필드가 누락되었습니다.'
    }

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        error_messages=common_error('아이디')
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        error_messages=common_error('비밀번호')
    )

class SignUpSerializer(LoginSerializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            **common_error('이메일'),
            'invalid': '유효한 이메일 형식이 아닙니다.'
        }
    )
    nickname = serializers.CharField(
        max_length=50,
        required=True,
        error_messages=common_error('닉네임')
    )