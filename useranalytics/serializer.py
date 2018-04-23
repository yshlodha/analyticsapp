from rest_framework import serializers

class ClientSerializer(serializers.Serializer):
    """
    """
    email = serializers.EmailField(required=True)


class ClientDataSerializer(serializers.Serializer):
    page_name = serializers.CharField(max_length=500, required=True)
    timestamp = serializers.DateTimeField(required=True)
    location = serializers.DictField(child=serializers.CharField())
    userinfo = serializers.DictField(child=serializers.CharField())
    sessioninfo = serializers.DictField(child=serializers.CharField())
    api_key = serializers.CharField(max_length=32, required=True)