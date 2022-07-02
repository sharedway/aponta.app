"""[summary]

[description]
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [         
            "username",
            "email",
            "token",
            "app_settings", 
            "first_name",
            "last_name",
            "authToken",
            "id",
        ]
