from django.contrib.auth.models import AbstractUser
from django.db.models import CharField


# Create your models here.

class User(AbstractUser):
    # 1. username(아이디), password, email은 부모가 이미 가지고 있음 (상속)
    nickname = CharField(max_length=50)

    class Meta:
        # unique_together는 테이블 수준의 제약 조건 (자바의 @UniqueConstraint)
        unique_together = ('email', 'nickname')

