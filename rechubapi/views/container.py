"""View module for handling requests about containers"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rechubapi.models import Container


class Containers(ViewSet):
    """Rec Hub containers"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single container

        Returns:
            Response -- JSON serialized container
        """
        try:
            container = Container.objects.get(pk=pk)
            serializer = ContainerSerializer(container, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all containers

        Returns:
            Response -- JSON serialized list of containers
        """
        containers = Container.objects.filter(user=request.auth.user)

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = ContainerSerializer(
            containers, many=True, context={'request': request})
        return Response(serializer.data)

class ContainerSerializer(serializers.ModelSerializer):
    """JSON serializer for containers

    Arguments:
        serializers
    """
    class Meta:
        model = Container
        fields = ('id', 'name', 'user')