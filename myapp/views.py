from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, LoginSerializer
from rest_framework import generics
from .models import Vendor
from .serializers import VendorSerializer
from django.utils import timezone
from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from .models import Vendor
from .serializers import VendorPerformanceSerializer
from rest_framework.permissions import IsAuthenticated



class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response({'message': "Regitered Successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'data' : serializer.validated_data['token']}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# vendor

class VendorListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'id'
    def put(self, request, id):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        try:
            instance = self.get_queryset().get(id=id)
            self.perform_destroy(instance)
            return Response({"message": "Vendor successfully deleted.","data":request.data}, status=status.HTTP_204_NO_CONTENT)
        except Vendor.DoesNotExist:
            return Response({"message": "Vendor not found."},status=status.HTTP_404_NOT_FOUND)

# Purchase Order

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'id'

    def put(self, request, id):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Purchase order successfully deleted."}, status=status.HTTP_204_NO_CONTENT)


# Historical Performance


class VendorPerformanceView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        performance_metrics = self.calculate_performance_metrics(instance)
        serializer = self.get_serializer(performance_metrics)
        return Response(serializer.data)


    def calculate_performance_metrics(self, vendor):
        total_completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
        on_time_delivery_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', delivery_date__lte=timezone.now()).count()
        on_time_delivery_rate = (on_time_delivery_orders / total_completed_orders) * 100 if total_completed_orders > 0 else 0

        quality_rating_avg = PurchaseOrder.objects.filter(vendor=vendor, status='completed').aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0

        response_times = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False).exclude(acknowledgment_date=F('issue_date')).annotate(response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField())).aggregate(avg_response_time=Avg('response_time'))
        average_response_time = response_times['avg_response_time'].total_seconds() if response_times['avg_response_time'] else 0

        total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
        fulfilled_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False).count()
        fulfillment_rate = (fulfilled_orders / total_orders) * 100 if total_orders > 0 else 0

        return {
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': average_response_time,
            'fulfillment_rate': fulfillment_rate
        }


class AcknowledgePurchaseOrder(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=id)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase order does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Update acknowledgment_date to current time
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        return Response({"message": "Purchase order acknowledged successfully"}, status=status.HTTP_200_OK)