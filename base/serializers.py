from rest_framework import serializers

class UrlSerializer(serializers.Serializer):
	urls = serializers.ListField(child=serializers.CharField())
	email = serializers.CharField()