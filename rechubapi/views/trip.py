"""View module for handling requests about trips"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rechubapi.models import Trip


class Trips(ViewSet):
    """Rec Hub trips"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single trip

        Returns:
            Response -- JSON serialized trip
        """
        try:
            trip = Trip.objects.get(pk=pk)
            serializer = TripSerializer(trip, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all trips

        Returns:
            Response -- JSON serialized list of trips
        """
        trips = Trip.objects.filter(user=request.auth.user)

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = TripSerializer(
            trips, many=True, context={'request': request})
        return Response(serializer.data)

class TripSerializer(serializers.ModelSerializer):
    """JSON serializer for trips

    Arguments:
        serializers
    """
    class Meta:
        model = Trip
        fields = ('id', 'location', 'activity', 'date', 'user')