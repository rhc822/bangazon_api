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
        depth = 2

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

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single order

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            delete_order = Order.objects.get(pk=pk)
            delete_order.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Payment Type instance
        """
        newOrder = Order()
        newOrder.customer_id = request.auth.user.customer.id
        newOrder.payment_type_id = request.data["payment_type_id"]
        newOrder.created_at = request.data["created_at"]
        newOrder.save()

        serializer = OrdersSerializer(newOrder, context={'request': request})

        return Response(serializer.data)