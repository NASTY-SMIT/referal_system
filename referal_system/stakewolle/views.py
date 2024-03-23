from datetime import date
import random
import string

from adrf.decorators import api_view
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.core.cache import cache
from djoser.serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

from .models import ReferralCode, ReferralRelationship
from .serializers import ReferralCodeSerializer
import stakewolle.templates as templates


@api_view(['POST'])
async def create_referral_code(
     request: Request,
     *args: any,
     **kwargs: any) -> Response:
    '''Создание реферального кода.'''
    serializer = ReferralCodeSerializer(data=request.data)
    if serializer.is_valid():
        referral_code_data = serializer.validated_data
        user: User = request.user
        existing_referral_code = await sync_to_async(
            ReferralCode.objects.filter(user=user).exists)()
        if existing_referral_code:
            return Response(
                templates.EXISTING_REFERRAL_CODE_ERROR,
                status=status.HTTP_400_BAD_REQUEST)
        code = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=20
            ))
        expiration_date = referral_code_data['expiration_date']
        if expiration_date <= date.today():
            return Response(
                templates.EXPIRY_DATE_ERROR,
                status=status.HTTP_400_BAD_REQUEST)
        referral_code = ReferralCode(
            user=user,
            code=code,
            expiration_date=expiration_date)
        referral_code_cache_key = f'referral_code_{user.email}'
        cache.set(referral_code_cache_key, code, timeout=None)
        await sync_to_async(referral_code.save)()
        serializer.validated_data['code'] = code
        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
async def delete_referral_code(request: Request) -> Response:
    '''Удаление реферального кода.'''
    user: User = request.user
    try:
        referral_code = await sync_to_async(
            ReferralCode.objects.get)(user=user)
        await sync_to_async(referral_code.delete)()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ReferralCode.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
async def get_referral_code_by_email(request: Request, email: str) -> Response:
    '''Получение кода по email реферера.'''
    referral_code_cache_key = f'referral_code_{email}'
    cached_referral_code = cache.get(referral_code_cache_key)
    if cached_referral_code:
        return Response(cached_referral_code, status=status.HTTP_200_OK)
    try:
        user = await sync_to_async(User.objects.get)(email=email)
        referral_code = await sync_to_async(
            ReferralCode.objects.get)(user=user)
        serializer = ReferralCodeSerializer(referral_code)
        referral_code_data = serializer.data
        cache.set(referral_code_cache_key, referral_code_data, timeout=None)
        return Response(referral_code_data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(
            templates.USER_NOT_FOUND_ERROR,
            status=status.HTTP_404_NOT_FOUND)
    except ReferralCode.DoesNotExist:
        return Response(
            templates.REFERRAL_CODE_NOT_FOUND_ERROR,
            status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
async def get_referrals_by_referrer_id(request: Request, referrer_id: int):
    '''Получение всех рефералов по id реферера'''
    try:
        referrer = await sync_to_async(User.objects.get)(id=referrer_id)
        relationships = await sync_to_async(
            ReferralRelationship.objects.filter)(referrer=referrer)
        referrals = await sync_to_async(
            lambda: [
                relationship.referral for relationship in relationships
                ])()
        serializer = UserSerializer(referrals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(
            templates.REFERER_NOT_FOUND_ERROR,
            status=status.HTTP_404_NOT_FOUND)
