"""[summary]

[description]
"""

from django.urls import path
from .consumers import Hello

websocket_urlpatterns = [
    path(
        "channels/matchs/<tipo>/<matchid>/",
        Hello.as_asgi(),
    ),
]