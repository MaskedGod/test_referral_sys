from django.db import models


class User(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    invite_code = models.CharField(max_length=6, unique=True)
    activated_invite_code = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Referral(models.Model):
    referrer = models.ForeignKey(
        User, related_name="referrals", on_delete=models.CASCADE
    )
    referred_user = models.OneToOneField(
        User, related_name="referred_by", on_delete=models.CASCADE
    )
    activated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("referrer", "referred_user")
