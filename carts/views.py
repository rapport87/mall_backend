from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from users.models import User
from products.models import Product
from .serializers import CartSerializer


# Create your views here.
class Carts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(user_cart_items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        product_id = request.data.get("product_id")  # product_id 추출

        if (
            product_id
            and Cart.objects.filter(user=request.user, product_id=product_id).exists()
        ):
            return Response(
                {"message": "상품이 이미 존재합니다"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CartSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        if pk is not None:
            try:
                cart_item = Cart.objects.get(pk=pk, user=request.user)
                cart_item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Cart.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            Cart.objects.filter(user=request.user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
