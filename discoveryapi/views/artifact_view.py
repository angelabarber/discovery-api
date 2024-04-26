from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from discoveryapi.models import Artifact, Site, Trait


class ArtifactView(ViewSet):
    """View set for Artifact model"""

    def create(self, request):
        try:
            # Extract user from request
            user = request.auth.user

            traits = []
            for trait_id in request.data["traits"]:
                trait = Trait.objects.get(pk=trait_id)
                traits.append(trait)

            # Deserialize and validate site data
            site_data = request.data.get("site")
            if site_data:
                site_serializer = SiteSerializer(data=site_data)
                site_serializer.is_valid(raise_exception=True)
                site = site_serializer.save()
            else:
                site = None

            # Create artifact instance
            artifact = Artifact()
            artifact.name = request.data["name"]
            artifact.description = request.data["description"]
            artifact.image_url = request.data.get("imageUrl", "")
            artifact.user = user
            artifact.site = site
            artifact.save()

            # Set many-to-many relationship between artifact and traits
            artifact.traits.set(traits)

            # Serialize and return artifact data
            serializer = ArtifactSerializer(artifact)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    # def create(self, request):
    #     try:
    #         # Extract user from request
    #         user = request.auth.user

    #         # Extract trait IDs from request data
    #         location_ids = request.data.get("location", [])
    #         material_ids = request.data.get("material", [])
    #         condition_ids = request.data.get("condition", [])
    #         trait_ids = location_ids + material_ids + condition_ids

    #         # Get traits based on IDs
    #         traits = Trait.objects.filter(pk__in=trait_ids)

    #         # Deserialize and validate site data
    #         site_data = request.data.get("site")
    #         if not site_data:
    #             raise serializers.ValidationError("Site data is required")

    #         site_serializer = SiteSerializer(data=site_data)
    #         site_serializer.is_valid(raise_exception=True)
    #         site = site_serializer.save()

    #         # Create artifact instance
    #         artifact = Artifact()
    #         artifact.name = request.data["name"]
    #         artifact.description = request.data["description"]
    #         artifact.image_url = request.data.get("imageUrl", "")
    #         artifact.user = user
    #         artifact.site = site

    #         artifact.save()

    #         # Set many-to-many relationship between artifact and traits
    #         artifact.traits.set(traits)

    #         # Serialize and return artifact data
    #         serializer = ArtifactSerializer(artifact)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     except serializers.ValidationError as ex:
    #         return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    #     except Exception as ex:
    #         return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

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


class TraitSerializer(serializers.ModelSerializer):
    """Serializer for Trait model"""

    class Meta:
        model = Trait
        fields = ("name", "category_name")


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
    traits = TraitSerializer(many=True)

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
