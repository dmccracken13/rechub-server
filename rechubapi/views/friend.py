"""View module for handling requests about friends"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rechubapi.models import Friend
from django.contrib.auth.models import User



class Friends(ViewSet):
    """Rec Hub friends"""

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