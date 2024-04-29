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
            # site_data = request.data.get("site")
            # if site_data:
            #     site_serializer = SiteSerializer(data=site_data)
            #     site_serializer.is_valid(raise_exception=True)
            #     site = site_serializer.save()
            # else:
            #     site = None

            site_id = request.data.get("site")
            site = None

            if site_id:
                site = Site.objects.get(pk=site_id)

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

    def update(self, request, pk=None):
        """Handle PUT requests"""

        try:
            user = request.auth.user

            traits = []
            for trait_id in request.data["traits"]:
                trait = Trait.objects.get(pk=trait_id)
                traits.append(trait)

            artifact = Artifact.objects.get(pk=pk)
            artifact.user = user
            artifact.save()
            artifact.traits.set(traits)

            # serializer = ArtifactSerializer(artifact)
            # if serializer.is_valid():
            #     serializer.save()
            #     return Response(serializer.data)
            # else:
            #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Artifact.DoesNotExist:
            return Response(
                {"error": "Artifact not found"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as ex:
            return HttpResponseServerError(ex)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

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

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            artifact = Artifact.objects.get(pk=pk)
            artifact.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Artifact.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        try:
            artifact = (
                Artifact.objects.select_related("site", "user")
                .prefetch_related("traits")
                .get(pk=pk)
            )
            serializer = ArtifactSerializer(artifact)
            return Response(serializer.data)
        except Artifact.DoesNotExist:
            return Response(
                {"error": "Artifact not found"}, status=status.HTTP_404_NOT_FOUND
            )


# def retrieve(self, request, pk=None):
#     """Handle GET requests for single item

#     Returns:
#         Response -- JSON serialized instance
#     """
#     try:
#         artifact = Artifact.objects.get(pk=pk)
#         artifact_serializer = ArtifactSerializer(artifact)
#         traits = Trait.objects.filter(artifact_id=pk)
#         trait_serializer = TraitSerializer(traits, many=True)
#         artifact_data = artifact_serializer.data
#         artifact_data["traits"] = trait_serializer.data
#         return Response(artifact_data)

#     except Exception as ex:
#         return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class TraitSerializer(serializers.ModelSerializer):
    """Serializer for Trait model"""

    class Meta:
        model = Trait
        fields = ("id", "name", "category_name")


class SiteSerializer(serializers.ModelSerializer):
    """Serializer for Site model"""

    class Meta:
        model = Site
        fields = (
            "id",
            "name",
        )


class ArtifactUserSerializer(serializers.ModelSerializer):
    """JSON Serializer"""

    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")

    class Meta:
        model = User
        fields = (
            "id",
            "firstName",
            "lastName",
            "username",
        )


class ArtifactSerializer(serializers.ModelSerializer):
    """Serializer for Artifact model"""

    user = ArtifactUserSerializer(many=False)
    site = (
        SiteSerializer()
    )  # Include the SiteSerializer for the nested representation of the Site

    imageUrl = serializers.CharField(source="image_url")
    traits = TraitSerializer(many=True)
    site = SiteSerializer(many=False)

    class Meta:
        model = Artifact
        fields = (
            "id",
            "name",
            "description",
            "imageUrl",
            "site",
            "user",
            "traits",
        )
