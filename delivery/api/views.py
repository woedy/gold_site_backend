

from django.contrib.auth import get_user_model

from accounts.api.custom_jwt import CustomJWTAuthentication
from activities.models import AllActivity
from delivery.api.serializers import DeliverySerializer, TrackingDeliverySerializer
from delivery.models import Delivery, DeliveryStatus
from portfolio.api.serializers import ContentSerializer, PortfolioSerializer
from portfolio.models import Content, Portfolio
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
def select_assets_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")
        assets = request.data.get('assets', [])

        # Validation for required fields
        if not user_id:
            errors['user_id'] = ['User ID is required.']
        if not assets:
            errors['assets'] = ['Assets required.']


        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        try:
            delivery = Delivery.objects.get(client=user)
        except:
            errors['user_id'] = ['User Delivery does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)



    
        for item in assets:
            content = Content.objects.get(id=item)
            delivery.assets.add(content)

        delivery.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload, status=status.HTTP_201_CREATED)

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delivery_location_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")
        location_name = request.data.get('location_name', "")
        lat = request.data.get('lat', "")
        lng = request.data.get('lng', "")

        # Validation for required fields
        if not user_id:
            errors['user_id'] = ['User ID is required.']
        if not location_name:
            errors['location_name'] = ['Location name is required.']
        if not lat:
            errors['lat'] = ['lat is required.']
        if not lng:
            errors['lng'] = ['lng is required.']



        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        try:
            delivery = Delivery.objects.get(client=user)
        except:
            errors['user_id'] = ['User Delivery does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        delivery.location_name = location_name
        delivery.lat = lat
        delivery.lng = lng
        delivery.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload, status=status.HTTP_201_CREATED)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def billing_address_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")
        address_line_1 = request.data.get('address_line_1', "")
        address_line_2 = request.data.get('address_line_2', "")
        address_line_3 = request.data.get('address_line_3', "")

        # Validation for required fields
        if not user_id:
            errors['user_id'] = ['User ID is required.']
        if not address_line_1:
            errors['address_line_1'] = ['Address line 1 is required.']


        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        try:
            delivery = Delivery.objects.get(client=user)
        except:
            errors['user_id'] = ['User Delivery does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        delivery.billing_address_1 = address_line_1
        delivery.billing_address_2 = address_line_2
        delivery.billing_address_3 = address_line_3
        delivery.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload, status=status.HTTP_201_CREATED)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def payment_option_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")
        option = request.data.get('option', "")
     
        # Validation for required fields
        if not user_id:
            errors['user_id'] = ['User ID is required.']
        if not option:
            errors['option'] = ['Option is required.']


        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        try:
            delivery = Delivery.objects.get(client=user)
        except:
            errors['user_id'] = ['User Delivery does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        delivery.payment_option = option

        delivery.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload, status=status.HTTP_201_CREATED)






 
@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delivery_overview_view(request):
    payload = {}
    data = {}
    errors = {}
    
    user_id = request.query_params.get('user_id', None)

    # Validation for required fields
    if not user_id:
        errors['user_id'] = ['User ID is required.']

    try:
        user = User.objects.get(user_id=user_id)
    except:
        errors['user_id'] = ['User does not exist.']
    try:
        delivery = Delivery.objects.get(client=user)
    except:
        errors['user_id'] = ['User Delivery does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    # Serialize the content details
    content_serializer = DeliverySerializer(delivery)

    # Prepare the response payload
    payload['message'] = "Successful"
    payload['data'] = content_serializer.data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def place_order_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")
     
        # Validation for required fields
        if not user_id:
            errors['user_id'] = ['User ID is required.']

        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        try:
            delivery = Delivery.objects.get(client=user)
        except:
            errors['user_id'] = ['User Delivery does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        delivery.delivery_status = "Initiated"
        delivery.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomJWTAuthentication])
def add_sub_status_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")
        _status = request.data.get('status', "")
        sub_status_list = request.data.get('sub_status', [])

        # Validation for required fields
        if not user_id:
            errors['user_id'] = ['User ID is required.']
        if not _status:
            errors['status'] = ['Status is required.']

        try:
            user = User.objects.get(user_id=user_id)  # Use 'id' instead of 'user_id'
        except User.DoesNotExist:
            errors['user_id'] = ['User does not exist.']

        try:
            delivery = Delivery.objects.get(client=user)
        except Delivery.DoesNotExist:
            errors['delivery'] = ['User Delivery does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        # Create associated sub-statuses for the delivery
        existing_sub_statuses = DeliveryStatus.objects.filter(delivery=delivery).values_list('sub_status', flat=True)

        for item in sub_status_list:
            if item in existing_sub_statuses:
                continue  # Skip if the sub-status already exists

            # Create new sub-status since it doesn't exist
            DeliveryStatus.objects.create(
                delivery=delivery,
                delivery_status=_status,
                sub_status=item
            )

        # Prepare response data
        data["id"] = delivery.id

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload, status=status.HTTP_201_CREATED)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomJWTAuthentication])
def track_order_view(request):
    payload = {}
    errors = {}

    if request.method == 'GET':
        user_id = request.query_params.get('user_id', None)
        tracking_number = request.query_params.get('tracking_number', None)

        # Validate required fields
        if not user_id:
            errors['user_id'] = ['User ID is required.']
        if not tracking_number:
            errors['tracking_number'] = ['Tracking number is required.']

        if errors:
            return Response({"message": "Errors", "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        # Validate user existence
        try:
            user = User.objects.get(user_id=user_id)  # Use 'id' instead of 'user_id'
        except User.DoesNotExist:
            return Response({"message": "Error", "errors": {"user": ["User does not exist."]}}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the delivery based on the tracking number and user
        try:
            delivery = Delivery.objects.get(tracking_number=tracking_number, client=user)

            # Serialize the delivery data
            serializer = TrackingDeliverySerializer(delivery)
            payload['message'] = "Successful"
            payload['data'] = serializer.data

        except Delivery.DoesNotExist:
            return Response({"message": "Error", "errors": {"delivery": ["Delivery not found."]}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "An error occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(payload, status=status.HTTP_200_OK)