from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from discoveryapi.models import Artifact, Comment


class CommentView(ViewSet):
    """Review view set"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response --JSON serialized instance
        """
        user = request.auth.user

        comment = Comment()
        comment.text = request.data["text"]
        comment.artifact = Artifact.objects.get(pk=request.data["artifact_id"])
        comment.user = user

        try:
            comment.save()
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(
                {"Stupid mortal malformed object dummy": ex.args[0]},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        try:
            comments = Comment.objects.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class UserReviewSerializer(serializers.ModelSerializer):
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


class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    user = UserReviewSerializer(many=False)

    class Meta:
        model = Comment
        fields = (
            "id",
            "artifact",
            "user",
            "text",
        )
