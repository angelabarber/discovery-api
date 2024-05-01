from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from discoveryapi.models import City


class CityView(ViewSet):
    """Category View set"""

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        try:
            cities = City.objects.all()
            serializer = CitySerializer(cities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        try:
            cities = City.objects.get(pk=pk)
            serializer = CitySerializer(cities)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class CitySerializer(serializers.ModelSerializer):
    """Serializer for Site model"""

    imageUrl = serializers.CharField(source="image_url")

    class Meta:
        model = City
        fields = ("id", "name", "location", "significance", "imageUrl")
