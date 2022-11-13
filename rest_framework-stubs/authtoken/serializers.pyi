from rest_framework import serializers

class AuthTokenSerializer(serializers.Serializer):
    username: serializers.CharField
    password: serializers.CharField
    token: serializers.CharField
