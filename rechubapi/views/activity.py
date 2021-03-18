"""View module for handling requests about activities"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rechubapi.models import Activity


class Activities(ViewSet):
    """Rec Hub activities"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized activity instance
        """

        # Create a new Python instance of the Activity class
        # and set its properties from what was sent in the
        # body of the request from the client.
        activity = Activity()
        activity.name = request.data["name"]
        user=request.auth.user
        activity.user = user

        # Try to save the new activity to the database, then
        # serialize the activity instance as JSON, and send the
        # JSON as a response to the client request
        try:
            activity.save()
            serializer = ActivitySerializer(activity, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for an activity

        Returns:
            Response -- Empty body with 204 status code
        """

        activity = Activity.objects.get(pk=pk)
        activity.name = request.data["name"]
        user=request.auth.user
        activity.user = user

        activity.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single activity

        Returns:
            Response -- JSON serialized activity
        """
        try:
            activity = Activity.objects.get(pk=pk)
            serializer = ActivitySerializer(activity, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single activity

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            activity = Activity.objects.get(pk=pk)
            activity.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Activity.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to get all activities

        Returns:
            Response -- JSON serialized list of activities
        """
        activities = Activity.objects.filter(user=request.auth.user)

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = ActivitySerializer(
            activities, many=True, context={'request': request})
        return Response(serializer.data)

class ActivitySerializer(serializers.ModelSerializer):
    """JSON serializer for activities

    Arguments:
        serializers
    """
    class Meta:
        model = Activity
        fields = ('id', 'name', 'user')