from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Referral
from django.core.cache import cache
from .serializers import UserSerializer, ReferralListSerializer
from .utils import generate_verification_code, generate_invite_code


def index(request):
    return HttpResponse(f"Here's your num: {generate_verification_code()}")


class PhoneAuthView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        verification_code = generate_verification_code()
        cache.set(f"verification_code_{phone_number}", verification_code, timeout=300)

        return Response(
            {"message": "Verification code sent!", "code": verification_code},
            status=status.HTTP_200_OK,
        )


class VerifyCodeView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        code = request.data.get("code")

        cached_code = cache.get(f"verification_code_{phone_number}")
        if cached_code and cached_code == code:
            user, created = User.objects.get_or_create(
                phone_number=phone_number,
                defaults={"invite_code": generate_invite_code()},
            )
            return Response(
                {"invite_code": user.invite_code}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid verification code."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProfileView(APIView):
    def get(self, request):
        phone_number = request.data.get("phone_number")
        user = User.objects.get(phone_number=phone_number)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        phone_number = request.data.get("phone_number")
        invite_code = request.data.get("invite_code")

        user = User.objects.get(phone_number=phone_number)
        referrer = User.objects.filter(invite_code=invite_code).first()

        if referrer and not user.activated_invite_code:
            user.activated_invite_code = invite_code
            user.save()

            Referral.objects.create(referrer=referrer, referred_user=user)
            return Response(
                {"message": "Invite code activated!"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid invite code or already activated."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ReferralListView(APIView):
    def get(self, request):
        phone_number = request.data.get("phone_number")
        user = User.objects.get(phone_number=phone_number)

        referrals = Referral.objects.filter(referrer=user)
        serializer = ReferralListSerializer(referrals, many=True)

        return Response(serializer.data)
