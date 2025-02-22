

from django.contrib.auth import get_user_model

from accounts.api.custom_jwt import CustomJWTAuthentication
from activities.models import AllActivity
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
def add_portfolio_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")
        title = request.data.get('title', "")
        _type = request.data.get('type', "")
        image = request.data.get('image', "")
        content_data = request.data.get('content', [])

        # Validation for required fields
        if not user_id:
            errors['user_id'] = ['User ID is required.']
        if not title:
            errors['title'] = ['Title is required.']
        if not image:
            errors['image'] = ['Image URL is required.']

        if not _type:
            errors['type'] = ['Portfolio type is required.']


        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']


        # Check if the portfolio title is already taken
        if Portfolio.objects.filter(title=title).exists():
            errors['title'] = ['A portfolio with this title already exists.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        # Create the new portfolio
        try:
            portfolio = Portfolio.objects.create(
                user=user,  # Associate the portfolio with the authenticated user
                title=title,
                type=_type,
                image=image
            )
        except Exception as e:
            payload['message'] = "Failed to create portfolio"
            payload['error'] = str(e)
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Create associated content for the portfolio
        content_list = []
        for item in content_data:
            try:
                content_type = item.get('type', "")
                value = item.get('value', "")
                quantity = item.get('quantity', 0)
                content_image = item.get('image', "")

                # Validate required fields for content
                if not content_type or not value or not content_image:
                    errors[content_type] = ['All fields (type, value, quantity, image) are required.']
                    continue

                # Create the content object
                content = Content.objects.create(
                    portfolio=portfolio,
                    type=content_type,
                    value=value,
                    quantity=int(quantity),
                    image=content_image
                )
                content_list.append({
                    "id": content.id,
                    "type": content.type,
                    "value": content.value,
                    "quantity": content.quantity,
                    "image": content.image
                })
            except Exception as e:
                errors[item.get('type', 'Unknown')] = [str(e)]

        if errors:
            payload['message'] = "Some content items were not added due to validation errors."
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        # Prepare response data
        data["id"] = portfolio.id
        data["title"] = portfolio.title
        data["image"] = portfolio.image.url if portfolio.image else None  # Handle image field properly
        #data["content"] = content_list

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload, status=status.HTTP_201_CREATED)










@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def list_user_portfolio_view(request):
    payload = {}
    data = {}
    errors = {}

    # Get search query and pagination parameters
    user_id = request.query_params.get('user_id', '')
    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10  # Number of items per page

    # Validation for required fields
    if not user_id:
        errors['user_id'] = ['User ID is required.']

    try:
        user = User.objects.get(user_id=user_id)
    except:
        errors['user_id'] = ['User does not exist.']




    # Retrieve portfolios for the authenticated user
    user_portfolios = Portfolio.objects.filter(user=user)

    # Apply search filter if a search query is provided
    if search_query:
        user_portfolios = user_portfolios.filter(Q(title__icontains=search_query))

    # Paginate the results
    paginator = Paginator(user_portfolios, page_size)

    try:
        paginated_portfolios = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_portfolios = paginator.page(1)  # Return first page if page_number is not an integer
    except EmptyPage:
        paginated_portfolios = paginator.page(paginator.num_pages)  # Return last page if out of range

    # Serialize paginated portfolios
    serialized_portfolios = PortfolioSerializer(paginated_portfolios, many=True).data

    # Prepare pagination information
    data['portfolios'] = serialized_portfolios
    data['pagination'] = {
        'page_number': paginated_portfolios.number,
        'total_pages': paginator.num_pages,
        'next': paginated_portfolios.next_page_number() if paginated_portfolios.has_next() else None,
        'previous': paginated_portfolios.previous_page_number() if paginated_portfolios.has_previous() else None,
        'total_items': paginator.count  # Total number of portfolios available for this user
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)
 


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def content_detail_view(request):
    payload = {}
    data = {}
    errors = {}

    # Retrieve content ID from query parameters
    content_id = request.query_params.get('content_id', None)

    if not content_id:
        errors['content_id'] = ["Content ID is required."]

    try:
        # Fetch the content item by ID
        content = Content.objects.get(id=content_id)
    except Content.DoesNotExist:
        errors['content_id'] = ['Content does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    # Serialize the content details
    content_serializer = ContentSerializer(content)

    # Prepare the response payload
    payload['message'] = "Successful"
    payload['data'] = content_serializer.data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_portfolio_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        portfolio_id = request.data.get('portfolio_id', "")
        title = request.data.get('title', "")
        image = request.data.get('image', "")

        if not portfolio_id:
            errors['id'] = ['Portfolio ID is required.']

        # Check if the portfolio exists
        try:
            portfolio = Portfolio.objects.get(id=portfolio_id)
        except:
            errors['id'] = ['Portfolio does not exist.']

        # Validate title if provided
        if title and Portfolio.objects.filter(title=title).exclude(id=portfolio_id).exists():
            errors['title'] = ['A portfolio with this title already exists.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        # Update fields only if provided and not empty
        if title:
            portfolio.title = title
        if image:
            portfolio.image = image

        portfolio.save()

        # Log the activity (if applicable)
        new_activity = AllActivity.objects.create(
            subject="Portfolio Edited",
            body=f"{portfolio.title} was edited."
        )
        new_activity.save()

        data["id"] = portfolio.id
        data["title"] = portfolio.title
        data["image"] = portfolio.image.url if portfolio.image else None

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_content_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        content_id = request.data.get('content_id', "")
        content_type = request.data.get('type', "")
        value = request.data.get('value', "")
        quantity = request.data.get('quantity', None)
        total = request.data.get('total', "")
        image = request.data.get('image', "")

        if not content_id:
            errors['id'] = ['Content ID is required.']

        # Check if the content exists
        try:
            content_item = Content.objects.get(id=content_id)
        except:
            errors['id'] = ['Content does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        # Update fields only if provided and not empty
        if content_type:
            content_item.type = content_type
        if value:
            content_item.value = value
        if quantity is not None:  # Check for None to allow 0 as a valid quantity
            content_item.quantity = quantity
        if total:
            content_item.total = total
        if image:
            content_item.image = image

        content_item.save()

        # Log the activity (if applicable)
        new_activity = AllActivity.objects.create(
            subject="Content Edited",
            body=f"{content_item.type} was edited."
        )
        new_activity.save()

        data["id"] = content_item.id
        data["type"] = content_item.type
        data["value"] = content_item.value
        data["quantity"] = content_item.quantity
        data["total"] = content_item.total
        data["image"] = content_item.image.url

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)