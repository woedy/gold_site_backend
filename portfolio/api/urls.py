from django.urls import path

from accounts.api.views import register_user, verify_user_email, resend_email_verification, UserLogin, \
    PasswordResetView, confirm_otp_password_view, resend_password_otp, new_password_reset_view, remove_user_view, \
    edit_profile, list_all_users_view, get_user_details_view, archive_user_view, unarchive_user_view, \
    list_all_archived_users_view, delete_user_view
from portfolio.api.portfolio_view import add_portfolio_view, content_detail_view, edit_content_view, edit_portfolio_view, list_user_portfolio_view

app_name = 'portfolio'

urlpatterns = [
    path('add-portfolio/', add_portfolio_view, name="add_portfolio_view"),
    path('edit-portfolio/', edit_portfolio_view, name="edit_portfolio_view"),
    path('edit-content/', edit_content_view, name="edit_content_view"),
    path('list-user-portfolio/', list_user_portfolio_view, name="list_user_portfolio_view"),
    path('content-details/', content_detail_view, name="content_detail_view"),


]
