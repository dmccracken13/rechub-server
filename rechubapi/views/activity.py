"""View module for handling requests about activities"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rechubapi.models import Activity


class Activities(ViewSet):
    """Rec Hub activities"""

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