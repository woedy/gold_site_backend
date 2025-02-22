from django.urls import path

from claims.api.views import change_claim_status_view, edit_claim_view, initiate_claim_view


app_name = 'claims'

urlpatterns = [
    path('initiate-claim/', initiate_claim_view, name="initiate_claim_view"),
    path('edit-claim/', edit_claim_view, name="edit_claim_view"),
    path('change-claim-status/', change_claim_status_view, name="change_claim_status_view"),

]
