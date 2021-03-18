"""View module for handling requests about trips"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rechubapi.models import Trip, Activity


class Trips(ViewSet):
    """Rec Hub trips"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized trip instance
        """

        # Create a new Python instance of the Trip class
        # and set its properties from what was sent in the
        # body of the request from the client.
        trip = Trip()
        trip.location = request.data["location"]
        user=request.auth.user
        trip.user = user
        activity = Activity.objects.get(pk=request.data["activity"])
        trip.activity = activity
        trip.date = request.data["date"]

        # Try to save the new trip to the database, then
        # serialize the activity instance as JSON, and send the
        # JSON as a response to the client request
        try:
            trip.save()
            serializer = TripSerializer(trip, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for an trip

        Returns:
            Response -- Empty body with 204 status code
        """

        trip = Trip.objects.get(pk=pk)
        trip.location = request.data["location"]
        user=request.auth.user
        trip.user = user
        activity = Activity.objects.get(pk=request.data["activity"])
        trip.activity = activity
        trip.date = request.data["date"]

        trip.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single trip

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            trip = Trip.objects.get(pk=pk)
            trip.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Trip.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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