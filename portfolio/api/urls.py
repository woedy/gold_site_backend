from django.urls import path

from accounts.api.views import register_user, verify_user_email, resend_email_verification, UserLogin, \
    PasswordResetView, confirm_otp_password_view, resend_password_otp, new_password_reset_view, remove_user_view, \
    edit_profile, list_all_users_view, get_user_details_view, archive_user_view, unarchive_user_view, \
    list_all_archived_users_view, delete_user_view

app_name = 'portfolio'

urlpatterns = [
    #path('register-user/', register_user, name="register_user"),


]
