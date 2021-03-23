"""View module for handling requests about items"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rechubapi.models import Item, Activity, Container, Status, Type
from django.contrib.auth.models import User


class Items(ViewSet):
    """Rec Hub items"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized item instance
        """

        # Create a new Python instance of the Item class
        # and set its properties from what was sent in the
        # body of the request from the client.
        item = Item()
        item.name = request.data["name"]
        user=request.auth.user
        item.user = user
        activity = Activity.objects.get(pk=request.data["activity"])
        item.activity = activity
        try: 
            container = Container.objects.get(pk=request.data["container"])
            item.container = container
        except Container.DoesNotExist: 
            item.container = None
        item_status = Status.objects.get(pk=request.data["status"])
        item.status = item_status
        type = Type.objects.get(pk=request.data["type"])
        item.type = type
        item.quantity = request.data["quantity"]

        # Try to save the new activity to the database, then
        # serialize the item instance as JSON, and send the
        # JSON as a response to the client request
        try:
            item.save()
            serializer = ItemSerializer(item, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for an item

        Returns:
            Response -- Empty body with 204 status code
        """

        item = Item.objects.get(pk=pk)
        item.name = request.data["name"]
        user=request.auth.user
        item.user = user
        activity = Activity.objects.get(pk=request.data["activity"])
        item.activity = activity
        try: 
            container = Container.objects.get(pk=request.data["container"])
            item.container = container
        except Container.DoesNotExist: 
            item.container = None        
        item_status = Status.objects.get(pk=request.data["status"])
        item.status = item_status
        type = Type.objects.get(pk=request.data["type"])
        item.type = type
        item.quantity = request.data["quantity"]

        item.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            item = Item.objects.get(pk=pk)
            item.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Activity.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized item
        """
        try:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all items

        Returns:
            Response -- JSON serialized list of items
        """
        items = Item.objects.filter(user=request.auth.user)

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = ItemSerializer(
            items, many=True, context={'request': request})
        return Response(serializer.data)

class UserItemSerializer(serializers.ModelSerializer):
    """JSON serializer for items

    Arguments:
        serializers
    """
    class Meta:
        model = User
        fields = ('id',)

class ItemSerializer(serializers.ModelSerializer):
    """JSON serializer for items

    Arguments:
        serializers
    """
    user = UserItemSerializer (many=False)
    class Meta:
        model = Item
        fields = ('id', 'name', 'user', 'activity', 'container', 'status', 'type', 'quantity' )
        depth = 1