from django.db.models import fields
from rest_framework import pagination, serializers
from rest_framework.reverse import reverse as rest_reverse

from accounts.api.serializers import UserPublicSerializers

from ..models import Category, Task


class CategorySerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "uri"]

    def get_uri(self, obj):
        request = self.context.get("request")
        return rest_reverse(
            "blog-api:category-api", kwargs={"category_slug": obj.slug}, request=request
        )


class TaskSerializers(serializers.ModelSerializer):
    user = UserPublicSerializers(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Task
        fields = list(
            (
                "id",
                "name",
                "user",
                "description",
                "created_at",
                "updated_at",
                "price",
                "category",
                "picture",
            )
        )
        read_only_fields = ["picture"]
