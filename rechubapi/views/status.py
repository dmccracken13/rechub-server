"""View module for handling requests about statuses"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rechubapi.models import Status


class Statuses(ViewSet):
    """Rec Hub statuses"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single status

        Returns:
            Response -- JSON serialized status
        """
        try:
            status = Status.objects.get(pk=pk)
            serializer = StatusSerializer(status, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all statuses

        Returns:
            Response -- JSON serialized list of statuses
        """
        statuses = Status.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = StatusSerializer(
        statuses, many=True, context={'request': request})
        return Response(serializer.data)

class StatusSerializer(serializers.ModelSerializer):
    """JSON serializer for statuses

    Arguments:
        serializers
    """
    class Meta:
        model = Status
        fields = ('id', 'name')