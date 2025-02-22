

from django.contrib.auth import get_user_model

from accounts.api.custom_jwt import CustomJWTAuthentication
from activities.models import AllActivity
from claims.models import Claim
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def initiate_claim_view(request):
    payload = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', None)
        claim_ref = request.data.get('claim_ref', "")
        security_answer_1 = request.data.get('security_answer_1', "")
        security_answer_2 = request.data.get('security_answer_2', "")

        # Validate required fields
        if not user_id:
            errors['user_id'] = ['User ID is required.']
        if not claim_ref:
            errors['claim_ref'] = ['Claim reference is required.']
        if not security_answer_1:
            errors['security_answer_1'] = ['Security answer 1 is required.']
        if not security_answer_2:
            errors['security_answer_2'] = ['Security answer 2 is required.']

        try:
            user = User.objects.get(user_id=user_id) 
        except User.DoesNotExist:
            errors['user_id'] = ['User does not exist.']

        # Check for validation errors
        if errors:
            return Response({"message": "Errors", "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user already has an initiated claim
        existing_claims = Claim.objects.filter(client=user, status__in=['Pending', 'Verified', 'Paid'])
        if existing_claims.exists():
            return Response({"message": "Error", "errors": {"claim": ["You already have an initiated claim."]}}, status=status.HTTP_400_BAD_REQUEST)

        # Validate each field individually
        try:
            claim = Claim.objects.get(client=user)

            # Validate claim_ref
            if claim.claim_ref != claim_ref:
                return Response({"message": "Invalid response", "errors": {"claim_ref": "Provided claim reference does not match."}}, status=status.HTTP_400_BAD_REQUEST)

            # Validate security_answer_1
            if claim.security_answer_1 != security_answer_1:
                return Response({"message": "Invalid response", "errors": {"security_answer_1": "Security answer 1 does not match."}}, status=status.HTTP_400_BAD_REQUEST)

            # Validate security_answer_2
            if claim.security_answer_2 != security_answer_2:
                return Response({"message": "Invalid response", "errors": {"security_answer_2": "Security answer 2 does not match."}}, status=status.HTTP_400_BAD_REQUEST)

        except Claim.DoesNotExist:
            return Response({"message": "Error", "errors": {"claim": ["No existing claim found for this user."]}}, status=status.HTTP_404_NOT_FOUND)





        # Create a new claim instance (if validation passes)
        try:
            claim.status="Pending" 
            claim.save()
        except Exception as e:
            return Response({"message": "Error", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Prepare response data
        payload["id"] = claim.id
        payload["claim_ref"] = claim.claim_ref
        payload["status"] = claim.status  # Default status is 'Pending'
        payload["claim_date"] = claim.claim_date.isoformat()  # Format date for JSON response

    return Response({"message": "Successful", "data": payload}, status=status.HTTP_201_CREATED)







@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_claim_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")

        # Validate required fields
        if not user_id:
            errors['user_id'] = ['User ID is required.']


        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        try:
            # Fetch the existing claim
            claim = Claim.objects.get(client=user)
        except Claim.DoesNotExist:
            errors['id'] = ['Claim does not exist or you do not have permission to edit it.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        # Update all fields if provided in the request
        claim_ref = request.data.get('claim_ref', None)
        claim_amount = request.data.get('claim_amount', None)
        verification_date = request.data.get('verification_date', None)
        payment_date = request.data.get('payment_date', None)
        security_question_1 = request.data.get('security_question_1', None)
        security_answer_1 = request.data.get('security_answer_1', None)
        security_question_2 = request.data.get('security_question_2', None)
        security_answer_2 = request.data.get('security_answer_2', None)
        bitcoin_qr = request.FILES.get('bitcoin_qr', None)
        bitcoin_address = request.FILES.get('bitcoin_address', None)

        # Update fields only if provided and not empty
        if claim_ref:
            claim.claim_ref = claim_ref
        if claim_amount is not None:  # Allow 0 as a valid value
            claim.claim_amount = claim_amount
        if verification_date:
            claim.verification_date = verification_date
        if payment_date:
            claim.payment_date = payment_date
        if security_question_1:
            claim.security_question_1 = security_question_1
        if security_answer_1:
            claim.security_answer_1 = security_answer_1
        if security_question_2:
            claim.security_question_2 = security_question_2
        if security_answer_2:
            claim.security_answer_2 = security_answer_2
        if bitcoin_qr:
            claim.bitcoin_qr = bitcoin_qr
        if bitcoin_address:
            claim.bitcoin_address = bitcoin_address

        # Save the updated claim instance
        claim.save()

        # Prepare response data with all updated fields
        data["id"] = claim.id
        data["claim_ref"] = claim.claim_ref
        data["status"] = claim.status
        data["claim_amount"] = str(claim.claim_amount) if claim.claim_amount else None  # Convert Decimal to string for JSON response
        data["verification_date"] = (
            claim.verification_date.isoformat() if claim.verification_date else None
        )
        data["payment_date"] = (
            claim.payment_date.isoformat() if claim.payment_date else None
        )
        data["security_question_1"] = claim.security_question_1
        data["security_answer_1"] = security_answer_1  # Mask sensitive information in response
        data["security_question_2"] = claim.security_question_2
        data["security_answer_2"] = security_answer_2 # Mask sensitive information in response
        data["bitcoin_qr"] = (
            request.build_absolute_uri(claim.bitcoin_qr.url) if claim.bitcoin_qr else None
        )
        data["bitcoin_address"] = (
            request.build_absolute_uri(claim.bitcoin_address.url) if claim.bitcoin_address else None
        )

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)








@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def change_claim_status_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")
        _status = request.data.get('status', "")

        # Validate required fields
        if not user_id:
            errors['user_id'] = ['User ID is required.']

        if not _status:
            errors['status'] = ['Status is required.']


        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        try:
            # Fetch the existing claim
            claim = Claim.objects.get(client=user)
        except Claim.DoesNotExist:
            errors['id'] = ['Claim does not exist or you do not have permission to edit it.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        # Update fields only if provided and not empty
        if _status:
            claim.status = _status

        # Save the updated claim instance
        claim.save()

        # Prepare response data with all updated fields
        data["id"] = claim.id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)
