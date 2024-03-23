from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    create_referral_code,
    delete_referral_code,
    get_referral_code_by_email,
    get_referrals_by_referrer_id)

app_name = 'stakewolle'

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('referral_codes/create/', create_referral_code,
         name='referral_code_create'),
    path('referral_codes/delete/', delete_referral_code,
         name='referral_code_delete'),
    path('referral_codes/get/<str:email>/', get_referral_code_by_email,
         name='get_referral_code_by_email'),
    path('users/<int:referrer_id>/', get_referrals_by_referrer_id,
         name='get_referrals_by_referrer_id'),
]
