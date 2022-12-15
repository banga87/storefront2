from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import User

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']