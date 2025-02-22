

from django.contrib.auth import get_user_model


from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from accounts.api.custom_jwt import CustomJWTAuthentication
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from bank_account.models import BankAccount
from claims.models import Claim
from portfolio.models import Portfolio
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomJWTAuthentication])
def get_dashboard_data_view(request):
    payload = {}
    data = {}
    errors = {}
    total_value = 0.0
    metal_total_value = 0.0  # Initialize total value for Metal portfolios

    claim_paid = False

    balanceInfo = {}

    if request.method == 'GET':
        user_id = request.query_params.get('user_id', '')

        if not user_id:
            errors['user_id'] = ['User ID is required.']

        try:
            user = User.objects.get(user_id=user_id)  # Use 'id' instead of 'user_id'
        except User.DoesNotExist:
            errors['user_id'] = ['User does not exist.']
            return Response({"message": "Errors", "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the user's bank account
        try:
            bank_account = BankAccount.objects.get(user=user)
        except BankAccount.DoesNotExist:
            errors['bank_account'] = ['Bank account does not exist for this user.']
            return Response({"message": "Errors", "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve all portfolios for the authenticated user
        try:
            portfolios = Portfolio.objects.filter(user=user)  # Assuming related_name='portfolios'

            # Calculate total value for each portfolio and total value for Metal portfolios
            serialized_portfolios = []
            for portfolio in portfolios:
                portfolio_value = calculate_portfolio_total(portfolio)
                total_value += portfolio_value

                # Check if portfolio type is Metal
                if portfolio.type == 'Metal':
                    metal_total_value += portfolio_value

                # Serialize portfolio data including contents
                serialized_portfolio = {
                    'id': portfolio.id,
                    'title': portfolio.title,
                    'image': portfolio.image.url if portfolio.image else None,
                    'total_value': portfolio_value,  # Total value for this portfolio
                    'contents': []  # Initialize contents list
                }

                # Serialize contents of the portfolio
                contents = portfolio.contents.all()  # Assuming related_name='content'
                for content in contents:
                    serialized_content = {
                        'type': content.type,
                        'value': content.value,
                        'quantity': content.quantity,
                        'total': content.total,
                        'image': content.image.url if content.image else None
                    }
                    serialized_portfolio['contents'].append(serialized_content)

                serialized_portfolios.append(serialized_portfolio)

            balanceInfo['gp_balance'] = bank_account.balance
            balanceInfo['assets_total'] = total_value
            balanceInfo['metal_total_value'] = metal_total_value  # Include total value for Metal portfolios

            data['portfolio'] = serialized_portfolios

        except Exception as e:
            payload['message'] = "An error occurred"
            payload['error'] = str(e)
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            claim = Claim.objects.get(client=user)  # Adjusted to match your Claim model's foreign key
            data['claim_status'] = claim.status  # Assuming you want to return the claim status
        except Claim.DoesNotExist:
            data['claim_status'] = None  # Handle case where claim does not exist
        
        data['balanceInfo'] = balanceInfo
        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


def calculate_portfolio_total(portfolio):
    total_value = 0.0
    contents = portfolio.contents.all()  # Assuming related_name='content'

    for content in contents:
        # Assuming content has fields: 'quantity' and 'value'
        # Convert value to float if it's stored as a string
        total_value += content.quantity * float(content.value.replace('$', '').replace(',', ''))

    return total_value
