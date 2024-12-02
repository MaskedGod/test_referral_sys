from django.urls import path
from .views import index, PhoneAuthView, VerifyCodeView, ProfileView, ReferralListView

urlpatterns = [
    path("code/", index, name="index"),
    path("auth/", PhoneAuthView.as_view(), name="phone_auth"),
    path("verify/", VerifyCodeView.as_view(), name="verify_code"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("referrals/", ReferralListView.as_view(), name="referrals"),
]
