from django.urls import path

from delivery.api.views import add_sub_status_view, billing_address_view, delivery_location_view, delivery_overview_view, payment_option_view, place_order_view, select_assets_view, track_order_view



app_name = 'delivery'

urlpatterns = [
    path('assets-selection/', select_assets_view, name="select_assets_view"),
    path('delivery-location/', delivery_location_view, name="delivery_location_view"),
    path('billing-address/', billing_address_view, name="billing_address_view"),
    path('payment-option/', payment_option_view, name="payment_option_view"),
    path('delivery-overview/', delivery_overview_view, name="delivery_overview_view"),
    path('place-order/', place_order_view, name="place_order_view"),
    path('track-order/', track_order_view, name="track_order_view"),
    path('add-sub-status/', add_sub_status_view, name="add_sub_status_view"),

]
