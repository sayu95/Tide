from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from users.models import User


class UserService :
    def signup(self, username, password, email, nickname):
        return User.objects.create_user(
            username=username,
            password=password,
            email=email,
            nickname=nickname
        )


    def login(self, username, password):
        user = authenticate(username = username, password=password)

        # 2. 결과 처리 (자바의 if (user == null) throw ... 와 동일)
        if user is None:
            # DRF가 제공하는 예외를 던지면 자동으로 401 Unauthorized 응답이 나갑니다.
            raise AuthenticationFailed("아이디 또는 비밀번호가 잘못되었습니다.")

        # 3. 인증된 유저 객체 리턴
        return user