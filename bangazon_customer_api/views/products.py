from rest_framework.viewsets import ViewSet
from bangazon_customer_api.models import Product
from rest_framework import serializers
from rest_framework.response import Response
from django.http import HttpResponseServerError


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for product
    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id', 'name', 'price', 'description', 'quantity', 'location', 'product_type')

class Products(ViewSet):
    def list(self, request):

        """Handle GET requests to park attractions resource
        Returns:
            Response -- JSON serialized list of park attractions
        """

        products = Product.objects.all()
        serializer = ProductSerializer(
            products,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """This is supposed to Handle GET requests for one product type

        Return:
            This returns a json serialized product type instance

        """

        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(
                product,
                context = {'request': request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Payment Type instance
        """
        newProduct = Product()
        newProduct.name = request.data["name"]
        newProduct.price = request.data["price"]
        newProduct.description = request.data["description"]
        newProduct.quantity = request.data["quantity"]
        newProduct.location = request.data["location"]
        newProduct.created_at = request.data["created_at"]
        newProduct.customer = request.auth.user.customer
        newProduct.product_type_id = request.data["product_type_id"]
        newProduct.save()

        serializer = ProductSerializer(newProduct, context={'request': request})

        return Response(serializer.data)