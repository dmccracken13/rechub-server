"""View module for handling requests about items"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rechubapi.models import Item


class Items(ViewSet):
    """Rec Hub items"""

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

class ItemSerializer(serializers.ModelSerializer):
    """JSON serializer for items

    Arguments:
        serializers
    """
    class Meta:
        model = Item
        fields = ('id', 'name', 'user', 'activity', 'container', 'status', 'type', 'quantity' )