from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from accounts.api.custom_jwt import CustomJWTAuthentication
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_dashboard_data_view(request):
    payload = {}
    data = {}
    errors = {}

    claim_paid = False

    portfolio = [
        {
            'title': 'Cryptocurrency',
            'image': 'https://png.pngtree.com/png-vector/20211027/ourmid/pngtree-d-realistic-bitcoin-cryptocurrency-vector-icon-copper-gold-coin-with-shadow-png-image_4011395.png',
            'content': [
                {
                    'type': 'Bitcoin',
                    'value': '$ 28,000',
                    'quantity': '12',
                    'total': '$ 3,452',
                    'image': 'https://upload.wikimedia.org/wikipedia/commons/4/46/Bitcoin.svg'
                },
                {
                    'type': 'Ethereum',
                    'value': '$ 1,800',
                    'quantity': '12',
                    'total': '$ 3,452',
                    'image': 'https://upload.wikimedia.org/wikipedia/commons/0/01/Ethereum_logo_2014.svg'
                },
                {
                    'type': 'Cardano',
                    'value': '$ 0.35',
                    'quantity': '12',
                    'total': '$ 3,452',
                    'image': 'https://upload.wikimedia.org/wikipedia/commons/5/53/Cardano_Logo_2020.svg'
                }
            ]
        },
        {
            'title': 'Gold',
            'image': 'https://png.pngtree.com/png-vector/20231026/ourmid/pngtree-realistic-gold-bars-png-image_10370401.png',
            'content': [
                {
                    'type': 'Gold Coins',
                    'value': '$ 1,900/oz',
                    'quantity': '12',
                    'total': '$ 3,452',
                    'image': 'https://www.example.com/gold-coins-image.png'
                },
                {
                    'type': 'Gold Bars',
                    'value': '$ 1,850/oz',
                    'quantity': '12',
                    'total': '$ 3,452',
                    'image': 'https://www.example.com/gold-bars-image.png'
                },
                {
                    'type': 'Jewelry',
                    'value': '$ 2,000/oz',
                    'quantity': '12',
                    'total': '$ 3,452',
                    'image': 'https://www.example.com/jewelry-image.png'
                }
            ]
        }
    ]


    balanceInfo = {
        'gp_balance': '$ 20,000',
        'asset_value': '$ 12,056,343',
        'assets_total': '$ 18,681,500'
      }
    
    if request.method == 'GET':
        user_id = request.query_params.get('user_id', '')

        if not user_id:
            errors['user_id'] = ['User ID is required.']

        



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        

    data['portfolio'] = portfolio
    data['balanceInfo'] = balanceInfo
    data['claim_paid'] = claim_paid
    
    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)
