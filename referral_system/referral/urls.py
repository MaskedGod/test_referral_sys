from django.urls import path
from .views import (
    HealthCheckView,
    PhoneAuthView,
    VerifyCodeView,
    ProfileView,
    ReferralListView,
)

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health_check"),
    path("auth/", PhoneAuthView.as_view(), name="phone_auth"),
    path("verify/", VerifyCodeView.as_view(), name="verify_code"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("referrals/", ReferralListView.as_view(), name="referrals"),
]
