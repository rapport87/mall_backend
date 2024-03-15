from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .serializers import CategoryProductsSerializer


class CategoryProductsView(APIView):
    def get(self, request, categories_id):
        try:
            category = Category.objects.get(id=categories_id)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # 카테고리에 속한 상품들을 직렬화하기 위해 수정
        serializer = CategoryProductsSerializer(category)
        return Response(serializer.data["products"])
