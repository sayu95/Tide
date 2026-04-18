from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.serializers import SignUpSerializer, LoginSerializer
from users.service.users_service import UserService


# Create your views here.
@api_view(['POST'])  # 회원가입은 데이터 생성이니 POST!
def signup_view(request):
    # 1. DTO(Serializer)로 데이터 검증
    serializer = SignUpSerializer(data=request.data)
    # 검증 실패 시 바로 400 에러 던짐
    serializer.is_valid(raise_exception=True)

    service = UserService()
    user = service.signup(**serializer.validated_data)

    return Response({
        "message": f"{user.nickname}님, 가입을 축하합니다!"
    }, status=201)


@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    service = UserService()
    # 서비스에서 authenticate가 실패하면 401을 raise
    # 여기서는 그냥 성공 케이스만 생각
    user = service.login(**serializer.validated_data)

    return Response({"message": f"{user.nickname}님 환영합니다!"
                     }, status=200)