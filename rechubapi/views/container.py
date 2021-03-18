"""View module for handling requests about containers"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rechubapi.models import Container


class Containers(ViewSet):
    """Rec Hub containers"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized container instance
        """

        # Create a new Python instance of the Container class
        # and set its properties from what was sent in the
        # body of the request from the client.
        container = Container()
        container.name = request.data["name"]
        user=request.auth.user
        container.user = user

        # Try to save the new container to the database, then
        # serialize the activity instance as JSON, and send the
        # JSON as a response to the client request
        try:
            container.save()
            serializer = ContainerSerializer(container, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for a container

        Returns:
            Response -- Empty body with 204 status code
        """

        container = Container.objects.get(pk=pk)
        container.name = request.data["name"]
        user=request.auth.user
        container.user = user

        container.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single container

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            container = Container.objects.get(pk=pk)
            container.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Container.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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