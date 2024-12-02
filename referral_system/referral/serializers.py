from rest_framework import serializers
from .models import User, Referral


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number", "invite_code", "activated_invite_code"]


class ReferralListSerializer(serializers.ModelSerializer):
    referred_user_phone = serializers.CharField(source="referred_user.phone_number")

    class Meta:
        model = Referral
        fields = ["referred_user_phone", "activated_at"]
