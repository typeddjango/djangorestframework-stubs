from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(label=_("Password"), style={"input_type": "password"}, trim_whitespace=False)
