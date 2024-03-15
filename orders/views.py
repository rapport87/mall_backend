from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem, OrderPayment
from .serializers import OrderSerializer, OrderItemSerializer


class OrderListView(APIView):
    def get(self, request, format=None):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class UserOrdersView(APIView):
    def get(self, request, username):
        orders = Order.objects.filter(username=username).order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class UserOrderItemsView(APIView):
    def get(self, request, username, pk):
        try:
            order = Order.objects.get(username=username, pk=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data)


class OrderDetailView(APIView):
    def get(self, request, pk, format=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateOrderView(APIView):
    def post(self, request):
        try:
            user_id = request.data.get("user_id")
            username = request.data.get("username")
            recipient_name = request.data.get("recipient_name")
            recipient_tel = request.data.get("recipient_tel")
            address = request.data.get("address")
            address_detail = request.data.get("address_detail")
            zip_code = request.data.get("zip_code")
            order_request = request.data.get("order_request")
            payment = request.data.get("payment")
            shipping_fee = request.data.get("shipping_fee")
            order = Order.objects.create(
                user_id=user_id,
                username=username,
                recipient_name=recipient_name,
                recipient_tel=recipient_tel,
                address=address,
                address_detail=address_detail,
                zip_code=zip_code,
                order_request=order_request,
                shipping_fee=shipping_fee,
            )

            OrderPayment.objects.create(
                order=order,
                payment=payment,
            )

            # 주문 품목 정보 추출 및 생성
            order_items_data = request.data.get("order_items", [])
            for item_data in order_items_data:
                OrderItem.objects.create(
                    order=order,
                    product_id=item_data["product_id"],
                    product_name=item_data["product_name"],
                    sale_price=item_data["sale_price"],
                    quantity=item_data["quantity"],
                    thumbnail=item_data["thumbnail"],
                )

            return Response(
                {
                    "success": "created ordered",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"fail": f"occurred some error while creating as {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
