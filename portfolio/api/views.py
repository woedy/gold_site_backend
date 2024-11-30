# views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Claim, Payment, Delivery, DeliveryConfirmation
from .serializers import ClaimSerializer, PaymentSerializer, DeliverySerializer, DeliveryConfirmationSerializer

@api_view(['POST'])
def initiate_claim(request):
    """
    API view to initiate a new claim for gold.
    """
    if request.method == 'POST':
        serializer = ClaimSerializer(data=request.data)
        if serializer.is_valid():
            claim = serializer.save()
            return Response(ClaimSerializer(claim).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def make_payment(request, claim_id):
    """
    API view to process payment for a specific claim.
    """
    try:
        claim = Claim.objects.get(id=claim_id)
    except Claim.DoesNotExist:
        return Response({"error": "Claim not found"}, status=status.HTTP_404_NOT_FOUND)

    if claim.status != 'pending':
        return Response({"error": "Claim has already been processed"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save(claim=claim)
            claim.status = 'paid'  # Update claim status to paid
            claim.payment_date = payment.payment_date
            claim.save()

            return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ship_gold(request, claim_id):
    """
    API view to initiate the shipment of gold after payment is confirmed.
    """
    try:
        claim = Claim.objects.get(id=claim_id)
    except Claim.DoesNotExist:
        return Response({"error": "Claim not found"}, status=status.HTTP_404_NOT_FOUND)

    if claim.status != 'paid':
        return Response({"error": "Payment not made yet"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        serializer = DeliverySerializer(data=request.data)
        if serializer.is_valid():
            delivery = serializer.save(claim=claim)
            claim.status = 'shipped'  # Update claim status to shipped
            claim.shipment_date = delivery.estimated_delivery_date
            claim.save()

            return Response(DeliverySerializer(delivery).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def confirm_delivery(request, delivery_id):
    """
    API view to confirm the delivery of gold.
    """
    try:
        delivery = Delivery.objects.get(id=delivery_id)
    except Delivery.DoesNotExist:
        return Response({"error": "Delivery not found"}, status=status.HTTP_404_NOT_FOUND)

    if delivery.delivery_status == 'delivered':
        return Response({"error": "Gold already delivered"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        serializer = DeliveryConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            delivery_confirmation = serializer.save(delivery=delivery)
            delivery.delivery_status = 'delivered'  # Mark the delivery as complete
            delivery.actual_delivery_date = delivery_confirmation.confirmation_date
            delivery.save()

            # Update the claim status to completed
            claim = delivery.claim
            claim.status = 'completed'
            claim.delivery_date = delivery_confirmation.confirmation_date
            claim.save()

            return Response(DeliveryConfirmationSerializer(delivery_confirmation).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
