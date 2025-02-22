from delivery.models import Delivery, DeliveryStatus
from portfolio.models import Content
from rest_framework import serializers


class AssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'type', 'value', 'quantity', 'total', 'image']


class DeliverySerializer(serializers.ModelSerializer):
    assets = AssetsSerializer(many=True)

    class Meta:
        model = Delivery
        fields = "__all__"


class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatus
        fields = "__all__"



class TrackingDeliverySerializer(serializers.ModelSerializer):
    assets = AssetsSerializer(many=True)  # Serialize related assets
    delivery_status = serializers.SerializerMethodField()  # Use a custom method for delivery_status

    class Meta:
        model = Delivery
        fields = "__all__"

    def get_delivery_status(self, obj):
        # Retrieve related delivery statuses
        delivery_statuses = DeliveryStatus.objects.filter(delivery=obj)
        return DeliveryStatusSerializer(delivery_statuses, many=True).data



