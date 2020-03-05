"""View module for handling requests about orders"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazon_customer_api.models import Order


class OrdersSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Orders

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='orders',
            lookup_field='id'
        )
        fields = ('id', 'created_at', 'customer_id', 'payment_type_id')


class Orders(ViewSet):
    """Orders for Bangazon"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single Order

        Returns:
            Response -- JSON serialized order instance
        """
        try:
            area = Order.objects.get(pk=pk)
            serializer = OrdersSerializer(area, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to Order resource

        Returns:
            Response -- JSON serialized list of Order
        """
        areas = Order.objects.all()
        serializer = OrdersSerializer(
            areas,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)