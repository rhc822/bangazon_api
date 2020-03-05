from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazon_customer_api.models import PaymentType, Customer

# Required Imports for functionality Above ^ allows use of framework Viewset, Response, Serializers(what changes data type) PaymentType and Customer are Models we created for blueprints later. JB- Comment

# Establishing Class for Payment Type Serializer. Converts Payment Type Data for consumption as JSON.

class PaymentTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for payment types

    Arguments:
        serializers.HyperlinkedModelSerializer

    This is a Jeremiah Bell Disaster
    """

    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='paymenttype',
            lookup_field='id'
        )
        fields = ('id', 'merchant_name', 'acct_number', 'expiration_date', 'customer_id', 'created_at')

        depth = 2

# Handling GET requests for Data of one payment type
class PaymentTypes(ViewSet):
        def retrieve(self, request, pk=None):
            """This is supposed to Handle GET requests for one payment type

            Return:
                This returns a json serialized payment type instance

            """

            try:
                payment_type = PaymentType.objects.get(pk=pk)
                serializer = PaymentTypeSerializer(payment_type,
                context = {'request': request})
                return Response(serializer.data)
            except Exception as ex:
                return HttpResponseServerError(ex)

        def list(self, request):
            """Handle Gets for payment type

            Return:
                This returns json serialized(jsonified) list of payment types
            """

            payment_types = PaymentType.objects.all()

            customer = self.request.query_params.get('customer', None)

            if customer is not None:
                payment_types = payment_types.filter(customer_id=customer)

            serializer = PaymentTypeSerializer(payment_types, many = True, context={'request': request})

            return Response(serializer.data)

        def create(self, request):
                """Handle POST operations

                Returns:
                    Response -- JSON serialized Payment Type instance
                """
                newPaymentType = PaymentType()
                newPaymentType.merchant_name = request.data["merchant_name"]
                newPaymentType.acct_number = request.data["acct_number"]
                newPaymentType.expiration_date = request.data["expiration_date"]
                newPaymentType.customer = request.auth.user.customer
                newPaymentType.created_at = request.data["created_at"]
                newPaymentType.save()

                serializer = PaymentTypeSerializer(newPaymentType, context={'request': request})

                return Response(serializer.data)