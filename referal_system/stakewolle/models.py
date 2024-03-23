from django.db import models
from django.contrib.auth.models import User


class ReferralCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True)
    expiration_date = models.DateField()

    def __str__(self):
        return self.code


class ReferralRelationship(models.Model):
    referrer = models.ForeignKey(
        User, related_name='referral_relationships',
        on_delete=models.CASCADE)
    referral_code = models.CharField(max_length=20)
    referral = models.ForeignKey(
        User, related_name='referred_by',
        on_delete=models.CASCADE)

    class Meta:
        unique_together = ('referrer', 'referral')
