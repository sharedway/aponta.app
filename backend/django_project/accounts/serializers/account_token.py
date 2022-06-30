"""[summary]

[description]
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model


class AccountTokenSerializer(serializers.ModelSerializer):
    session_token = serializers.SerializerMethodField()

    def get_session_token(self, obj):
        return obj.getSessionToken()

    class Meta:
        model = get_user_model()
        fields = [
            "session_token",
        ]
