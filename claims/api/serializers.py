# serializers.py
from portfolio.models import Content, Portfolio
from rest_framework import serializers

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'type', 'value', 'quantity', 'total', 'image']




class ListContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'type', 'value', 'quantity', 'total', 'image']


class PortfolioSerializer(serializers.ModelSerializer):
    contents_count = serializers.SerializerMethodField()  # Add a field for content count
    contents = ListContentSerializer(many=True)

    class Meta:
        model = Portfolio
        fields = ['id', 'title', 'image', 'contents_count', 'contents']

    def get_contents_count(self, obj):
        return obj.contents.count()  # Count the number of associated content items






