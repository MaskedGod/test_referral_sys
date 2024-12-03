from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User, Referral
from django.core.cache import cache
from .serializers import UserSerializer, ReferralListSerializer
from .utils import get_uptime, generate_verification_code, generate_invite_code


class HealthCheckView(APIView):
    """
    API endpoint for health check and service status.
    """

    @swagger_auto_schema(
        operation_description="Returns health check information with service status and a sample verification code."
    )
    def get(self, request):
        verification_code = generate_verification_code()
        service_status = "Healthy"
        uptime = get_uptime()

        return Response(
            {
                "status": service_status,
                "uptime": uptime,
                "message": "Service is running smoothly!",
                "verification_code_sample": verification_code,
            }
        )


class PhoneAuthView(APIView):
    """
    Send a verification code to the user's phone number.
    """

    @swagger_auto_schema(
        operation_description="Send a verification code to the specified phone number.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "phone_number": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Phone number to send the verification code to.",
                    default=1234567890,
                )
            },
            required=["phone_number"],
        ),
    )
    def post(self, request):
        phone_number = request.data.get("phone_number")

        cache_key = f"verification_code_{phone_number}"
        cache.delete(cache_key)

        verification_code = generate_verification_code()
        cache.set(cache_key, verification_code, timeout=180)

        return Response(
            {"message": "Verification code sent!", "code": verification_code},
            status=status.HTTP_200_OK,
        )


class VerifyCodeView(APIView):
    """
    Verify the code sent to the user's phone number.
    """

    @swagger_auto_schema(
        operation_description="Verify the received code for the provided phone number. Optionally, provide a custom code for verification.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "phone_number": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Phone number to send the verification code to.",
                    default=1234567890,
                ),
                "code": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Code received by the user.",
                    default=1234,
                ),
            },
            required=["phone_number", "code"],
        ),
    )
    def post(self, request):
        phone_number = request.data.get("phone_number")
        code = request.data.get("code")
        custom_code = request.data.get("custom_code")

        # Use custom_code if provided, otherwise use cached code
        if custom_code:
            cached_code = custom_code
        else:
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
    """
    Retrieve or update the user's profile and activate invite codes.
    """

    @swagger_auto_schema(
        operation_description="Get the user's profile information.",
        manual_parameters=[
            openapi.Parameter(
                "phone_number",
                openapi.IN_QUERY,
                description="Phone number to retrieve the profile.",
                type=openapi.TYPE_STRING,
                default=1234567890,
            )
        ],
    )
    def get(self, request):
        phone_number = request.data.get("phone_number")
        user = User.objects.get(phone_number=phone_number)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Activate an invite code for the user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "phone_number": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Phone number to send the verification code to.",
                    default=1234567890,
                ),
                "invite_code": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Code received by the user.",
                    default=123456,
                ),
            },
            required=["phone_number", "invite_code"],
        ),
    )
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
    """
    Retrieve the list of referrals for the user.
    """

    @swagger_auto_schema(
        operation_description="Get a list of referrals for the current user.",
        manual_parameters=[
            openapi.Parameter(
                "phone_number",
                openapi.IN_QUERY,
                description="Phone number to retrieve referrals.",
                type=openapi.TYPE_STRING,
                default=1234567890,
            )
        ],
    )
    def get(self, request):
        phone_number = request.data.get("phone_number")
        user = User.objects.get(phone_number=phone_number)

        referrals = Referral.objects.filter(referrer=user)
        serializer = ReferralListSerializer(referrals, many=True)

        return Response(serializer.data)
