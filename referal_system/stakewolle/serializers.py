from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .mixins import UsernameValidationMixin
from .models import ReferralCode, ReferralRelationship
import stakewolle.templates as templates


class SignUpSerializer(
     UserCreateSerializer,
     UsernameValidationMixin):
    '''Сериализатор для регистрации пользователя.'''
    email = serializers.EmailField()
    username = serializers.CharField()
    referral_code = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'referral_code']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs: dict[str, any]) -> dict[str, any]:
        username = attrs.get('username')
        email = attrs.get('email')
        if User.objects.filter(username=username, email=email).exists():
            raise serializers.ValidationError(
                templates.USER_ALREADY_EXISTS_ERROR
            )
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                templates.USERNAME_ALREADY_EXISTS_ERROR
            )
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                templates.EMAIL_ALREADY_EXISTS_ERROR
            )
        return attrs

    def create(self, validated_data: dict[str, any]) -> any:
        referral_code = validated_data.pop('referral_code', None)
        user = User.objects.create_user(**validated_data)
        if referral_code:
            try:
                referrer = ReferralCode.objects.get(
                    code=referral_code).user
                ReferralRelationship.objects.create(
                    referrer=referrer, referral=user)
            except ReferralCode.DoesNotExist:
                pass
        return user


class ReferralCodeSerializer(serializers.ModelSerializer):
    '''Сериализатор для работы с реферальными кодами.'''
    expiration_date = serializers.DateField()
    code = serializers.CharField(read_only=True)

    class Meta:
        model = ReferralCode
        fields = ['code', 'expiration_date']
