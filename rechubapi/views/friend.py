"""View module for handling requests about friends"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rechubapi.models import Friend


class Friends(ViewSet):
    """Rec Hub friends"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized friend instance
        """

        # Create a new Python instance of the Friend class
        # and set its properties from what was sent in the
        # body of the request from the client.
        friend = Friend()
        friend.friend = request.data["friend"]
        user=request.auth.user
        friend.user = user

        # Try to save the new friend to the database, then
        # serialize the activity instance as JSON, and send the
        # JSON as a response to the client request
        try:
            friend.save()
            serializer = FriendSerializer(friend, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single friend

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            friend = Friend.objects.get(pk=pk)
            friend.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Friend.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single friend

        Returns:
            Response -- JSON serialized friend
        """
        try:
            friend = Friend.objects.get(pk=pk)
            serializer = FriendSerializer(friend, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all friends

        Returns:
            Response -- JSON serialized list of friends
        """
        friends = Friend.objects.filter(user=request.auth.user)

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = FriendSerializer(
            friends, many=True, context={'request': request})
        return Response(serializer.data)

class FriendSerializer(serializers.ModelSerializer):
    """JSON serializer for friends

    Arguments:
        serializers
    """
    class Meta:
        model = Friend
        fields = ('id', 'friend', 'user')