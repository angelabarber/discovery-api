from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from discoveryapi.models import Artifact, Site


class ArtifactView(ViewSet):
    """View set for Artifact model"""

    def create(self, request):
        """Handle POST operations"""
        serializer = ArtifactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item"""
        try:
            artifact = Artifact.objects.get(pk=pk)
            serializer = ArtifactSerializer(artifact)
            return Response(serializer.data)
        except Artifact.DoesNotExist:
            return Response(
                {"error": "Artifact not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request, pk=None):
        """Handle PUT requests"""
        try:
            artifact = Artifact.objects.get(pk=pk)
            serializer = ArtifactSerializer(artifact, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Artifact.DoesNotExist:
            return Response(
                {"error": "Artifact not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item"""
        try:
            artifact = Artifact.objects.get(pk=pk)
            artifact.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Artifact.DoesNotExist:
            return Response(
                {"error": "Artifact not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        try:
            artifacts = Artifact.objects.all()
            serializer = ArtifactSerializer(artifacts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class SiteSerializer(serializers.ModelSerializer):
    """Serializer for Site model"""

    class Meta:
        model = Site
        fields = ("name",)


class ArtifactSerializer(serializers.ModelSerializer):
    """Serializer for Artifact model"""

    site = (
        SiteSerializer()
    )  # Include the SiteSerializer for the nested representation of the Site

    imageUrl = serializers.CharField(source="image_url")

    class Meta:
        model = Artifact
        fields = (
            "id",
            "name",
            "description",
            "imageUrl",
            "site",
            "traits",
        )
