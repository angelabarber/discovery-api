from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from discoveryapi.models import Trait


class TraitView(ViewSet):
    """Category View set"""

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        try:
            traits = Trait.objects.all()
            serializer = TraitSerializer(traits, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        try:
            trait = Trait.objects.get(pk=pk)
            serializer = TraitSerializer(trait)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class TraitSerializer(serializers.ModelSerializer):
    """Serializer for Trait model"""

    class Meta:
        model = Trait
        fields = ("id", "name", "category_name")
